# Question bank

Take questions in order for the subtype; skip any already answered by the request, the code or the caller. `quick` = the first 3 unanswered, `standard` = up to 8, `deep` = all, then probe each spec section for gaps. Offer likely answers where you can.

## Technical — all subtypes
1. What should be true when this is done — the observable outcome?
2. Who uses it — role, system, API consumer?
3. Where does it live? *(confirm what inspection found)*
4. Inputs and outputs — shapes, formats, examples (placeholders only)?
5. Edge cases — empty, invalid, duplicate, concurrent, timeout?
6. Constraints — stack, versions, performance budget, backwards compatibility?
7. How will we know it works — the tests or checks you'd accept?
8. What must not change (out of scope)?

## Additions by subtype

| Subtype | Ask |
|---|---|
| `feature` | Permissions — who may, who must be blocked? · Data — new fields, migrations, retention? · Rollout — flag, staged, all at once; how to undo? |
| `bug` | Steps to reproduce · expected vs actual · since when, which environments · logs or errors (redacted) · workaround in use? |
| `integration` | Which service and API version · auth method (env var names only) · rate limits and retries · sandbox access · failure behaviour when it's down? |
| `refactor` | Why now — what hurts? · behaviour that must stay identical · test coverage today · how far it may spread? |
| `architecture` | Scale and growth expected · non-functional priorities (latency, cost, availability) · existing systems it must fit · decisions already made? |
| `data` | Sources and owners · volume · freshness · who may see it · retention and deletion? |

## General — all subtypes
1. What is the deliverable — document, plan, analysis, content, decision?
2. Who is the audience, and what should they do after reading it?
3. Scope — what's in, what's out?
4. Sources to use or avoid?
5. Length, format, tone, language?
6. Deadline and review path?
7. What makes it excellent rather than acceptable?
8. An example of something similar you liked?

## Additions by subtype

| Subtype | Ask |
|---|---|
| `research` | The question to answer · how recent the sources must be · depth vs breadth · how confident the answer must be? |
| `documentation` | Reader's level · docs this sits beside · what they must be able to do afterwards? |
| `planning` | Goal and success metric · constraints (people, budget, dates) · decisions already made · who approves? |
| `content` | Channel · voice · call to action · words or claims to avoid? |
| `analysis` | The decision it informs · data available · the comparison that matters · how the result will be presented? |
