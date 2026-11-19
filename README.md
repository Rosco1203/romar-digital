# romar-digital
Rosco's files

## Personal demo page for a lead (`demo/lead-template.html`)

A one-page, chatbot-only demo that a lead can open to see a demo made for them. Branded RoMar Digital, labeled as a demo, noindex, not linked from the site navigation. **Nothing is sent to anyone by these files.**

**Placeholders** (each appears as double curly braces around the UPPERCASE name):

| Placeholder | What to put there |
|---|---|
| `BUSINESS_NAME` | The business name as it appears publicly |
| `CITY` | City (and state if it helps) |
| `TRADE` | Trade or business type, e.g. Plumbing |
| `CONTACT_FIRST_NAME` | First name of the person we are writing to |
| `HOURS` | Their published hours, copied from a public source |
| `SERVICES` | Their published services, separated by `;` |

**Rules for these pages**
- A page is built only after a lead engages (replies, or asks for a demo). Not in advance, not in bulk.
- Roy approves each link before it is shared. **Nothing is sent automatically**; these files send nothing and call no API. Any outreach follows the normal approval process.
- The URL is an unguessable random token. It never contains the business name or any lead info: `demo/p/<token>/` (160-bit token, lowercase letters and digits, e.g. `demo/p/n5tiv5mtntiynvpk7qt47qu7vzkpcndy/`). The page itself, including its `<title>`, does show the business name, which is fine.
- The mapping from token to lead is kept in a local log **outside this repo** (default `/workspace/business/sales/lead-demo-tokens.csv`, or `--log PATH`). `.gitignore` blocks `lead-demo-tokens*` files and any CSV under `demo/`. Never put a token-to-name list in the repo.
- The live chat uses the main-site agent as built (`chat-widget.js`, same as the main site). It answers as RoMar Digital's assistant and does not know the lead's business. A business-specific agent would need a new Retell agent and Roy's approval. No new phone line is used and the page has no phone CTA to a demo line. The CTA goes to the main site's contact section.
- To take a page down, delete its token directory (`demo/p/<token>/`), merge that deletion, and mark the log row removed.

**How Jordan fills it for one lead**
1. Collect public facts only (their own website or listing). No invented reviews, ratings or prices. No prospect logo.
2. Run, from the repo root: `python3 demo/fill_lead_demo.py --business "..." --city "..." --trade "..." --first-name "..." --hours "..." --services "A; B; C"`. It escapes all text, refuses to write a page if any placeholder is left, writes `demo/p/<token>/index.html`, prints the relative URL (`demo/p/<token>/`), and appends a row to the local log. It refuses to overwrite an existing token directory unless you add `--force`. To regenerate a known page use `--token <existing token> --force`.
   (By hand instead: copy `demo/lead-template.html` to `demo/p/<random token>/index.html`, search-and-replace the six placeholders, repeat the SERVICES list line once per service, change every `../` in href/src to `../../../`, delete the instructions comment at the top, check that `grep -c '{{' index.html` prints 0, and add the lead to the local log yourself.)
3. Open the file in a browser and check the banner, the text and the chat button.
4. **Do not commit or push it until Roy has approved that link.** Pages pushed to main are public to anyone who has the URL. Do not share the URL until Roy approves it.
