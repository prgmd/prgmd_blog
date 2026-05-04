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
├── assets/                 # 정적 에셋 (이미지, SVG 등)
├── admin/                  # Decap CMS 온라인 에디터
│   ├── index.html          # Decap CMS CDN 로드
│   └── config.yml          # CMS 설정 (레포, 브랜치, 필드 정의)
├── api/                    # Vercel Serverless Functions
│   ├── auth.js             # GitHub OAuth 시작
│   └── callback.js         # OAuth 콜백 — code → access_token 교환
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

---

**Contributions 그래프 추가**

소개 페이지 하단에 GitHub 잔디 스타일의 게시글 작성 현황 그래프를 추가했습니다.

- 최근 52주(1년) 기간의 게시글 작성 날짜를 격자로 시각화
- 색상: 0개(회색) → 1개 → 2개 → 3개+(파랑, 블로그 primary 색상)
- hover 시 날짜 및 게시글 수 tooltip 표시
- 가로 스크롤바 커스텀 스타일 적용 (4px, 다크 테마)
- 날짜 형식 불일치 자동 정규화 처리 (`2026-1-23` → `2026-01-23`)

---

**게시글 숨김 기능 추가**

frontmatter에 `hidden: true`를 추가하면 목록에서 노출되지 않습니다.

```yaml
---
id: example-post
title: 제목
date: 2026-03-17
category: learning
subCategory: AWS
hidden: true
---
```

- 기본값: 노출 (`hidden` 미설정 또는 `hidden: false`)
- 숨김 설정 시 카테고리 목록, 서브카테고리 목록에서 제외
- 직접 URL(`#post/{id}`) 접근은 가능
- `generate_posts.py`에 불리언 파싱 추가 (`true`/`false` 문자열 → Python bool)

---

### 2026-04-03

**게시글 본문 디자인 개선**

`.prose` 스타일 전반을 개선했습니다.

| 대상 | 변경 내용 |
|---|---|
| `h1` | border-b 제거 → `bg-zinc-800/60` 배경 + 라운드 처리 |
| `h2` | `border-b border-white/20` 하단 구분선 유지 |
| `h3` | 좌측 border 제거, `text-zinc-200` 색상으로만 계층 표현 |
| `h4` | `text-zinc-300` |
| `strong` | `text-white` → `text-amber-200` (강조 색상) |
| `blockquote` | 좌측 선만 → 배경색 + 좌측 바 + 우측 라운드 조합 |
| `blockquote` 내 `p` | 하단 마진 제거 (공백 이중 삽입 방지) |
| `blockquote` 내 `strong` | not-italic 명시 + `text-amber-200` 적용 |
| `pre` (코드블럭) | `bg-[#121212]` → `bg-[#1a1a1a]` + `border-zinc-600` (가시성 개선) |
| 수식 플레이스홀더 | `<MATHBLOCK>` 형식 → `AURORA_BLOCK_N_MATHEND` 형식으로 변경 (marked의 HTML escape 방지, `$$` 블록 수식 미적용 버그 수정) |
| blockquote 내 bold 미렌더링 | `marked.parse()` 전 `> ` 라인 대상으로 `**...**` → `<strong>` 직접 치환 처리 추가 |

---

### 2026-04-03 (2)

**게시글 본문 디자인 추가 조정**

| 대상 | 변경 내용 |
|---|---|
| `h1` | 배경색 제거, `3xl/4xl`로 사이즈 확대 |
| `h2` | `2xl/3xl`로 사이즈 확대 |
| `h3` | `xl/2xl`로 사이즈 확대 |
| `h4` | `lg/xl`로 사이즈 확대 |
| `blockquote` | 배경 `bg-amber-950/30`, border `border-amber-700/50`, 텍스트 `text-amber-200/70` (따뜻한 노트 톤) |
| `blockquote strong` | `not-italic` 제거 — 인용구 내 볼드도 이탤릭 유지 |

---

**Decap CMS 서브카테고리 복수 저장 버그 수정**

`admin/config.yml`의 `subCategory` 위젯을 `string` → `list`로 변경했습니다.
기존 단일 문자열 게시글은 `index.html`의 `Array.isArray()` 분기로 호환성 유지.

---

### 2026-05-04

**마크다운 중첩 목록 들여쓰기 정렬 버그 수정**

`.prose ul / ol`에 적용된 `list-inside`로 인해 중첩 목록과 줄바꿈 텍스트의 들여쓰기가 어긋나는 문제를 수정했습니다.

| 대상 | 변경 전 | 변경 후 |
|---|---|---|
| `.prose ul` | `list-disc list-inside ml-4 mb-6 space-y-2` | `list-disc list-outside pl-6 mb-6 space-y-2` |
| `.prose ol` | `list-decimal list-inside ml-4 mb-6 space-y-2` | `list-decimal list-outside pl-6 mb-6 space-y-2` |
| `.prose ul ul`, `.prose ol ul` | (없음) | `mt-2 mb-0 pl-6` |
| `.prose ul ol`, `.prose ol ol` | (없음) | `mt-2 mb-0 pl-6` |
| `.prose li` | `text-zinc-300` | `text-zinc-300 pl-1` |

**원인**

`list-inside`는 불릿 마커를 텍스트 흐름 안에 배치하므로, 항목 텍스트가 줄바꿈될 때 두 번째 줄이 불릿 아래가 아닌 좌측 끝으로 붙는 hanging indent 미처리 문제가 발생합니다. 중첩 목록에서 특히 두드러집니다.

**해결**

`list-outside` + `pl-6`으로 변경해 불릿이 padding 영역에 걸리도록 하고, 줄바꿈 시 텍스트 시작점이 항상 일정하게 유지되도록 했습니다. 중첩 목록에는 별도 `pl-6`을 부여해 단계별 들여쓰기가 명확히 구분됩니다.

---

### 2026-04-28

**Decap CMS 제목 변경 오류 수정 및 다중 태그 파싱 수정**

**추가된 파일**

| 파일 | 내용 |
|---|---|
| `rename_to_ids.py` | `files/` 내 파일명을 각 게시글의 `id` 필드값으로 일괄 rename하는 일회성 마이그레이션 스크립트 |

**수정된 파일**

| 파일 | 내용 |
|---|---|
| `generate_posts.py` | YAML 블록 리스트 형식(`- item`) 파싱 지원 추가 |

**버그 1 — Decap CMS 제목 변경 시 오류**

`admin/config.yml`의 `slug: "{{fields.id}}"` 설정으로 인해 Decap CMS는 저장 시 파일명이 `id` 필드값과 일치해야 한다고 간주합니다. 기존 파일 대부분이 한국어 제목으로 생성되어 `id` 값과 불일치한 상태였기 때문에, 저장할 때마다 파일 rename을 시도하고 GitHub API 오류가 발생했습니다.

`rename_to_ids.py`를 1회 실행해 모든 파일명을 `{id}.md` 형식으로 정렬하면 해소됩니다.

```bash
python3 rename_to_ids.py
python3 generate_posts.py
```

**버그 2 — 다중 서브카테고리 저장 후 인덱스 누락**

Decap CMS `list` 위젯은 다중 항목을 YAML 블록 리스트 형식으로 저장합니다.

```yaml
subCategory:
  - Docker
  - Kubernetes
```

기존 `generate_posts.py`의 파서는 `key: value` 한 줄 형식만 처리해 블록 리스트 항목(`- item`)을 무시했고, `subCategory`가 빈 값으로 `posts.json`에 기록되었습니다. 파서를 수정해 블록 리스트 수집 모드를 추가했으며, 기존 인라인 배열(`["A", "B"]`) 형식도 그대로 지원합니다.
