---
id: 20250729-learning-aws-07
title: "EKS 클러스터 구축 및 백엔드 개발 환경 설정"
date: "2025-07-29"
category: "learning"
subCategory: ["AWS", "Kubernetes"]
---

## 1. Amazon EKS (Elastic Kubernetes Service) 개요
EKS는 쿠버네티스의 컨트롤 플레인을 관리해 주는 AWS의 관리형 서비스이다.

### 1) 주요 특징
* **VPC 통합**: 파드(Pod) 네트워크가 VPC 내부 주소 대역을 사용할 수 있어 클러스터 외부와의 통신이 원활하다.
* **IAM 인증**: AWS IAM을 통해 클러스터의 인증 및 인가 관리를 수행한다.
* **ELB 연계**: 쿠버네티스 서비스 타입 중 LoadBalancer를 설정하면 자동으로 AWS ELB가 생성되어 L7 로드 밸런싱 기능을 구현할 수 있다.
* **데이터 플레인 선택**: EC2 인스턴스뿐만 아니라 서버리스 방식인 Fargate 서비스도 활용 가능하다.

## 2. 클러스터 구축 도구 및 환경 설정
클러스터 구축을 위해 IaC(Infrastructure as Code) 도구와 명령줄 인터페이스를 설치한다.

* **AWS CLI**: AWS 리소스 조작을 위한 도구로, 액세스 키 설정을 통해 인증을 완료해야 한다.
* **eksctl**: EKS 클러스터 구축 전용 도구로, 복잡한 인프라 생성을 명령어로 간소화한다.
* **kubectl**: 클러스터 내부의 리소스를 관리하기 위한 표준 명령줄 도구이다.
* **AWS CloudFormation**: 템플릿 기반으로 리소스를 관리하며, 동일한 스택을 일관성 있게 반복 배포할 수 있도록 돕는다.

## 3. EKS 클러스터 구축 과정
실제 구축은 네트워크 인프라 준비와 클러스터 생성 단계로 나뉜다.

### 1) 기본 리소스 생성 (CloudFormation)
* YAML 템플릿을 사용하여 VPC, 서브넷(WorkerSubnet), 인터넷 게이트웨이 및 라우팅 테이블을 생성한다.
* 생성된 스택의 출력(Outputs) 탭에서 서브넷 ID 목록을 복사하여 다음 단계에서 활용한다.

### 2) 클러스터 생성 (eksctl)
* `eksctl create cluster` 명령어를 사용하여 클러스터 이름, 리전, 버전, 노드 그룹 설정 등을 포함하여 실행한다.
* 관리 권한을 위해 IAM 사용자에게 필요한 인라인 정책을 추가로 부여한다.

## 4. 클러스터 연결 및 동작 확인
구축된 클러스터를 로컬 환경과 연결하고 테스트용 워크로드를 배포한다.

* **kubeconfig 설정**: `aws eks update-kubeconfig` 명령을 통해 로컬의 설정 파일을 업데이트하여 클러스터에 접속할 정보를 저장한다.
* **동작 테스트**: `nginx-pod`를 생성하여 배포하고, `kubectl port-forward`를 통해 로컬 브라우저에서 접속 가능 여부를 검증한다.

## 5. 백엔드 애플리케이션 개발 환경 구성
EKS에 배포할 백엔드 앱의 로컬 테스트 환경을 구축한다.

### 1) 데이터베이스 설정 (PostgreSQL)
* 도커를 이용하여 PostgreSQL 컨테이너를 구동하고, 전용 사용자와 데이터베이스(`myworkdb`)를 생성한다.
* `region`, `location`, `batch_processing` 등의 샘플 테이블을 생성하고 기초 데이터를 입력한다.

### 2) Spring Boot 프로젝트 구성
* **의존성 설정**: Data JPA, PostgreSQL Driver, Spring Web, Lombok 등을 포함한다.
* **애플리케이션 설정**: `application.yaml` 파일을 통해 DB 접속 정보와 하이버네이트 방언(Dialect)을 설정한다.
* **엔티티(Entity) 개발**: `AbstractEntity`를 상속받는 `RegionEntity`, `LocationEntity` 등을 작성하여 DB 테이블과 매핑을 완료한다.