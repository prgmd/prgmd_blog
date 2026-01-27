---
id: learning-cicd-06
title: "GitOps와 Argo CD: 원칙부터 실습까지"
date: "2025-08-22"
category: "learning"
subCategory: "cicd"
excerpt: "선언적 인프라 관리를 위한 GitOps 원칙, Argo CD 아키텍처, Helm을 이용한 설치 및 애플리케이션 배포 실습 정리"
---

## 1. GitOps의 정의와 핵심 원칙
GitOps는 운영 업무에 Pull Request를 활용하고, 인프라 설정을 Git으로 통제하는 프로세스이다.

### 1) 주요 운영 원칙
* **선언적 구성**: 시스템이 도달해야 할 최종 상태를 선언하면 에이전트가 이를 구현한다.
* **불변적 저장소**: 모든 설정은 버전 제어가 가능한 저장소에서 관리한다.
* **자동화된 배포**: 저장소 변경이 감지되면 소프트웨어 에이전트가 실제 환경에 즉시 동기화한다.
* **지속적 루프**: 선언된 상태와 실제 상태를 계속 비교하여 일치하도록 유지한다.

### 2) 쿠버네티스와의 정합성
쿠버네티스는 선언형 API 모델에 최적화되어 있어 GitOps 구현에 적합하다.

## 2. Argo CD 아키텍처

### 1) 주요 구성 요소
* **Application Controller**: 애플리케이션 상태를 감시하며, 레플리카 수를 조정하여 성능을 높일 수 있다.
* **Kustomization 활용**: 패치 파일을 통해 설정을 코드로 관리한다.

### 2) Redis 캐시
* **성능 최적화**: Git 레포지토리에서 생성된 매니페스트를 캐싱하여 동기화 성능을 높인다.
* **고가용성**: 3개의 레플리카를 갖춘 StatefulSet 구성을 권장한다.

## 3. Argo CD 설치 및 초기 설정
Helm을 사용하여 설치하고 외부 접속 환경을 구성한다.

### 1) 설치 단계
* **레포지토리 추가**: `helm repo add argo https://argoproj.github.io/argo-helm`
* **네임스페이스 생성**: `argocd` 전용 네임스페이스 생성
* **설치 수행**: `helm install argocd argo/argo-cd -n argocd`

### 2) 외부 접속 설정
* **로컬 환경**: `kubectl port-forward`로 브라우저와 연결
* **클라우드 환경**: 서비스 타입을 `NodePort`나 `LoadBalancer`로 수정
* **비밀번호 확인**: `kubectl get secret`으로 초기 관리자 비밀번호 확인

## 4. 애플리케이션 배포 실습

### 1) 매니페스트(YAML) 방식
* `Application` 리소스 파일에 소스 저장소, 대상 클러스터, 네임스페이스 등을 정의
* `syncPolicy`로 자동 동기화, 리소스 삭제, 자가 치유 기능 활성화
* `kubectl apply -f` 명령으로 클러스터에 적용

### 2) CLI 방식
* `argocd login`으로 인증 후 `argocd app create`로 배포
* `argocd app sync`로 명시적 상태 동기화

## 5. Argo CD Autopilot
GitOps 방식으로 Argo CD를 더 쉽게 운영하기 위한 도구이다.

* **핵심 기능**: Git 리포지토리 중심의 자동화된 관리 구조 제공
* **장점**: 새로운 서비스 추가 시 Git 구조에 맞게 자동 세팅, 재해 복구 및 시크릿 암호화 지원
