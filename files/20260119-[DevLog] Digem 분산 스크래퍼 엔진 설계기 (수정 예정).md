---
id: 20260119-[DevLog] Digem 분산 스크래퍼 엔진 설계기 (수정 예정)
title: "[DevLog] Digem: 분산 스크래퍼 엔진 설계기 (수정 예정)"
date: "2026-01-19"
category: "projects"
subCategory: "Digem"
hidden: True
---

## 1. 개요
"Dig your uncut gems"라는 슬로건 아래, 흩어져 있는 음악 비평과 아티클을 한곳에 모아 요약·번역해주는 서비스 **Digem**의 핵심 엔진인 스크래퍼 개발 과정을 기록합니다.가

## 2. 해결하고자 했던 문제 (Problem)
단일 스크래퍼로 여러 매체(Pitchfork, The Quietus 등)를 긁어올 때 다음과 같은 병목 현상이 발생했습니다.
- **차단 리스크:** 단일 IP에서의 과도한 요청으로 인한 밴(Ban).
- **확장성 부족:** 수집 대상 매체가 늘어날수록 선형적으로 늘어나는 실행 시간.
- **데이터 유실:** 네트워크 에러 발생 시 진행 중인 작업의 상태 저장 불가.



## 3. 설계 전략 (Architecture)
문제를 해결하기 위해 **Redis 기반의 작업 큐**와 **분산 워커 시스템**을 도입했습니다.

| 구성 요소 | 역할 | 비고 |
| :--- | :--- | :--- |
| **Scheduler** | 수집 대상을 정의하고 Redis 큐에 Task 삽입 | Python (APScheduler) |
| **Redis** | 중복 수집 방지(Filtering) 및 작업 대기열 관리 | In-memory DB |
| **Worker Nodes** | 실제 스크래핑 로직 수행 (Multi-Instance) | Dockerized App |
| **MongoDB** | 정형화된 아티클 데이터 저장 | NoSQL |
