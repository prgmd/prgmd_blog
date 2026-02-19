---
id: learning-cicd-03
title: "GitHub Actions 심화 및 프로젝트 실습"
date: "2025-07-17"
category: "learning"
subCategory: ["CI/CD", "GitHub Actions"]
---

## 1. CI/CD와 GitHub Actions 개요
소프트웨어 개발의 전 과정(개발, 테스트, 빌드, 반영, 배포)을 자동화하는 것을 CI/CD라고 한다.

* **CI (Continuous Integration)**: 코드 변경 사항을 정기적으로 빌드하고 테스트하여 공유 레포지토리에 통합하는 과정이다. 주요 도구로 Circle CI, Bamboo 등이 있다.
* **CD (Continuous Deployment/Delivery)**: CI를 통과한 코드를 실제 운영 환경에 자동으로 배포하는 과정이다. 주요 도구로 GitHub Action, GitLab CI/CD, Jenkins, Argo CD 등이 활용된다.
* **GitHub Actions의 특징**: GitHub 환경에 통합되어 있으며, 이벤트(Push, Pull Request 등) 기반으로 특정 명령을 실행하는 구조를 가진다.

## 2. GitHub Actions 핵심 용어
* **Event**: 워크플로우를 트리거하는 특정 활동이다.
* **Jobs**: 단일 가상 환경에서 실행되는 명령의 집합으로, 여러 잡이 독립적으로 혹은 병렬로 실행될 수 있다.
* **Steps**: 잡 내부에서 순차적으로 실행되는 개별 프로세스 단위다.
* **Actions**: 잡을 구성하기 위한 독립적인 명령이자 워크플로우의 가장 작은 빌드 단위다.

## 3. Node.js 프로젝트 자동화 실습
Node.js 프로젝트를 생성하고 GitHub Actions를 통해 테스트와 배포를 관리하는 과정이다.

### 1) 프로젝트 환경 구성
* `npm init`을 통해 프로젝트를 초기화하고, `mocha`와 같은 테스트 프레임워크를 설치한다.
* `package.json`의 스크립트 항목에 테스트 실행 명령을 정의한다.
* `.gitignore` 파일을 생성하여 `node_modules` 등 불필요한 파일이 원격 저장소에 올라가지 않도록 설정한다.

### 2) 워크플로우 적용
* 로컬 저장소를 GitHub 원격 저장소와 연결한다.
* `.github/workflows` 디렉토리를 생성하고 YAML 형식의 워크플로우 파일을 작성하여 특정 브랜치에 푸시될 때 테스트와 배포가 이루어지도록 설정한다.

## 4. Python 웹 프로젝트 Docker Hub 배포 실습
Flask 프레임워크와 MongoDB를 사용하는 웹 애플리케이션을 빌드하여 Docker Hub에 자동 배포한다.

### 1) 애플리케이션 및 이미지 준비
* Flask 프로젝트 소스 코드(`app.py`)와 의존성 리스트(`requirements.txt`)를 작성한다.
* `FROM python:3.8-slim`을 기반으로 하는 Dockerfile을 작성하여 컨테이너 이미지를 정의한다.
* 로컬에서 `docker build`와 `docker run` 명령을 통해 애플리케이션이 정상적으로 구동되는지 검증한다.

### 2) 자동 배포 파이프라인(CI Pipeline) 구축
* **보안 설정**: Docker Hub 계정 정보와 액세스 토큰을 GitHub 레포지토리의 `Secrets`에 등록한다. (보안상의 이유로 평문 비밀번호 대신 토큰 사용 권장)
* **YAML 워크플로우 작성**:
    1.  `actions/checkout`: 소스 코드를 가상 환경으로 가져온다.
    2.  `actions/setup-python`: 필요한 파이썬 버전을 설정한다.
    3.  `docker/login-action`: GitHub Secrets를 활용해 Docker Hub에 로그인한다.
    4.  **Build & Push**: 컨테이너 이미지를 빌드하고 태그를 부여한 뒤 Docker Hub 레포지토리로 전송한다.