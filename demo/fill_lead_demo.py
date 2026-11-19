#!/usr/bin/env python3
"""Fill demo/lead-template.html for ONE lead. Static fill, stdlib only. Sends nothing, calls no API.

Example (fictional business):
  python3 demo/fill_lead_demo.py --business "Sample Plumbing Co." --city "Fort Lauderdale" --trade "Plumbing" \
      --first-name "Sam" --hours "Mon-Fri 8 AM-5 PM" --services "Leak repair; Drain cleaning; Water heaters"

Output: demo/p/<token>/index.html. The token is random (160 bits, lowercase a-z and 2-7) and never contains the
business name or any lead info. The script prints the relative URL (demo/p/<token>/).
A local log maps token -> lead. It is kept OUT of the repo (default /workspace/business/sales/lead-demo-tokens.csv,
or --log PATH) and .gitignore blocks lead-demo-tokens files and any CSV under demo/.

Every value is HTML-escaped. SERVICES is split on ';' or newlines, one list item each.
The script refuses to write a page if any {{PLACEHOLDER}} is left, and refuses to overwrite an existing token
directory unless --force. Use --token <existing> --force to regenerate a known page.
Do NOT commit or push the output unless Roy has approved that link: pages pushed to main are public.
"""
import argparse, base64, csv, datetime, html, os, re, secrets, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LOG = '/workspace/business/sales/lead-demo-tokens.csv'
TOKEN_RE = re.compile(r'^[a-z2-7]{26,64}$')  # lowercase base32 alphabet, at least 130 bits

def new_token():
    # 20 random bytes = 160 bits, base32 lower-case, no padding (32 chars). Nothing derived from lead data.
    return base64.b32encode(secrets.token_bytes(20)).decode('ascii').lower().rstrip('=')

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--business', required=True, help='BUSINESS_NAME')
    p.add_argument('--city', required=True, help='CITY')
    p.add_argument('--trade', required=True, help='TRADE')
    p.add_argument('--first-name', required=True, help='CONTACT_FIRST_NAME')
    p.add_argument('--hours', required=True, help='HOURS (public hours, as published)')
    p.add_argument('--services', required=True, help='SERVICES, separated by ; or newlines')
    p.add_argument('--token', help='reuse a known token (lowercase a-z2-7, 26+ chars) to regenerate that page; needs --force if it exists')
    p.add_argument('--force', action='store_true', help='overwrite an existing token directory')
    p.add_argument('--log', default=DEFAULT_LOG, help='token -> lead log, kept outside the repo (default: %s)' % DEFAULT_LOG)
    p.add_argument('--out-dir', default=HERE, help='demo directory to write under (default: this demo/ folder); pages go to <out-dir>/p/<token>/index.html')
    a = p.parse_args()

    # The log must never live inside the repo.
    repo = os.path.dirname(HERE)
    log = os.path.abspath(a.log)
    if os.path.commonpath([log, repo]) == repo:
        sys.exit('--log must be outside the repo (%s)' % repo)

    token = a.token if a.token else new_token()
    if not TOKEN_RE.match(token):
        sys.exit('token must be 26-64 characters of lowercase a-z and 2-7')
    slug = re.sub(r'[^a-z0-9]+', '', a.business.lower())
    if len(slug) >= 4 and slug in token:
        sys.exit('token must not contain the business name')
    out_dir = os.path.join(a.out_dir, 'p', token)
    existed = os.path.exists(out_dir)
    if existed and not a.force:
        sys.exit('%s already exists. Use --force to overwrite it.' % out_dir)

    e = lambda s: html.escape(s.strip(), quote=True)
    services = [x.strip() for x in re.split(r'[;\n]', a.services) if x.strip()]
    if not services:
        sys.exit('SERVICES is empty')
    src = open(os.path.join(HERE, 'lead-template.html'), encoding='utf-8').read()
    li = '<li>{{SERVICES}}</li>'
    if src.count(li) != 1:
        sys.exit('template changed: expected exactly one SERVICES list item')
    src = src.replace(li, '\n              '.join('<li>%s</li>' % e(s) for s in services))
    for key, val in [('BUSINESS_NAME', a.business), ('CITY', a.city), ('TRADE', a.trade),
                     ('CONTACT_FIRST_NAME', a.first_name), ('HOURS', a.hours)]:
        src = src.replace('{{%s}}' % key, e(val))
    # The page sits at demo/p/<token>/index.html, three levels below the site root: fix the relative links.
    src, n = re.subn(r'(href|src)="\.\./', r'\1="../../../', src)
    if n == 0:
        sys.exit('template changed: no relative links found to rewrite')
    # Drop the instructions comment from the filled page (it contains the placeholder names).
    src = re.sub(r'<!--\s*LEAD DEMO TEMPLATE.*?-->\s*', '', src, count=1, flags=re.S)
    left = re.findall(r'\{\{[A-Z_]+\}\}', src)
    if left:
        sys.exit('Placeholders left: %s' % sorted(set(left)))

    if existed:
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    out = os.path.join(out_dir, 'index.html')
    open(out, 'w', encoding='utf-8').write(src)

    # Local mapping log, outside the repo.
    os.makedirs(os.path.dirname(log), exist_ok=True)
    new_file = not os.path.exists(log)
    with open(log, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(['created_at', 'action', 'token', 'relative_url', 'business', 'city', 'trade', 'contact_first_name', 'approved_by_roy', 'shared'])
        w.writerow([datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'overwritten' if existed else 'created',
                    token, 'demo/p/%s/' % token, a.business, a.city, a.trade, a.first_name, 'no', 'no'])
    print('demo/p/%s/' % token)
    print('file: %s' % out, file=sys.stderr)
    print('log:  %s' % log, file=sys.stderr)

if __name__ == '__main__':
    main()
