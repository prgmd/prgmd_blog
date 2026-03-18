---
id: 20250806-learning-aws-10
title: "EKS 로그 관리, 오토스케일링 및 클러스터 보안"
date: "2025-08-06"
category: "learning"
subCategory: ["AWS", "Kubernetes", "Monitoring"]
---

## 1. 로그 관리와 운영
쿠버네티스 환경에서는 파드가 동적으로 생성 및 삭제되므로 기존의 서버 파일 로그 저장 방식 대신 통합된 로그 관리 체계가 필요하다.

### 1) 주요 로그 관리 도구
* **ELK / EFK 스택**: 데이터 저장(Elastic Search), 수집 및 변환(Log Stash 또는 Fluentd), 시각화(Kibana) 도구를 조합하여 사용한다.
* **EKS 표준 방식**: Fluentd를 데몬셋(DaemonSet)으로 기동하여 각 노드에서 파드의 로그를 수집하고, 이를 AWS의 CloudWatch Logs로 전송하여 관리한다.

### 2) 로그 수집 구성
* **애플리케이션 로그**: 컨테이너 로그는 호스트 변경 가능성으로 인해 표준 출력(stdout)으로 구성하는 것을 권장하며, `kubectl logs` 명령어로 실시간 확인이 가능하다.
* **CloudWatch 연동 실습**: 
    - 데이터 노드의 IAM 역할에 `CloudWatchAgentServerPolicy` 정책을 연결한다.
    - 전용 네임스페이스(`amazon-cloudwatch`)를 생성하고 클러스터 정보를 담은 ConfigMap을 등록한다.
    - Fluentd를 데몬셋으로 실행하여 CloudWatch Logs에 애플리케이션, 호스트, 데이터 플레인 로그 그룹이 자동 생성되도록 한다.

## 2. 오토스케일링 (AutoScaling)
시스템 부하 상황에 따라 노드 또는 파드의 리소스를 자동으로 조정하여 가용성을 확보한다.

### 1) Cluster AutoScaler (데이터 플레인)
* **동작 원리**: 파드 배포 시 리소스 요청(requests) 대비 노드의 여유 자원이 부족하여 파드가 `Pending` 상태가 되면 이를 감지하고 새로운 워커 노드를 자동으로 추가한다.
* **주의사항**: 실제 CPU 부하가 낮더라도 파드의 `requests` 설정값이 크면 불필요하게 노드가 증설될 수 있으며, 반대로 `limits` 설정 없이 `requests`만 낮으면 노드 과부하(Over Commit)가 발생할 수 있다.

### 2) Horizontal Pod Autoscaler (HPA)
* **기능**: 파드의 리소스(CPU, 메모리) 사용 현황을 실시간 모니터링하여 설정된 임계값을 넘을 경우 파드의 복제본 수(Replicas)를 자동으로 늘리거나 줄인다.
* **필수 요소**: HPA 작동을 위해서는 클러스터 내부에 리소스 사용량을 측정하는 메트릭 서버(Metrics Server)가 배포되어 있어야 한다.

## 3. 클러스터 보안 및 인가 관리
EKS는 AWS IAM과 쿠버네티스의 RBAC를 결합하여 강력한 보안 체계를 제공한다.

### 1) 인증(Authentication)과 인가(Authorization)
* **인증**: AWS CLI와 IAM을 사용하여 클러스터에 접근하는 사용자의 신원을 확인한다.
* **인가**: RBAC(Role-Based Access Control)를 통해 특정 사용자나 그룹이 수행할 수 있는 조작 권한을 제어한다.

### 2) RBAC 주요 오브젝트
* **Role / ClusterRole**: 파드나 서비스에 대해 수행 가능한 권한(get, list, watch 등)의 집합을 정의한다.
* **RoleBinding**: 특정 사용자 또는 그룹에 정의된 롤(Role)을 연결하여 실제로 권한을 부여한다.

### 3) 실습 예시: 제한된 권한의 사용자 생성
* 전용 네임스페이스(`rbac-test-ns`)를 생성하고, 해당 영역에서만 리소스를 조회할 수 있는 `ClusterRole`과 `RoleBinding`을 설정한다.
* `eksctl create iamidentitymapping` 명령어를 사용하여 AWS IAM 사용자를 쿠버네티스 내의 특정 권한 그룹과 매핑하여 보안 정책을 완성한다.