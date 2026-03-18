---
id: 20250722-learning-aws-02
title: "EC2 앱 배포 및 Elastic Load Balancing"
date: "2025-07-22"
category: "learning"
subCategory: "AWS"
---

## 1. EC2 애플리케이션 배포 (Django)
로컬에서 개발한 Django 프로젝트를 AWS EC2 인스턴스로 옮겨 실행하는 환경을 구축한다.

### 1) 애플리케이션 준비 및 설정
* 가상 환경을 생성하고 필요한 패키지(Django 등)를 설치한다.
* `settings.py`의 `ALLOWED_HOSTS`를 수정하여 모든 호스트에서의 접근을 허용하고, `pip freeze`를 통해 의존성 목록(`requirements.txt`)을 생성한다.

### 2) EC2 환경 구축 및 실행
* Git을 이용해 코드를 가져온 후, EC2 내부에서 의존성 패키지를 설치한다. (시스템 패키지 충돌 시 `--break-system-packages` 옵션 등을 활용 가능)
* `manage.py runserver 0.0.0.0:80` 명령으로 서버를 구동하며, 보안 그룹에서 80번 포트가 개방되어 있어야 외부 접속이 가능하다.

## 2. Route53 도메인 연결
사용자가 고정된 IP 대신 도메인 이름을 통해 서비스에 접근할 수 있도록 설정한다.

* **A 레코드 생성**: 구매한 도메인에 대해 EC2의 퍼블릭 IP를 매핑하는 A 레코드를 등록한다.
* **HTTPS 준비**: 도메인이 연결되어야 보안 인증서(SSL/TLS) 적용이 가능하므로 운영 환경에서 도메인 설정은 필수적이다.

## 3. Elastic Load Balancing (ELB)
AWS에서 제공하는 부하 분산 서비스로, 여러 대상에 트래픽을 효율적으로 분배한다.

### 1) ELB의 주요 종류
* **ALB (Application Load Balancer)**: OSI 7계층(애플리케이션)에서 동작한다. URL 경로나 호스트 이름 등 HTTP/HTTPS 요청 내용을 기반으로 정교한 라우팅을 수행한다.
* **NLB (Network Load Balancer)**: 4계층(전송)에서 동작한다. 매우 높은 성능이 요구되거나 고정 IP 주소가 필요한 경우, TCP/UDP 트래픽 분산에 적합하다.
* **CLB (Classic Load Balancer)**: 예전 방식의 로드 밸런서로, 신규 시스템 구축 시에는 권장되지 않는다.

### 2) 비용 구조
* 시간당 사용료와 처리된 트래픽의 용량 단위(LCU) 요금의 합계로 부과된다.