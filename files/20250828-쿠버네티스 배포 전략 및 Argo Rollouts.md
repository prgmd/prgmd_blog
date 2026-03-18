---
id: 20250828-learning-cicd-08
title: "쿠버네티스 배포 전략 및 Argo Rollouts"
date: "2025-08-28"
category: "learning"
subCategory: ["CI/CD", "Kubernetes"]
---

## 1. 쿠버네티스 표준 블루-그린 배포 (Blue-Green)
별도의 도구 없이 쿠버네티스 기본 리소스(Deployment, Service)만을 이용하여 트래픽을 전환하는 방식이다.

### 1) 배포 준비 및 수행
* **애플리케이션 준비**: 버전 정보(v1.0, v2.0)를 반환하는 소스 코드를 빌드하여 각각 다른 태그의 도커 이미지로 생성한다.
* **Blue 환경 구성**: `version: "1.0"` 레이블을 가진 Deployment를 생성하고, 서비스의 `selector`가 해당 버전을 바라보도록 설정하여 배포한다.
* **Green 환경 구성**: 새 버전인 `version: "2.0"` 레이블을 가진 Deployment를 클러스터에 미리 배포한다. 이 시점에서는 서비스가 여전히 v1.0을 바라보고 있으므로 사용자에게는 영향이 없다.
* **트래픽 전환**: 서비스(Service) 매니페스트의 `selector` 값을 `version: "2.0"`으로 수정하여 적용하면 즉시 모든 트래픽이 새 버전으로 전환된다.

## 2. Argo Rollouts를 활용한 고급 배포 전략
쿠버네티스 기본 Deployment의 롤링 업데이트 한계를 극복하기 위해 확장된 기능을 제공하는 컨트롤러이다.

### 1) 도입 배경 (Rolling Update의 한계)
* 업데이트 속도 조절이 불가능하고 트래픽 미세 전환 기능이 부족하다.
* 배포 중 상태를 확인할 수 있는 메트릭 분석 기능이 없으며, 장애 발생 시 자동 롤백을 지원하지 않는다.

### 2) Argo Rollouts 설치
* 전용 네임스페이스(`argo-rollouts`)를 생성하고 공식 설치 경로를 통해 컨트롤러를 배포한다.

### 3) 주요 배포 전략 및 설정
* **블루-그린 (Blue-Green)**:
    - `activeService`와 `previewService`를 지정하여 배포 전후의 서비스를 명확히 구분한다.
    - `autoPromotionEnabled` 옵션을 통해 새 버전 검증 후 자동으로 승격할지 여부를 결정할 수 있다.
* **카나리 (Canary)**:
    - 전체 트래픽 중 일부(예: 20%)만 신규 버전으로 보내 안정성을 먼저 검토한다.
    - `steps` 설정을 통해 가중치 조절(`setWeight`)과 일시 중단(`pause`) 시간을 단계별로 정의하여 배포를 세밀하게 제어한다.

## 3. 시크릿(Secret) 관리 보안
애플리케이션 배포 시 민감한 정보를 보호하기 위한 권장 사항이다.
* 쿠버네티스 기본 Secret에 저장하는 것보다 Vault, AWS Secret Manager, Azure Key Vault 등 전문 외부 저장소를 활용하는 것이 가장 안전하다.