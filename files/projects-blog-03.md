---
id: blog-dev-003
title: "길고도 험난했던 Dev 블로그 제작기: (3) 게시글 실행 오류에 직면하다"
date: "2026-1-23"
category: "projects"
subCategory: "blog"
excerpt: "vercel.json 빌드 구조 바꾸기"
tags: ["Obsidian", "Cloudflare", "DevOps", "DigitalGarden"]
---

## 1. 게시글 실행 오류

만들자마자 뭔가 좀 이상했다. Blog 카테고리에 저장되어 있는 글을 누르면 잘 열리기는 한데, 무조건 최신 글로 강제 이동되는 현상이 있던 것. 예를 들어, projects-blod-01.md이 게시글 목록에 올라와있지만 해당 글을 읽으려고 하면 projects-blod-02.md가 켜지는 식이었다. 

대체 뭐가 문제일까 코드를 찾아보니, generator_posts.py이 posts.json 파일에 자동 업데이트를 못하는 것을 확인했다. 처음에 AI로 가이드를 잡을 때 수동 관리는 죽어도 싫었기 때문에 일부러 게시글을 모아두는 files를 읽고 이들을 모두 posts.json에 자동 등록하는 로직을 작성해뒀는데, 정작 versel.json 파일이 배포시 이걸 실행하지 않지 않아 연동이 안 되고 있던 것이었다. 그래서 아마도 index.html이 무조건 가장 최신 글을 호출하는 것으로 보였다.
  
하지만 로직을 개선하던 도중 충격적인 사실을 발견했다. 나중에 보니 내가 id를 똑같이 설정해뒀더라... 물론 내가 id를 잘못 중복한 탓에 벌어진 현상이었지만, 이참에 id 기준이 아닌 폴더-파일명 기준으로 중복되지 않는 고유 id를 찍기로 로직을 변경했다. 
  
나중에는 포매터 상 id도 뺄 예정이고, 제목-일자-카테고리-서브카테고리-소주제-파일 정도로만 운영할 예정이다. id는 글 제목으로 대체할 예정인데 그래도 괜찮으려나? 원래 데이터 구조 짤때는 무조건 id를 넣는게 중요하다고 배웠는데, 차라리 숫자 시퀀스를 자동 등록되게 만드는 게 좋아보인다. 태그는 크게 필요없을듯. 블로그 상으로 태크 검색 기능은 제외할 예정이라 (내가 잘 안 쓴다. 애초에 폴더 구조를 미리 만들어 두기도 했고)
  
빌드 설정 추가해서 파이썬 스크립트가 먼저 실행된 다음 배포되도록 vercel.json을 수정했다. 

``` json
{
  "version": 2,
  "builds": [
    {
      "use": "@vercel/static-build",
      "config": {
        "distDir": ".",
        "buildCommand": "python3 generate_posts.py"
      }
    }
  ],
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}

```

> `"public": true`는 Vercel에게 '이 프로젝트는 빌드 과정이 없는 순수 정적
  파일들로만 이루어져 있으니, 폴더 안의 모든 파일을 그대로 웹사이트에 복사해서
  보여줘'라는 의미. 이걸 사용하면 로컬 상태 그대로 바로 배포가 가능하지만, 지금은 `generate_posts.py`를 실행해야 하므로 정적 사이트로 먼저 선언해준 다음 `index.html`을 읽어줘라고 직접 지시를 해줘야 한다.
  
generator_posts.py도 로직을 일부 수정.
  
``` python
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
      
```
  
![](https://velog.velcdn.com/images/paramad/post/dd1e7be6-3bd7-4e45-b7bd-24d78c89860d/image.png)
  
잘 읽어오는 것 확인. 이제 Vercel에 배포해서도 잘 되는지 확인해 봐야 했다. 그리고...
  
![](https://velog.velcdn.com/images/paramad/post/490086ba-a780-45fa-a4af-a5545af4746e/image.png)
  
`assets/image.png`와 같은 정적 파일을 Vercel이 빌드 대상으로 잘못 인식하여 오류를 발생시켰다. 차라리 그래서 복잡한 `vercel.json` 설정으로 Vercel 내부 동작 충돌을 야기하기 보다, Vercel이 가장 안정적으로 지원하는 표준 방식인 `package.json` 방식을 선택. `scripts` 안에 `"build": "python3 generate_posts.py"` 스크립트를 정의하고 `vercel.json`은 SPA 라우팅을 위한 rewrites 규칙만 남겼다. 이후 값을 override하는 Vercel 세팅을 초기화. 이후 잘 뜨는 걸 확인할 수 있었다.
