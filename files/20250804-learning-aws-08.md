---
id: 20250804-learning-aws-08
title: "EKS 구축 도구 및 RDS 인프라 구성"
date: "2025-08-04"
category: "learning"
subCategory: ["AWS", "Kubernetes"]
---

## 1. EKS 구축 및 관리 도구 설치
EKS 클러스터를 효율적으로 구축하고 조작하기 위해 세 가지 핵심 CLI(Command Line Interface) 도구를 설치하고 설정한다.

### 1) AWS CLI
* **용도**: AWS 리소스를 명령어로 제어하고 `eksctl`이 AWS 자격 증명을 사용할 수 있도록 기반을 제공한다.
* **설정**: 사용자 생성 시 필요한 권한을 부여한 후 발급받은 액세스 키(Access Key)와 비밀 액세스 키(Secret Access Key)를 `aws configure` 명령을 통해 등록한다.
* **확인**: `aws --version`으로 설치 여부를 확인하고, `aws configure list-profiles`로 등록된 프로필을 확인한다.

### 2) eksctl
* **용도**: EKS 클러스터를 생성, 관리, 업데이트하기 위한 전용 CLI 도구다.
* **설치**: Windows(바이너리), Mac(Homebrew), Linux 등 운영체제별 환경에 맞춰 설치한다.
* **확인**: `eksctl version` 명령어를 사용한다.

### 3) kubectl
* **용도**: 표준 쿠버네티스 명령어로 클러스터 내부의 파드, 서비스 등 리소스를 관리한다.
* **확인**: `kubectl version --client` 명령어를 사용한다.

## 2. EKS 인프라 구축 절차 (CloudFormation 연동)
AWS의 인프라 자동화 도구인 CloudFormation을 활용하여 네트워크와 클러스터를 구성한다.

### 1) VPC 및 네트워크 환경 구축
* CloudFormation을 통해 리전, 가용 영역(AZ), IP 대역이 설정된 VPC를 구축한다.
* 생성 완료 후 스택의 출력(Output) 탭에서 워커 노드가 배치될 서브넷 정보(`WorkerSubnets`)를 반드시 복사해 둔다.

### 2) EKS 클러스터 생성
* `eksctl create cluster` 명령어를 실행할 때 복사한 서브넷 ID를 `--vpc-public-subnets` 옵션에 입력한다.
* 클러스터 이름, 리전, 쿠버네티스 버전 등을 명시하여 클러스터 구축을 완료한다.

## 3. 애플리케이션 이미지 관리 및 RDS 구축
구축된 클러스터에서 실행할 애플리케이션 이미지와 데이터를 저장할 데이터베이스 환경을 준비한다.

### 1) ECR (Elastic Container Registry) 활용
* 로컬에서 빌드한 백엔드 애플리케이션 이미지를 AWS의 프라이빗 레지스트리인 ECR에 푸시한다.
* 이미지 태그 형식 예시: `[AWS_ACCOUNT_ID].dkr.ecr.[REGION].amazonaws.com/k8s/backend-app:1.0.0`

### 2) RDS (Relational Database Service) 환경 구성
* **고가용성 설계**: 서비스 안정성을 위해 데이터베이스를 여러 가용 영역(Multi-AZ)에 걸쳐 다중화하여 구축한다.
* **관리형 서비스의 특성**: RDS는 AWS가 관리하는 서비스이므로 DB 서버 OS에 직접 로그인할 수 없으며, 환경 설정에 일부 제약이 존재한다.
* **Bastion Host 활용**: 보안이 강화된 내부 네트워크의 DB에 접근하기 위해 중계 서버인 베스천 호스트(Bastion Host)를 구축하여 관리 포인트로 활용한다. 이는 주로 EC2 인스턴스를 통해 구현한다.