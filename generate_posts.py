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
    for line in yaml_block.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            # 따옴표 및 공백 제거
            metadata[key.strip()] = value.strip().strip('"').strip("'")
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
