import os
import json
import re

def parse_frontmatter(content):
    """마크다운 상단의 --- 영역을 파싱합니다."""
    match = re.search(r'^---\s*(.*?)\s*---', content, re.DOTALL | re.MULTILINE)
    if not match:
        return None

    yaml_block = match.group(1)
    metadata = {}
    current_list_key = None

    for line in yaml_block.split('\n'):
        stripped = line.strip()

        # YAML 블록 리스트 항목 수집 (Decap CMS list 위젯 저장 형식)
        if current_list_key is not None:
            if stripped.startswith('- '):
                item = stripped[2:].strip().strip('"').strip("'")
                metadata[current_list_key].append(item)
                continue
            # 리스트 항목이 아닌 줄이 나오면 리스트 종료
            if not metadata[current_list_key]:
                metadata[current_list_key] = ''
            current_list_key = None

        if ':' not in line:
            continue

        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()

        # 값이 없으면 블록 리스트 시작 가능성
        if not value:
            current_list_key = key
            metadata[key] = []
            continue

        # 인라인 배열 형식 처리: ["A", "B"] or ['A', 'B']
        if value.startswith('['):
            try:
                parsed = json.loads(value)
                metadata[key] = parsed
                continue
            except json.JSONDecodeError:
                pass

        # 불리언 처리
        if value.lower() == 'true':
            metadata[key] = True
            continue
        if value.lower() == 'false':
            metadata[key] = False
            continue

        # 일반 문자열
        metadata[key] = value.strip('"').strip("'")

    # 마지막 키가 빈 블록 리스트인 경우 처리
    if current_list_key is not None and not metadata[current_list_key]:
        metadata[current_list_key] = ''

    return metadata

def build_posts_json():
    posts = []
    files_dir = './files'
    
    if not os.path.exists(files_dir):
        print("오류: 'files' 폴더를 찾을 수 없습니다.")
        return

    for dirpath, _, filenames in os.walk(files_dir):
        for filename in sorted(filenames, reverse=True):
            if filename.endswith('.md'):
                full_path = os.path.join(dirpath, filename)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    metadata = parse_frontmatter(content)
                    if metadata:
                        # 'files' 디렉토리를 기준으로 한 상대 경로를 저장
                        relative_path = os.path.relpath(full_path, files_dir)
                        metadata['file'] = relative_path.replace(os.path.sep, '/') # 일관성을 위해 경로 구분자를 /로 변경
                        
                        # ID가 없으면 파일 경로 기반으로 생성 (예: 'folder/file.md' -> 'folder-file')
                        if 'id' not in metadata:
                            metadata['id'] = relative_path.replace('.md', '').replace(os.path.sep, '-')
                        posts.append(metadata)
    
    # 날짜 기준 최신순 정렬
    posts.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)
    print(f"성공: {len(posts)}개의 게시글이 posts.json에 등록되었습니다.")

if __name__ == "__main__":
    build_posts_json()
