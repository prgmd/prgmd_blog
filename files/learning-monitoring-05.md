---
id: learning-monitoring-05
title: "ELK 스택 설치 및 Spring Boot 로그 수집 환경 구축"
date: "2026-08-29"
category: "learning"
subCategory: "monitoring"
excerpt: "Linux 서버에 Elasticsearch, Logstash, Kibana를 직접 설치하고 Spring Boot 애플리케이션의 로그를 실시간으로 수집하는 방법 정리"
---

## 1. ELK Stack 리눅스 서버 설치
데이터 수집, 처리, 시각화를 위한 ELK 스택의 각 컴포넌트를 Ubuntu 환경에 설치하고 기본 설정을 수행한다.

### 1) 사전 준비 및 Elasticsearch 설치
* **패키지 업데이트**: `apt update`를 통해 시스템을 최신 상태로 유지하고, HTTPS 통신을 위한 필수 패키지(`wget`, `apt-transport-https`, `gnupg`)를 설치한다.
* **Elasticsearch 설치**: Elastic 공식 GPG 키와 저장소를 추가한 후 패키지를 설치한다.
* **보안 설정**: 설치 후 `elasticsearch-reset-password` 명령을 사용하여 `elastic` 관리자 계정의 비밀번호를 발급받는다.
* **서비스 실행**: `systemctl`을 이용하여 서비스를 활성화하고 시작하며, 9200 포트에서 정상 구동 여부를 확인한다.

### 2) Logstash 및 Kibana 설치
* **Logstash**: 패키지를 설치한 후 JDK 17 환경을 구성한다. 바이너리 실행을 위해 환경 변수(PATH)를 등록한다.
* **Kibana**: 패키지 설치 후 외부 접속을 위해 `kibana.yml` 설정 파일의 `server.host`를 `0.0.0.0`으로 수정한다.
* **방화벽 허용**: 서비스 통신을 위해 5601(Kibana), 9200(Elasticsearch), 5044(Logstash Beats) 포트를 개방한다.
* **Kibana 연동**: Elasticsearch 서버에서 생성한 등록 토큰(enrollment token)과 `journalctl`로 확인한 검증 코드를 입력하여 보안 설정을 완료한다.

### 3) 에이전트(Beat) 설치
* 로그 파일 전송을 위한 **Filebeat**와 시스템 지표 수집을 위한 **Metricbeat**를 추가로 설치하여 수집 체계를 보완한다.

## 2. Spring Boot 프로젝트 로그 수집 연동
애플리케이션에서 발생하는 로그를 실시간으로 Logstash로 전송하여 Elasticsearch에 저장하는 파이프라인을 구축한다.

### 1) Logstash 파이프라인 설정
* **Input**: TCP 5044 포트를 통해 JSON 코덱 형식의 로그 데이터를 수신하도록 설정한다.
* **Output**: 수신된 데이터를 Elasticsearch의 특정 인덱스(`springboot-elk`)로 전송하도록 정의하며, 인증 정보를 포함한다.

### 2) Spring Boot 애플리케이션 구성
* **의존성 추가**: `build.gradle`에 `logstash-logback-encoder` 라이브러리를 추가하여 로그를 JSON 포맷으로 변환할 수 있게 한다.
* **Logback 설정**: `logback.xml` 파일을 생성하여 `LogstashTcpSocketAppender`를 등록한다. 이때 목적지(destination)는 Logstash 서버의 IP와 포트로 지정한다.
* **로그 출력 예시**:
    - **Controller**: `/member/{name}` 등 특정 경로 호출 시 `log.info`를 사용하여 추적용 로그를 남긴다.
    - **ApplicationRunner**: 반복문을 사용하여 주기적으로 테스트 로그를 발생시켜 수집 상태를 실시간으로 검증한다.

### 3) 로그 확인 및 분석
* 설정이 완료되면 Kibana UI에 접속하여 생성된 인덱스 패턴을 등록하고, 애플리케이션에서 발생한 로그가 대시보드에 실시간으로 적재되는지 확인한다.