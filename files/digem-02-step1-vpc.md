---
id: digem-02-step1-vpc
title: "Digem 개발기 2편 — 초기 설계: VPC 안에 Lambda를 넣었더니"
date: "2026-05-19"
category: "projects"
subCategory: "Digem"
---

# Step 1 — VPC Isolation 기반 설계

## 구조

처음 설계는 보안을 최우선으로 생각했습니다. Lambda 함수를 VPC(Virtual Private Cloud)의 Private Subnet 안에 배치하고, EC2를 스토리지로 사용하는 구조였습니다.

```
크롤러 (Lambda, VPC Private Subnet)
    ↓
NAT Gateway (외부 인터넷 접근을 위한 관문)
    ↓
외부 사이트 (크롤링 대상)
    ↓
EC2 (수집 데이터 저장)
```

VPC는 AWS 안에 격리된 가상 네트워크입니다. Private Subnet에 Lambda를 두면 외부 인터넷에서 직접 접근할 수 없어 보안상 안전합니다. 여기까지는 좋은 설계처럼 보였습니다.

## 문제 발생 — NAT Gateway 비용

그런데 청구서를 확인하고 당황했습니다. 예상보다 훨씬 많은 비용이 나오고 있었습니다.

원인은 NAT Gateway였습니다. VPC Private Subnet 안에 있는 Lambda가 외부 인터넷(크롤링 대상 사이트)에 접근하려면 반드시 NAT Gateway를 거쳐야 합니다. NAT Gateway의 요금 구조는 두 가지로 구성됩니다.

- **시간당 고정 요금**: NAT Gateway가 켜져 있는 시간만큼 고정으로 부과
- **데이터 전송 요금**: NAT Gateway를 통해 오가는 데이터 양에 비례해 부과

크롤링은 외부 사이트에 요청을 보내고 대량의 HTML/데이터를 받아오는 작업입니다. 일반적인 웹 서비스와 달리 외부로 나가는 트래픽이 많고, 받아오는 데이터 양도 상당합니다. 이 특성 때문에 데이터 전송 요금이 빠르게 쌓였습니다.

개인 프로젝트에서 이 비용을 계속 감당하기는 어려웠습니다.

## 깨달은 것

설계할 때 보안 측면만 생각하고 비용 구조를 제대로 따져보지 않았습니다. AWS 서비스는 각각의 요금 모델이 다르고, 워크로드 특성에 따라 예상치 못한 곳에서 비용이 발생합니다.

**크롤링처럼 외부 트래픽이 많은 워크로드에 VPC + NAT Gateway 조합은 맞지 않습니다.** Lambda를 VPC 밖으로 꺼내는 것이 비용과 구조 모두에서 더 나은 선택이라는 결론을 내렸습니다.

---

# 다음 편에서는

VPC를 걷어내고 Public Lambda + S3 구조로 전환하는 과정을 다룹니다. 특히 이미 운영 중인 서비스를 중단하지 않고 인프라를 통째로 교체하기 위해 적용한 Blue-Green 배포 전략을 자세히 설명합니다.
