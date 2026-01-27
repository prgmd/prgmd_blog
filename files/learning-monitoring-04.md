---
id: learning-monitoring-04
title: "MSA 구성 요소 및 Elastic Stack 개요"
date: "2026-08-28"
category: "learning"
subCategory: "monitoring"
excerpt: "마이크로서비스 아키텍처를 지탱하는 주요 컴포넌트들과 전문 검색 및 빅데이터 처리를 위한 엘라스틱 스택의 구조 정리"
---

## 1. 마이크로서비스 아키텍처(MSA) 주요 컴포넌트
MSA 환경에서는 분산된 서비스들을 효율적으로 관리하기 위해 다양한 기술적 요소들이 유기적으로 결합되어야 한다.

### 1) API Gateway
* 각각의 마이크로서비스 API를 외부 클라이언트에게 통합된 인터페이스로 제공하는 진입점 역할을 수행한다.
* 오픈소스로는 Zuul, Spring Cloud Gateway 등이 활용되며, 상용 제품으로는 Google의 APIgee나 Redhat의 3Scale 등이 존재한다.

### 2) 서비스 메시 (Service Mesh)
* 서비스 간의 디스커버리, 라우팅, 로드 밸런싱, 보안, 인증/인가 등의 기능을 담당한다.
* 데이터 플레인(Data Plane)과 컨트롤 플레인(Control Plane)으로 계층을 나누어 관리한다.
* 구현 방식에 따라 Mesh-Native, Mesh-Aware, Mesh-Agnostic(Istio/Envoy 등)으로 분류되며, Istio를 사용하면 코드 수정 없이 보안 및 정책 관리가 가능하다.

### 3) 백킹 서비스 (Backing Service) 및 텔레메트리
* **백킹 서비스**: 지속성을 위한 RDBMS/NoSQL, 속도 향상을 위한 캐시(Redis), 비동기 통신을 위한 메시지 브로커(Kafka, Rabbit MQ) 등이 포함된다.
* **텔레메트리 (Telemetry)**: 분산된 서비스의 상태를 파악하기 위해 로깅(ELK/EFK), 추적(Sleuth/Zipkin), 모니터링(Prometheus/Grafana) 기술을 사용한다.

## 2. CI/CD 및 자동화 환경
* 개발, 테스트, 배포 전 과정을 자동화하여 지속적인 통합과 전달을 지원한다.
* 주요 도구로 Git, Gradle, Maven, JUnit, Jenkins, Helm, Nexus, Harbor 등이 유기적으로 사용된다.

## 3. 엘라스틱 스택 (Elastic Stack)
전문 검색(Full Text Search)과 빅데이터 파이프라인 구축을 위한 오픈소스 솔루션 집합이다.

### 1) 탄생과 발전
* 텍스트 검색 라이브러리인 Lucene 프로젝트를 기반으로, 이를 솔루션화한 Elastic Search가 중심이 된다.
* 빅데이터의 수집, 처리, 분석 요구를 충족하기 위해 여러 구성 요소를 스택 형태로 쌓아 올린 구조를 가진다.

### 2) 핵심 구조
* **Elasticsearch**: 분산형 저장소로서 데이터를 검색하고 분석하는 핵심 엔진이다.
* **Logstash**: 다양한 소스에서 데이터를 수집하고 변환하여 저장소로 전송하는 처리 단계이다.
* **Kibana**: 저장된 데이터를 시각화하고 엘라스틱 서치를 관리하는 JavaScript 기반 도구이다.