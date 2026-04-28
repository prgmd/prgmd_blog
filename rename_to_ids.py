import os
import re

def get_id(content):
    match = re.search(r'^---\s*(.*?)\s*---', content, re.DOTALL | re.MULTILINE)
    if not match:
        return None
    for line in match.group(1).split('\n'):
        if line.startswith('id:'):
            return line.split(':', 1)[1].strip().strip('"').strip("'")
    return None

def rename_files():
    files_dir = './files'
    renamed = []
    skipped = []
    errors = []

    for filename in sorted(os.listdir(files_dir)):
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(files_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        post_id = get_id(content)
        if not post_id:
            skipped.append(f'  [NO ID]  {filename}')
            continue

        expected_name = post_id + '.md'
        if filename == expected_name:
            skipped.append(f'  [OK]     {filename}')
            continue

        new_path = os.path.join(files_dir, expected_name)
        if os.path.exists(new_path):
            errors.append(f'  [CONFLICT] {filename} → {expected_name} (already exists)')
            continue

        os.rename(filepath, new_path)
        renamed.append(f'  {filename}\n    → {expected_name}')

    print(f'\n=== rename_to_ids.py 결과 ===\n')
    print(f'[변경됨] {len(renamed)}개')
    for r in renamed:
        print(r)
    print(f'\n[건너뜀] {len(skipped)}개 (이미 일치하거나 id 없음)')
    for s in skipped:
        print(s)
    if errors:
        print(f'\n[오류] {len(errors)}개')
        for e in errors:
            print(e)
    print(f'\n완료. posts.json 재생성: python3 generate_posts.py')

if __name__ == '__main__':
    rename_files()
