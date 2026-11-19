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

**How Jordan fills it for one lead**
1. Collect public facts only (their own website or listing). No invented reviews, ratings or prices. No prospect logo.
2. Run, from the repo root: `python3 demo/fill_lead_demo.py --business "..." --city "..." --trade "..." --first-name "..." --hours "..." --services "A; B; C"`. It escapes all text, refuses to write a page if any placeholder is left, and writes `demo/<name>-<random>.html`.
   (By hand instead: copy `demo/lead-template.html`, search-and-replace the six placeholders, repeat the SERVICES list line once per service, delete the instructions comment at the top, and check that `grep -c '{{' yourfile.html` prints 0.)
3. Open the file in a browser and check the banner, the text and the chat button.
4. **Do not commit or push it without Roy's approval.** Pages pushed to main are public to anyone with the link.
5. Send nothing from here. Any outreach follows the normal approval process.

**What the chat does:** the page loads the existing RoMar Digital chat widget (`chat-widget.js`, the same one as the main site). It answers as RoMar Digital's assistant and does not know the lead's business. A business-specific chat agent would need a new Retell agent, which needs Roy's approval. No new phone line is used. The page has no phone CTA to a demo line. The CTA goes to the existing contact section (`../#contact`).
