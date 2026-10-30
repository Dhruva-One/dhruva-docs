#!/usr/bin/env python3
"""
Import the DhruvaOne AI cards (cards.json) into GitHub as issues and add them to an
organisation Project (v2), setting Phase, Priority, Module, Source, Flag and Req ID.

Requires: Python 3.8+, GitHub CLI (`gh`) logged in with the `repo` and `project` scopes:
    gh auth login
    gh auth refresh -s project,repo

Typical use (run from this folder):
    python3 import_cards.py --dry-run                 # show what would happen, change nothing
    python3 import_cards.py --only AI-CHT-001         # try one card first
    python3 import_cards.py                           # import all 89 cards

Safe to re-run: created cards are remembered in .import-state.json and skipped.
Use --drafts to create draft items in the project instead of repository issues.
Screenshots: run ./publish_images.sh first so the image links in the cards resolve.
"""
import argparse, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, '.import-state.json')

FIELDS_SELECT = {  # field name -> (card key, options)
    'Phase': ('ph', ['MVP', 'P2', 'P3']),
    'Priority': ('pri', ['Must', 'Should', 'Could']),
    'Source': ('src', ['Design', 'Spec']),
}
LABEL_COLORS = {'area': '5319E7', 'phase': '1D76DB', 'priority': 'D93F0B', 'source': '0E8A16', 'module': 'C5DEF5', 'flag': 'FBCA04'}


def run(cmd, check=True, dry=False, quiet=False):
    if dry:
        print('  [dry-run] ' + ' '.join(cmd if len(' '.join(cmd)) < 200 else cmd[:6] + ['...']))
        return ''
    p = subprocess.run(cmd, capture_output=True, text=True)
    if check and p.returncode != 0:
        sys.exit('\nCommand failed: %s\n%s' % (' '.join(cmd[:8]), p.stderr.strip()))
    return p.stdout.strip()


def gh_json(cmd, dry=False):
    out = run(cmd, dry=dry)
    return json.loads(out) if out else {}


def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {}


def save_state(s):
    json.dump(s, open(STATE, 'w'), indent=1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--repo', default='Dhruva-One/dhruva-docs', help='repository for the issues (owner/name)')
    ap.add_argument('--owner', default='Dhruva-One', help='organisation that owns the project')
    ap.add_argument('--project', type=int, default=1, help='project number (the 1 in /projects/1)')
    ap.add_argument('--branch', default='main', help='branch holding the published images')
    ap.add_argument('--images-path', default='Funtional/Spec/cards/ai/images', help='folder in the repo holding the images')
    ap.add_argument('--cards', default=os.path.join(HERE, 'cards.json'))
    ap.add_argument('--only', help='comma-separated card IDs to import, for a trial')
    ap.add_argument('--drafts', action='store_true', help='create draft project items instead of repository issues')
    ap.add_argument('--no-images', action='store_true', help='leave screenshots out of the card text')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--delay', type=float, default=1.5, help='seconds between cards (avoids GitHub rate limits)')
    a = ap.parse_args()
    dry = a.dry_run

    if not dry:
        if subprocess.run(['gh', '--version'], capture_output=True).returncode != 0:
            sys.exit('GitHub CLI (gh) not found. Install from https://cli.github.com and run: gh auth login')
        st = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True)
        if st.returncode != 0:
            sys.exit('gh is not logged in. Run: gh auth login   then: gh auth refresh -s project,repo')

    cards = json.load(open(a.cards))
    all_mods = sorted(set(c['module'] for c in cards))
    if a.only:
        want = set(x.strip() for x in a.only.split(','))
        cards = [c for c in cards if c['id'] in want]
    print('%d card(s) to process%s' % (len(cards), ' (dry run)' if dry else ''))

    img_base = 'https://github.com/%s/blob/%s/%s' % (a.repo, a.branch, a.images_path)

    # --- project and fields
    if dry:
        pid = 'PVT_dry'; fields = {}
    else:
        pv = gh_json(['gh', 'project', 'view', str(a.project), '--owner', a.owner, '--format', 'json'])
        pid = pv['id']
        print('Project: %s (%s)' % (pv.get('title'), pid))

        def field_list():
            return {f['name']: f for f in gh_json(['gh', 'project', 'field-list', str(a.project), '--owner', a.owner, '--format', 'json', '--limit', '100'])['fields']}
        fields = field_list()
        created = False
        for name, (_, opts) in FIELDS_SELECT.items():
            if name not in fields:
                run(['gh', 'project', 'field-create', str(a.project), '--owner', a.owner, '--name', name, '--data-type', 'SINGLE_SELECT', '--single-select-options', ','.join(opts)]); created = True
        mods = all_mods
        if 'Module' not in fields:
            run(['gh', 'project', 'field-create', str(a.project), '--owner', a.owner, '--name', 'Module', '--data-type', 'SINGLE_SELECT', '--single-select-options', ','.join(mods)]); created = True
        for name in ('Req ID', 'Flag'):
            if name not in fields:
                run(['gh', 'project', 'field-create', str(a.project), '--owner', a.owner, '--name', name, '--data-type', 'TEXT']); created = True
        if created:
            fields = field_list()
        # single-select options that do not exist yet (e.g. a new module) cannot be added by the CLI
        mod_opts = {o['name'] for o in fields['Module'].get('options', [])} if 'Module' in fields else set()
        missing = [m for m in mods if mod_opts and m not in mod_opts]
        if missing:
            print('Note: the project field "Module" has no option for: %s. Add them in the project settings, or those cards will skip Module.' % ', '.join(missing))

    # --- labels (issues only)
    if not a.drafts:
        labs = sorted({l for c in cards for l in c['labels']})
        print('Ensuring %d labels in %s' % (len(labs), a.repo))
        for l in labs:
            kind = l.split(':')[0]
            run(['gh', 'label', 'create', l, '--repo', a.repo, '--color', LABEL_COLORS.get(kind, 'EDEDED'), '--description', 'DhruvaOne spec', '--force'], dry=dry, check=False)

    state = load_state()
    # what already exists on GitHub (so re-runs never create duplicates, even without the state file)
    existing = {}
    if not dry:
        if a.drafts:
            lst = gh_json(['gh', 'project', 'item-list', str(a.project), '--owner', a.owner, '--format', 'json', '--limit', '1000'])
            for it in (lst.get('items', []) if isinstance(lst, dict) else []):
                t = it.get('title') or (it.get('content') or {}).get('title') or ''
                existing[t.split(' \u00b7 ')[0]] = ''
        else:
            lst = gh_json(['gh', 'issue', 'list', '--repo', a.repo, '--state', 'all', '--limit', '1000', '--json', 'number,title,url'])
            for it in (lst if isinstance(lst, list) else []):
                existing[it['title'].split(' \u00b7 ')[0]] = it['url']
    done = failed = 0
    for c in cards:
        key = c['id']
        if key in state and not dry:
            print('skip  %s (already imported: %s)' % (key, state[key].get('url', '')))
            continue
        body = c['body'].replace('@@IMG@@', img_base)
        if a.no_images:
            body = '\n'.join(l for l in body.split('\n') if not l.startswith('![') and not (l.startswith('*') and l.endswith('*') and len(l) > 2))
        title = c['title']
        print('card  %s' % title)
        item_id = None
        url = ''
        if a.drafts and key in existing and not dry:
            print('  already in the project as a draft, skipping'); state[key] = {'url': '', 'item': 'existing'}; save_state(state); continue
        if a.drafts:
            out = gh_json(['gh', 'project', 'item-create', str(a.project), '--owner', a.owner, '--title', title, '--body', body, '--format', 'json'], dry=dry)
            item_id = out.get('id')
        else:
            bodyfile = os.path.join(HERE, '.tmp-body.md')
            if not dry and key not in existing:
                open(bodyfile, 'w').write(body)
            cmd = ['gh', 'issue', 'create', '--repo', a.repo, '--title', title, '--body-file', bodyfile]
            for l in c['labels']:
                cmd += ['--label', l]
            if key in existing and not dry:
                url = existing[key]; print('  issue already exists, making sure it is in the project: ' + url)
            else:
                url = run(cmd, dry=dry).splitlines()[-1] if not dry else ''
            out = gh_json(['gh', 'project', 'item-add', str(a.project), '--owner', a.owner, '--url', url, '--format', 'json'], dry=dry)
            item_id = out.get('id')
        if not dry and not item_id:
            print('  !! could not add to the project'); failed += 1; continue
        # set project fields
        if not dry:
            def setsel(name, value):
                f = fields.get(name)
                if not f: return
                opt = next((o for o in f.get('options', []) if o['name'] == value), None)
                if not opt:
                    return
                run(['gh', 'project', 'item-edit', '--id', item_id, '--project-id', pid, '--field-id', f['id'], '--single-select-option-id', opt['id']])
            def settext(name, value):
                f = fields.get(name)
                if f:
                    run(['gh', 'project', 'item-edit', '--id', item_id, '--project-id', pid, '--field-id', f['id'], '--text', value])
            for name, (k, _) in FIELDS_SELECT.items():
                setsel(name, c[k])
            setsel('Module', c['module'])
            settext('Req ID', c['id'])
            settext('Flag', c['flag'])
            state[key] = {'url': url, 'item': item_id}
            save_state(state)
            time.sleep(a.delay)
        done += 1
    if os.path.exists(os.path.join(HERE, '.tmp-body.md')):
        os.remove(os.path.join(HERE, '.tmp-body.md'))
    print('\nFinished: %d created%s, %d failed.' % (done, ' (dry run, nothing changed)' if dry else '', failed))


if __name__ == '__main__':
    main()
