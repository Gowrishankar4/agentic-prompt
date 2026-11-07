#!/usr/bin/env python3
"""Repo checks: manifests, skill frontmatter, formatting, references, configs, example specs, broken fixture."""
import json, pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "plugins/prompt/skills/prompt"
VAL = ROOT / "tools/validate_spec.py"
errors = []
def err(m): errors.append(m); print("ERROR:", m)

market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
for e in market["plugins"]:
    man = json.loads((ROOT / e["source"] / ".claude-plugin/plugin.json").read_text())
    if man["name"] != e["name"]: err("marketplace entry name != plugin name")
    if not re.fullmatch(r"\d+\.\d+\.\d+", man.get("version", "")): err("version must be semver")

text = (SKILL / "SKILL.md").read_text()
m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
fm = dict(re.findall(r"^(\w[\w-]*):\s*(.*)$", m.group(1), re.M)) if m else {}
if set(fm) != {"name", "description"}: err(f"frontmatter keys must be name, description (got {sorted(fm)})")
if fm.get("name") != "prompt": err("skill name must match folder")
if len(text.splitlines()) > 500: err("SKILL.md over 500 lines")

for md in (ROOT / "plugins").rglob("*.md"):
    t = md.read_text()
    for i, line in enumerate(t.splitlines(), 1):
        if re.match(r"^ +\|", line) or re.match(r"^ {1,3}```", line): err(f"{md.relative_to(ROOT)}:{i}: leading spaces")
    for ref in re.findall(r"`((?:\.\./)*(?:references|templates|config|scripts)/[^`\s<]+?\.(?:md|yml|py))`", t):
        if not (md.parent / ref).exists() and not (SKILL / ref).exists(): err(f"{md.relative_to(ROOT)}: missing {ref}")

for y in list((SKILL / "config").glob("*.yml")) + list((ROOT / "examples/configs").glob("*.yml")):
    r = subprocess.run([sys.executable, str(VAL), "--validate-config", str(y)], capture_output=True, text=True)
    if r.returncode: err(f"config invalid: {y.relative_to(ROOT)}\n{r.stdout}")
for s in (ROOT / "examples/specs").glob("*.md"):
    r = subprocess.run([sys.executable, str(VAL), str(s), "--format", "json"], capture_output=True, text=True)
    if r.returncode or json.loads(r.stdout or "[]"): err(f"example spec not clean: {s.name}\n{r.stdout}")
r = subprocess.run([sys.executable, str(VAL), str(ROOT / "tests/fixtures/broken-spec.md"), "--format", "json"], capture_output=True, text=True)
found = {f["check"] for f in json.loads(r.stdout or "[]")}
expected = {"empty-section", "duplicate-id", "criterion-unknown", "criterion-covers", "uncovered-requirement", "tbd-not-listed", "status", "sensitive-data"}
if expected - found: err(f"broken fixture: validator missed {sorted(expected - found)}")

print("OK" if not errors else f"{len(errors)} error(s)")
sys.exit(1 if errors else 0)
