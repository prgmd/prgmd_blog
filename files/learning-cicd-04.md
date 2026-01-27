---
id: learning-cicd-04
title: "CI/CD (4) - Jenkins 개요 및 파이프라인 실습"
date: "2025-07-18"
category: "learning"
subCategory: "cicd"
excerpt: "오픈소스 자동화 서버인 Jenkins의 특징과 설치 방법, 그리고 Declarative/Scripted 파이프라인 작성법"
---

## 1. Jenkins 개요 및 특징
Jenkins는 Java로 작성된 오픈 소스 자동화 서버로, 소프트웨어 개발 시 빌드, 테스트, 배포 공정을 자동화하기 위해 사용된다.

* **주요 특징**:
    * **확장성**: 수많은 플러그인을 지원하여 다양한 도구와 연동이 가능하다.
    * **이식성**: Java 기반으로 운영체제 제약 없이 실행 가능하며 Docker 이미지, WAR 파일 등 다양한 형태를 지원한다.
    * **분산 처리**: Master/Agent 구조를 통해 여러 노드에 작업을 분산하여 실행할 수 있다.
    * **지원 범위**: 대부분의 버전 관리 시스템과 프로그래밍 언어를 지원한다.

## 2. Jenkins 설치 및 환경 설정
가장 효율적인 설치 방법 중 하나인 Docker를 이용한 설치 과정과 초기 설정 방법이다.

### 1) Docker를 이용한 설치
* `docker run` 명령을 통해 Jenkins 서버 컨테이너를 구동한다. 이때 8080 포트와 Agent 통신을 위한 50000 포트를 연결한다.
* 데이터의 영속성을 위해 `-v` 옵션으로 볼륨을 연결한다.
* 설치 후 `docker logs` 명령이나 컨테이너 내부의 `initialAdminPassword` 파일을 확인하여 초기 관리자 비밀번호를 획득한다.

### 2) GitHub WebHook 연동
* **Access Token 발급**: GitHub에서 토큰을 생성하여 Jenkins와의 인증에 사용한다.
* **Credential 등록**: Jenkins 관리 메뉴에서 발급받은 토큰을 'Secret text' 형태로 저장한다.
* **Trigger 설정**: Jenkins 아이템 설정에서 'GitHub hook trigger for GITScm polling'을 활성화하여 코드 업데이트 시 자동 빌드가 수행되도록 한다.

## 3. Jenkins Pipeline 활용
파이프라인은 CI/CD 과정을 하나의 스크립트로 정의하는 기능이다. 시각화를 위해 'Delivery Pipeline' 플러그인을 주로 사용한다.

### 1) 파이프라인 작성 방식
* **Declarative (선언형)**: `pipeline` 블록으로 시작하며 구조가 엄격하여 가독성이 좋다. 최신 표준 방식이다.
* **Scripted (스크립트형)**: `node` 블록으로 시작하며 Groovy 기반의 제어문(if, for 등)을 자유롭게 사용할 수 있어 복잡한 로직 구현에 유리하다.

### 2) 스크립트 예시 구조
* **Ready/Build/Deploy**: 각 단계를 `stage`로 구분하여 정의한다.
* **Agent 설정**: 작업을 실행할 환경을 지정한다. (예: `agent any`)

## 4. 빌드 도구 연동 (Maven)
* Java 프로젝트 빌드를 위해 Jenkins 도구 설정 메뉴에서 Maven 플러그인을 설치한다.
* 사용하고자 하는 Maven 버전을 설정한 후, Jenkins 아이템에서 Maven 프로젝트를 생성하여 빌드 절차를 구성한다.