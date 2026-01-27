---
id: learning-cicd-07
title: "CI/CD (7) - Argo CD 실습: 설치 및 애플리케이션 배포"
date: "2025-08-22"
category: "learning"
subCategory: "cicd"
excerpt: "Helm을 이용한 Argo CD 설치와 CLI 및 Manifest를 활용한 Nginx 애플리케이션 배포 실습 정리"
---

## 1. 사전 지식
Argo CD 실습을 위해 쿠버네티스(Kubernetes), 헬름(Helm), 커스터마이즈(Kustomize)에 대한 이해가 필요하며, 모니터링을 위한 프로메테우스(Prometheus) 지식이 요구된다.

## 2. Argo CD 설치 및 초기 설정
Helm 저장소를 사용하여 특정 네임스페이스에 Argo CD를 설치하고 외부 접속 환경을 구성한다.

### 1) 설치 단계
* **레포지토리 추가**: `helm repo add argo https://argoproj.github.io/argo-helm` 명령으로 저장소를 등록하고 업데이트한다.
* **네임스페이스 생성**: 관리의 편의를 위해 `argocd`라는 전용 네임스페이스를 생성한다.
* **설치 수행**: `helm install argocd argo/argo-cd -n argocd` 명령으로 설치를 완료한다.

### 2) 외부 접속 설정
* **서비스 타입**: 기본적으로 모든 서비스가 `ClusterIP`로 생성되므로 클러스터 외부에서는 접근이 불가능하다.
* **접속 방법**:
    - 로컬 환경: `kubectl port-forward`를 사용하여 특정 포트를 브라우저와 연결한다.
    - 클라우드 환경: 서비스 타입을 `NodePort`나 `LoadBalancer`로 수정하여 공인 IP를 할당받는다.
* **비밀번호 확인**: 설치 시 생성된 초기 관리자 비밀번호는 `kubectl get secret` 명령을 통해 확인 후 Base64로 디코딩하여 사용한다.

## 3. 애플리케이션 배포 실습
Argo CD를 통해 Nginx 웹 서버를 배포하는 두 가지 방법을 실습한다.

### 1) 매니페스트(YAML) 방식
* `Application` 리소스 파일을 작성하여 소스 저장소(GitHub), 대상 클러스터, 배포할 네임스페이스 등을 정의한다.
* `syncPolicy` 설정을 통해 자동 동기화(automated) 및 리소스 삭제(prune), 자가 치유(selfHeal) 기능을 활성화할 수 있다.
* `kubectl apply -f` 명령으로 해당 리소스를 클러스터에 적용한다.

### 2) Argo CD CLI 방식
* 전용 CLI 도구를 설치하여 명령줄에서 직접 배포를 제어한다.
* `argocd login`으로 인증을 수행한 뒤 `argocd app create` 명령을 사용하여 저장소 URL과 차트 이름을 지정해 배포한다.
* `argocd app sync` 명령을 통해 명시적으로 상태를 동기화할 수 있다.

## 4. Argo CD Autopilot
Argo CD를 GitOps 방식으로 더 쉽게 운영하기 위한 도구이다.

* **핵심 기능**: 수동 설치 대신 Git 리포지토리 중심의 자동화된 관리 구조를 제공한다.
* **장점**: 새로운 서비스 추가 시 Git 구조에 맞게 자동으로 세팅되며, 재해 복구나 시크릿 암호화 기능을 지원하여 운영 안정성을 높인다.