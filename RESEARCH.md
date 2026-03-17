# 온라인 편집 전환 리서치

> 목표: Git push 없이 브라우저에서 직접 게시글 작성·수정·삭제 가능한 구조로 전환

---

## 현재 구조 이해

```
files/*.md (마크다운 + frontmatter)
    ↓  generate_posts.py
posts.json (메타데이터 인덱스)
    ↓  index.html의 fetch('./posts.json')
브라우저 → fetch('./files/{file}') → marked.js 렌더링
```

**핵심 제약**: Vercel 정적 호스팅은 파일시스템에 쓰기가 불가능하다.
어떤 방법을 택하든 **"쓰기 레이어"를 별도로 추가**해야 한다.

---

## 접근법 비교

### 방법 1. GitHub API 직접 호출

**원리**
브라우저에서 GitHub REST API(`PUT /repos/.../contents/files/*.md`)를 호출해 커밋.
커밋 감지 → Vercel 자동 재빌드 → `generate_posts.py` 실행 → 배포 완료.

**변경 범위**
- `index.html`에 에디터 UI (textarea, 저장 버튼) 추가
- GitHub PAT 또는 OAuth로 인증 처리
- 기존 파일 수정 시 현재 파일의 `sha` 먼저 조회 필요

**장점**
- 콘텐츠가 계속 Git에 남음 (버전 관리 유지)
- `.md` + frontmatter 형식 100% 유지
- 추가 비용 없음, 인프라 변경 없음

**단점**
- 저장 후 Vercel 빌드 완료까지 30초~2분 대기
- PAT를 브라우저에서 사용하면 보안 주의 필요

**난이도**: 중 / **비용**: 무료

---

### 방법 2. Vercel Serverless Functions + Vercel Blob

**원리**
`api/` 디렉토리에 Serverless Function으로 CRUD API 구성.
마크다운 파일을 Vercel Blob(오브젝트 스토리지)에 저장.
포스트 인덱스는 Blob의 `posts.json`으로 실시간 갱신.

**변경 범위**
- `api/posts.js` 신규 작성 (GET/POST/PUT/DELETE)
- `index.html`의 `fetch('./posts.json')` → `fetch('/api/posts')` 교체
- 기존 80개 `.md` 파일 → Blob으로 마이그레이션
- `generate_posts.py` 불필요해짐

**장점**
- 저장 즉시 반영 (재빌드 없음)
- Vercel 생태계 내에서 해결

**단점**
- 콘텐츠가 Blob에 종속 → Git에서 `.md` 파일 사라짐, 버전 관리 불가
- 구현 범위가 전방위적 (API + 인증 + 스토리지 + 프론트 데이터레이어 교체)

**난이도**: 상 / **비용**: Blob 500MB 이하 무료

---

### 방법 3. Supabase 백엔드

**원리**
PostgreSQL 테이블에 포스트 저장 (`id`, `title`, `date`, `category`, `subCategory`, `content`).
Supabase JS SDK를 `index.html`에서 직접 호출해 CRUD.
Row Level Security(RLS)로 인증 처리.

**변경 범위**
- 80개 `.md` → PostgreSQL 마이그레이션 (일회성)
- `index.html` 데이터 로딩 로직 전면 교체
- `.md` + frontmatter 형식 포기 → DB 컬럼으로 대체

**장점**
- 저장 즉시 반영
- Auth 구현이 상대적으로 쉬움
- Supabase Dashboard에서 직접 데이터 수정 가능

**단점**
- 마크다운 파일 기반 구조 완전 포기
- 외부 서비스 의존 — 장애 시 블로그 전체 영향
- 무료 티어: 2주 비활성 시 프로젝트 자동 pause

**난이도**: 중~상 / **비용**: 무료 (단, pause 주의)

---

### 방법 4. Decap CMS (구 Netlify CMS)

**원리**
Git 기반 헤드리스 CMS. 내부적으로 방법 1(GitHub API)의 완성형 솔루션.
`admin/index.html` + `admin/config.yml` 추가만으로 `/admin` 경로에 에디터 UI가 생긴다.
GitHub OAuth로 인증 후 저장 시 GitHub API를 통해 자동 커밋 → Vercel 재빌드.

**변경 범위**
- `admin/index.html`, `admin/config.yml` 파일 2개 추가
- GitHub OAuth App 등록 (GitHub Settings에서 5분 작업)
- `vercel.json`에 `/admin` 경로 처리 추가 (현재 rewrite 규칙 충돌 방지)
- 기존 `.md` + frontmatter 형식 그대로 유지

**config.yml 핵심 구조 예시**
```yaml
backend:
  name: github
  repo: prgmd/prgmd_blog
  branch: main

media_folder: files
public_folder: /files

collections:
  - name: posts
    label: Posts
    folder: files
    create: true
    fields:
      - { name: id, label: ID }
      - { name: title, label: Title }
      - { name: date, label: Date, widget: datetime }
      - { name: category, label: Category, widget: select, options: [projects, learning, algorithm] }
      - { name: subCategory, label: SubCategory }
      - { name: body, label: Body, widget: markdown }
```

**장점**
- 현재 아키텍처 변경 최소화 — 파일 2개 추가가 전부
- `.md` + frontmatter + Git 기반 구조 100% 유지
- 완성된 마크다운 에디터 UI 제공
- 오픈소스, 완전 무료

**단점**
- 저장 후 Vercel 빌드 대기 (30초~2분) — 즉시 반영 아님
- 마지막 주요 릴리스가 2023년으로 유지보수 수준에 머묾
- 기본 UI가 현재 블로그 디자인 테마와 이질적

**난이도**: 하 / **비용**: 무료

---

### 방법 5. Cloudflare Workers + R2

**원리**
Vercel에서 Cloudflare로 이전. Workers(서버리스)에서 API 처리, R2(오브젝트 스토리지)에 `.md` 저장.

**장점**: 무료 티어가 넉넉하고 응답 속도 우수
**단점**: Vercel 환경 포기, 가장 큰 아키텍처 변경, 학습 곡선

**난이도**: 상 / **비용**: 무료

---

## 비교 요약

| 항목 | GitHub API | Vercel Blob | Supabase | **Decap CMS** | Cloudflare |
|---|:---:|:---:|:---:|:---:|:---:|
| 구현 난이도 | 중 | 상 | 중~상 | **하** | 상 |
| .md 형식 유지 | O | O | X | **O** | O |
| 즉시 반영 | X | O | O | X | O |
| Vercel 유지 | O | O | O | **O** | X |
| Git 버전 관리 | O | X | X | **O** | X |
| 아키텍처 변경 범위 | 소 | 대 | 대 | **최소** | 최대 |
| 비용 | 무료 | 무료 | 무료 | **무료** | 무료 |

---

## 결론 및 추천

### 1순위 — Decap CMS

현재 구조를 가장 적게 건드리면서 요구사항을 충족한다.
`admin/` 파일 2개 추가 + GitHub OAuth App 등록으로 완성.
기존 `.md` + frontmatter + `generate_posts.py` + Vercel 배포 파이프라인이 전부 유지된다.

개인 블로그 특성상 "저장 후 1~2분 대기"는 실용적으로 큰 문제가 아니다.

### 2순위 — GitHub API 직접 구현

Decap CMS의 기본 UI(밝은 테마, 외부 디자인)가 현재 블로그 철학과 맞지 않거나,
에디터를 `index.html` 내에 완전히 통합하고 싶은 경우.
인증은 PAT를 `sessionStorage`에 임시 저장하는 방식으로 단순화 가능.
(개인만 사용하는 블로그 수준에서 수용 가능한 보안 트레이드오프)

### 즉시 반영이 반드시 필요한 경우만

Vercel Blob(방법 2) 또는 Supabase(방법 3)를 고려.
단, 이 경우 Git 버전 관리와 `.md` 파일 기반 구조를 포기해야 한다.

---

## 다음 단계 (Decap CMS 기준)

1. GitHub에서 OAuth App 등록 (`Settings > Developer settings > OAuth Apps`)
2. `admin/index.html` 생성 (Decap CMS CDN 로드)
3. `admin/config.yml` 생성 (frontmatter 필드 정의)
4. `vercel.json` rewrite 규칙에서 `/admin` 경로 제외
5. Vercel 환경변수에 OAuth Client ID 등록
6. 배포 후 `/admin` 접속 테스트
