#!/usr/bin/env python3
"""Check a spec (XML, or a markdown file containing an ```xml block) — and optionally a config.

  validate_spec.py <spec.md|spec.xml> [--format md|json]
  validate_spec.py --validate-config <config.yml>

Exit code 0 = no errors, 1 = errors, 2 = usage.
"""
import argparse, json, pathlib, re, sys
import xml.etree.ElementTree as ET

REQUIRED = ["context", "task", "requirements", "acceptance_criteria", "assumptions", "open_questions"]
SENSITIVE = {
    "secrets": [r"(?i)\b(password|secret|api[_-]?key|token)\s*[:=]\s*['\"]?[^\s'\"<>$]{6,}", r"\bAKIA[0-9A-Z]{16}\b",
                r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"[a-z]+://[^\s:/@<>]+:[^\s@<>]+@[^\s/]+"],
    "pii": [r"\b[A-Za-z0-9._%+-]+@(?!example\.(com|org|net)\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", r"\b\d{3}-\d{2}-\d{4}\b"],
    "phi": [r"(?i)\bMRN\s*[:#=]?\s*\d{4,}", r"(?i)\b(DOB|date of birth)\s*[:=]\s*\d"],
    "pci": [r"(?i)\bcvv\s*[:=]\s*\d{3,4}\b"],
}
EVENTS = {"before_interview", "after_classify", "after_spec", "after_approval", "after_execute", "after_validate"}
KEYS = {"version", "mode", "depth", "one_question_at_a_time", "approval_view", "spec_format", "sections", "save_to", "save_on_approval",
        "sensitive_data", "extra_questions", "capabilities", "rules", "include"}
ENTRY = re.compile(r"^(skill:.+|command:/.+|mcp:.+|mcp\?.+|script:.+|subagent:.+|instruction:.+|builtin|none)$")


def extract_xml(text):
    m = re.search(r"```xml\n(.*?)```", text, re.S)
    body = m.group(1) if m else text
    body = body.strip()
    if not body.startswith("<spec"):
        body = f"<spec>{body}</spec>"
    # placeholders like <API_KEY> or <TBD: …> are text, not tags
    body = re.sub(r"<(TBD[^>]*|[A-Z][A-Z0-9_]*)>", lambda x: "&lt;" + x.group(1) + "&gt;", body)
    return body


def check_spec(path, profiles=("secrets", "pii", "phi", "pci")):
    out = []
    add = lambda sev, check, msg: out.append({"severity": sev, "check": check, "message": msg})
    text = pathlib.Path(path).read_text()
    try:
        root = ET.fromstring(extract_xml(text))
    except ET.ParseError as e:
        add("error", "xml", f"spec is not well-formed XML: {e}")
        return out
    for sec in REQUIRED:
        el = root.find(sec)
        if el is None:
            add("error", "missing-section", f"<{sec}> is missing")
        elif not "".join(el.itertext()).strip() and not list(el):
            add("error", "empty-section", f"<{sec}> is empty (write None if nothing applies)")
    reqs = root.findall("./requirements/requirement")
    ids = [r.get("id") for r in reqs]
    if not reqs:
        add("error", "no-requirements", "no <requirement> entries")
    for i in ids:
        if not i:
            add("error", "requirement-id", "a <requirement> has no id")
    for d in {i for i in ids if i and ids.count(i) > 1}:
        add("error", "duplicate-id", f"requirement id {d} is used more than once")
    covered = set()
    for c in root.findall("./acceptance_criteria/criterion"):
        cov = (c.get("covers") or "").split()
        if not cov:
            add("error", "criterion-covers", f"criterion {c.get('id') or '?'} has no covers=")
        for r in cov:
            if r not in ids:
                add("error", "criterion-unknown", f"criterion {c.get('id')} covers unknown requirement {r}")
        covered.update(cov)
    for r in ids:
        if r and r not in covered:
            add("error", "uncovered-requirement", f"{r} has no acceptance criterion")
    oq = "".join(root.find("open_questions").itertext()) if root.find("open_questions") is not None else ""
    everything = "".join(root.itertext())
    for tbd in set(re.findall(r"<TBD:?([^>]*)>", everything)):
        if tbd.strip() and tbd.strip() not in oq:
            add("warn", "tbd-not-listed", f"TBD '{tbd.strip()[:60]}' is not listed in <open_questions>")
    status = root.get("status", "")
    if status and not re.match(r"^(DRAFT|APPROVED \d{4}-\d{2}-\d{2} \(.+\))$", status):
        add("warn", "status", f"status '{status}' should be DRAFT or APPROVED YYYY-MM-DD (<who>)")
    for prof in profiles:
        for rx in SENSITIVE.get(prof, []):
            for n, line in enumerate(text.splitlines(), 1):
                if re.search(rx, line):
                    add("error", "sensitive-data", f"line {n}: possible {prof} value (not shown)")
    return out


def check_config(path):
    try:
        import yaml
    except ImportError:
        print("PyYAML needed: pip install pyyaml"); return 2
    try:
        cfg = yaml.safe_load(pathlib.Path(path).read_text()) or {}
    except yaml.YAMLError as e:
        print(f"YAML error: {e}\nTip: quote entries with '?', e.g. \"mcp?jira comment\""); return 1
    probs = [f"unknown key '{k}'" for k in cfg if k not in KEYS]
    for k, v in {"mode": ("execute", "save", "handoff"), "depth": ("quick", "standard", "deep"), "spec_format": ("xml", "markdown"), "approval_view": ("summary", "spec")}.items():
        if k in cfg and cfg[k] not in v:
            probs.append(f"{k} must be one of {v}")
    for name, chain in (cfg.get("capabilities") or {}).items():
        for e in chain or []:
            s = e.get("use") if isinstance(e, dict) else e
            if not isinstance(s, str) or not (ENTRY.match(s) or re.fullmatch(r"[a-z][a-z0-9-]*", s)):
                probs.append(f"capabilities.{name}: bad entry {e!r}")
    seen = set()
    for r in cfg.get("rules") or []:
        rid = r.get("id")
        if rid in seen: probs.append(f"rules: duplicate id {rid}")
        seen.add(rid)
        if r.get("enabled") is False: continue
        if not any(k in r for k in ("trigger", "on_event", "when")):
            probs.append(f"rules.{rid}: no trigger (trigger / on_event / when)")
        bad = set(r.get("on_event") or []) - EVENTS
        if bad: probs.append(f"rules.{rid}: unknown events {sorted(bad)}")
        acts = [k for k in ("use", "ask", "instruction_file") if k in r] + (["instruction"] if "instruction" in r and "use" not in r else [])
        if len(acts) != 1: probs.append(f"rules.{rid}: needs exactly one of use / ask / instruction / instruction_file")
    for q in cfg.get("extra_questions") or []:
        if not q.get("question"): probs.append(f"extra_questions.{q.get('id')}: no question")
    print("\n".join(probs) if probs else "✅ Config valid.")
    return 1 if probs else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", nargs="?")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--validate-config", metavar="FILE")
    a = ap.parse_args()
    if a.validate_config:
        sys.exit(check_config(a.validate_config))
    if not a.spec:
        ap.print_usage(); sys.exit(2)
    f = check_spec(a.spec)
    if a.format == "json":
        print(json.dumps(f, indent=2))
    else:
        print("✅ Spec valid." if not f else "\n".join(f"- [{x['severity']}] {x['check']}: {x['message']}" for x in f))
    sys.exit(1 if any(x["severity"] == "error" for x in f) else 0)


if __name__ == "__main__":
    main()
