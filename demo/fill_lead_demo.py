#!/usr/bin/env python3
"""Fill demo/lead-template.html for ONE lead. Static fill, stdlib only. Sends nothing, calls no API.

Example:
  python3 demo/fill_lead_demo.py --business "Sample Plumbing Co." --city "Fort Lauderdale" --trade "Plumbing" \
      --first-name "Sam" --hours "Mon-Fri 8 AM-5 PM" --services "Leak repair; Drain cleaning; Water heaters"

Every value is HTML-escaped. SERVICES is split on ';' or newlines, one list item each.
The script refuses to write a page if any {{PLACEHOLDER}} is left. Output: demo/<slug>-<random>.html (unguessable name).
Do NOT commit or push the output unless Roy approves: pages pushed to main are public on GitHub Pages.
"""
import argparse, html, os, re, secrets, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--business', required=True, help='BUSINESS_NAME')
    p.add_argument('--city', required=True, help='CITY')
    p.add_argument('--trade', required=True, help='TRADE')
    p.add_argument('--first-name', required=True, help='CONTACT_FIRST_NAME')
    p.add_argument('--hours', required=True, help='HOURS (public hours, as published)')
    p.add_argument('--services', required=True, help='SERVICES, separated by ; or newlines')
    p.add_argument('--out-dir', default=HERE, help='where to write the page (default: demo/)')
    a = p.parse_args()

    e = lambda s: html.escape(s.strip(), quote=True)
    services = [x.strip() for x in re.split(r'[;\n]', a.services) if x.strip()]
    if not services:
        sys.exit('SERVICES is empty')
    src = open(os.path.join(HERE, 'lead-template.html'), encoding='utf-8').read()
    # Fill the SERVICES list item first: one <li> per service.
    li = '<li>{{SERVICES}}</li>'
    if src.count(li) != 1:
        sys.exit('template changed: expected exactly one SERVICES list item')
    src = src.replace(li, '\n              '.join('<li>%s</li>' % e(s) for s in services))
    for key, val in [('BUSINESS_NAME', a.business), ('CITY', a.city), ('TRADE', a.trade),
                     ('CONTACT_FIRST_NAME', a.first_name), ('HOURS', a.hours)]:
        src = src.replace('{{%s}}' % key, e(val))
    # Drop the instructions comment from the filled page (it contains the placeholder names).
    src = re.sub(r'<!--\s*LEAD DEMO TEMPLATE.*?-->\s*', '', src, count=1, flags=re.S)
    left = re.findall(r'\{\{[A-Z_]+\}\}', src)
    if left:
        sys.exit('Placeholders left: %s' % sorted(set(left)))
    slug = re.sub(r'[^a-z0-9]+', '-', a.business.lower()).strip('-')[:40] or 'lead'
    out = os.path.join(a.out_dir, '%s-%s.html' % (slug, secrets.token_hex(4)))
    open(out, 'w', encoding='utf-8').write(src)
    print(out)

if __name__ == '__main__':
    main()
