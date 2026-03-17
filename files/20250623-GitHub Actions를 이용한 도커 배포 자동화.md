---
id: 20250623-GitHub Actions를 이용한 도커 배포 자동화
title: "GitHub Actions를 이용한 도커 배포 자동화"
date: "2025-06-23"
category: "learning"
subCategory: ["Docker", "CI/CD", "GitHub Actions"]
---

## 1. Go 애플리케이션 작성 및 이미지 빌드
자동화 배포를 위한 대상 애플리케이션을 준비하고 도커파일을 작성한다.

### 1) Go 소스 코드 작성 (main.go)
* 표준 출력으로 "GO GO GO"를 출력하는 간단한 Go 프로그램을 작성하고 `go run` 명령으로 실행을 확인한다.

### 2) 멀티 스테이지 Dockerfile 구성
* **빌드 단계**: `golang:1.15-alpine3.12` 이미지를 사용하여 소스 코드를 컴파일하고 실행 파일을 생성한다.
* **실행 단계**: `scratch` 이미지를 사용하여 빌드 결과물만 포함한 초경량 이미지를 구성한다.

## 2. GitHub Actions 주요 개념
GitHub에서 제공하는 CI/CD 도구로, 소프트웨어 워크플로우를 자동화한다.

* **Workflow**: 하나 이상의 Job으로 구성되며, 이벤트(push, pull request 등)에 의해 트리거되는 자동화 프로세스이다. `.github/workflows` 디렉토리에 YAML 파일로 정의한다.
* **Event**: 워크플로우를 실행하는 특정 활동이다.
* **Job**: 동일한 Runner에서 실행되는 일련의 Step 집합이다.
* **Step**: 커맨드를 실행하거나 Action을 호출하는 개별 태스크이다.
* **Action**: 복잡하고 자주 반복되는 작업을 수행하기 위한 독립적인 커맨드로, 재사용이 가능하다.
* **Runner**: 워크플로우가 실행될 서버 인스턴스(예: ubuntu-latest)이다.

## 3. 도커 허브(Docker Hub) 사전 준비
GitHub Actions가 도커 허브에 접근하여 이미지를 업로드할 수 있도록 인증 정보를 설정해야 한다.

* **레포지토리 생성**: 이미지가 저장될 공간인 `actiontest` 레포지토리를 생성한다.
* **Access Token 발급**: 보안을 위해 계정 비밀번호 대신 사용할 액세스 토큰을 발급받는다.
* **GitHub Secrets 설정**: 발급받은 토큰과 사용자 이름을 GitHub 레포지토리의 `Settings > Secrets`에 등록하여 보안을 유지한다.

## 4. 워크플로우(Workflow) 파일 작성 및 적용
`.github/workflows/actiontest.yml` 파일을 작성하여 자동화 흐름을 정의한다.

### 1) 워크플로우 트리거 설정
* `main` 브랜치에 코드가 `push`될 때마다 워크플로우가 실행되도록 설정한다.

### 2) 주요 작업 단계(Steps)
1. **코드 체크아웃**: `actions/checkout@v3`를 사용하여 Runner로 소스 코드를 가져온다.
2. **Go 환경 설정**: 빌드에 필요한 Go 버전을 설정한다.
3. **도커 허브 로그인**: GitHub Secrets에 저장된 정보를 불러와 `docker/login-action`으로 인증을 수행한다.
4. **이미지 빌드 및 푸시**: Dockerfile을 실행하여 이미지를 생성하고, 지정된 태그(예: latest)를 붙여 도커 허브로 전송한다.

## 5. 결과 확인
* 로컬에서 수정된 코드를 GitHub에 `git push` 하면 자동으로 워크플로우가 동작한다.
* GitHub의 **Actions** 탭에서 진행 상황을 확인하고, 완료 후 도커 허브 레포지토리에 새로운 이미지가 업로드되었는지 검토한다.