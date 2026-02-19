import os
import re

files_dir = os.path.join(os.path.dirname(__file__), 'files')

# subCategory casing map
casing_map = {
    'linux': 'Linux',
    'docker': 'Docker',
    'kubernetes': 'Kubernetes',
    'database': 'Database',
    'ci/cd': 'CI/CD',
    'monitoring': 'Monitoring',
    'network': 'Network',
    'cloud': 'Cloud',
    'blog': 'Blog',
    'python': 'Python',
    'digem': 'Digem',
    'blackbox': 'Blackbox',
    'ansible': 'Ansible',
    'aws': 'AWS',
}

updated = 0
skipped = 0

for fname in sorted(os.listdir(files_dir)):
    if not fname.endswith('.md'):
        continue
    fpath = os.path.join(files_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content

    # Remove excerpt line (entire line including newline)
    new_content = re.sub(r'^excerpt:.*\n?', '', new_content, flags=re.MULTILINE)

    # Fix subCategory casing
    def fix_sub(m):
        key = m.group(1)
        val = m.group(2).strip().strip('"').strip("'")
        fixed = casing_map.get(val, val)
        return f'subCategory: "{fixed}"'

    new_content = re.sub(
        r'subCategory:\s*["\']?([^"\'\n]*)["\']?',
        lambda m: 'subCategory: "' + casing_map.get(m.group(1).strip().strip('"').strip("'"), m.group(1).strip().strip('"').strip("'")) + '"',
        new_content
    )

    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated: {fname}')
        updated += 1
    else:
        skipped += 1

print(f'\nDone: {updated} updated, {skipped} unchanged.')
