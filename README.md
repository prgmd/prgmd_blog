# AURORACAMP — Dev Blog

> 장준환(Jang Jun Hwan)의 기술 블로그. Vercel에서 운영 중인 정적 SPA.

---

## 개요

프레임워크 없이 순수 HTML + Vanilla JS로 구현한 단일 파일 블로그입니다.
마크다운 게시글을 `files/` 폴더에 쌓고, Python 빌드 스크립트로 `posts.json` 인덱스를 생성해 배포합니다.

---

## 기술 스택

| 역할 | 사용 기술 |
|---|---|
| 레이아웃 / 스타일 | Tailwind CSS (CDN) |
| 마크다운 렌더링 | marked.js |
| 코드 하이라이팅 | Prism.js (Okaidia 테마) |
| 수식 렌더링 | KaTeX |
| 폰트 | Pretendard, Material Symbols |
| 빌드 | Python 3 (`generate_posts.py`) |
| 호스팅 | Vercel (SPA rewrite) |

---

## 프로젝트 구조

```
prgmd_blog/
├── index.html              # SPA 진입점 (전체 UI + 라우팅 포함)
├── posts.json              # 게시글 메타데이터 인덱스 (빌드 산출물)
├── vercel.json             # Vercel SPA 리라이트 설정
├── package.json            # 빌드 스크립트 정의
├── generate_posts.py       # files/ 탐색 → posts.json 생성
└── files/                  # 마크다운 게시글 원본
```

---

## 빌드 및 배포

### posts.json 재생성

`files/` 내 마크다운 파일을 추가·수정한 뒤 실행합니다.

```bash
python3 generate_posts.py
# 또는
npm run build
```

### 로컬 미리보기

별도 서버 없이 `index.html`을 브라우저에서 직접 열거나, 간단한 HTTP 서버를 사용합니다.

```bash
python3 -m http.server 8000
```

### Vercel 배포

`main` 브랜치에 push하면 Vercel이 자동 배포합니다.
`vercel.json`의 rewrite 설정으로 모든 경로가 `index.html`로 라우팅됩니다.

---

## 게시글 작성 방법

`files/` 폴더에 마크다운 파일을 추가하고 상단에 프론트매터를 작성합니다.

```markdown
---
id: learning-aws-01
title: 클라우드 기초 및 EC2 인스턴스 활용
date: 2025-07-21
category: learning
subCategory: AWS
---

본문 내용...
```

| 필드 | 설명 |
|---|---|
| `id` | URL에 사용되는 고유 식별자 |
| `title` | 게시글 제목 |
| `date` | 작성일 (YYYY-MM-DD) |
| `category` | `projects` / `learning` / `algorithm` |
| `subCategory` | 단일 문자열 또는 배열 `["AWS", "Docker"]` |

작성 후 `python3 generate_posts.py`로 인덱스를 갱신합니다.

---

## 라우팅 구조

해시 기반 SPA 라우팅을 사용합니다.

| 경로 | 화면 |
|---|---|
| `#` (기본) | 소개 페이지 (About) |
| `#archive/projects` | Projects 카테고리 목록 |
| `#archive/learning` | Learning 카테고리 목록 |
| `#archive/algorithm` | Algorithm 카테고리 목록 |
| `#post/{id}` | 게시글 본문 |

---

## 카테고리 현황

### Projects
| 서브카테고리 | 게시글 수 |
|---|---|
| Blog | 3 |
| Digem | 1 |
| Blackbox | 1 |

### Learning
| 서브카테고리 | 게시글 수 |
|---|---|
| Python | 2 |
| Database | 6 |
| Linux | 9 |
| Network | 4 |
| Docker | 11 |
| Kubernetes | 9 |
| CI/CD | 9 |
| AWS | 11 |
| Ansible | 2 |
| Monitoring | 5 |
| Cloud | 4 |

---

## 주요 기능

- **다크 모드** 고정 (`#050505` 배경)
- **Explorer 패널** — VS Code 스타일의 사이드바 네비게이션
- **필터 버튼** — 카테고리 내 서브카테고리별 게시글 필터링
- **수식 지원** — `$...$` 인라인, `$$...$$` 블록 KaTeX 렌더링
- **코드 하이라이팅** — Prism.js Autoloader로 언어 자동 감지
- **모바일 반응형** — 768px 이하에서 Explorer 오버레이 전환

---

## 업데이트 내역

### 2026-03-17

**Decap CMS 온라인 에디터 추가**

Git push 없이 브라우저에서 직접 게시글을 작성·수정·삭제할 수 있도록 `/admin` 경로에 Decap CMS를 연동했습니다.

**추가된 파일**

| 파일 | 내용 |
|---|---|
| `admin/index.html` | Decap CMS CDN 로드 |
| `admin/config.yml` | CMS 설정 (레포, 브랜치, 필드 정의) |
| `api/auth.js` | GitHub OAuth 시작 — Vercel Serverless Function |
| `api/callback.js` | OAuth 콜백 — code → access_token 교환 후 CMS에 전달 |

**수정된 파일**

| 파일 | 내용 |
|---|---|
| `vercel.json` | `/admin` 경로를 SPA rewrite에서 제외 |

**삭제된 파일**

| 파일 | 이유 |
|---|---|
| `fix_frontmatter.py` | 일회성 마이그레이션 스크립트, 역할 완료 |
| `update_subcategories.py` | 일회성 마이그레이션 스크립트, 역할 완료 |

**동작 방식**

- `/admin` 접속 → GitHub OAuth 로그인 → Decap CMS 에디터 진입
- 게시글 저장(Publish) 시 GitHub API로 `files/*.md` 커밋 → Vercel 자동 재빌드 (~1분)
- 일반 방문자에게는 `/admin` 경로가 노출되지 않으며, GitHub 계정 인증 없이는 편집 불가
