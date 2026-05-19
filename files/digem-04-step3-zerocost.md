---
id: digem-04-step3-zerocost
title: "Digem 개발기 4편 — 운영비 0원: Supabase + Vercel로의 전환"
date: "2026-05-19"
category: "projects"
subCategory: "Digem"
---

# Step 3 — Zero-Cost 아키텍처

## 왜 또 바꿨나

Step 2에서 NAT Gateway 비용 문제는 해결했습니다. 하지만 AWS Lambda와 S3도 사용량이 쌓이면 비용이 발생합니다. Free Tier 한도를 넘으면 조금씩이라도 청구가 되는 구조입니다.

개인 프로젝트를 장기적으로 운영하려면 비용 부담이 없어야 한다는 결론을 내렸습니다. 목표는 단순했습니다. **월 운영비 0원.**

## Supabase + Vercel 조합

Free Tier가 강력한 플랫폼들로 전환했습니다.

### Supabase

Supabase는 PostgreSQL 기반의 BaaS(Backend as a Service)입니다. AWS RDS처럼 관계형 DB를 사용할 수 있으면서, 사용자 인증(Auth) 기능까지 내장되어 있습니다. Free Tier에서 500MB DB와 월 50,000 MAU까지 무료로 제공합니다.

기존에 S3에 파일 형태로 저장하던 데이터를 Supabase PostgreSQL로 옮겼습니다. 파일 시스템 대신 정형화된 스키마로 관리하니 데이터 조회와 필터링이 훨씬 편리해졌습니다.

### Vercel

Vercel은 Next.js 프론트엔드를 배포하기에 최적화된 플랫폼입니다. GitHub에 코드를 푸시하면 자동으로 빌드·배포되고, Serverless Functions와 Edge Functions도 Free Tier에서 사용할 수 있습니다.

Vercel Cron Jobs를 활용해 기존에 AWS EventBridge + Lambda로 처리하던 주기적 크롤링 스케줄링을 대체했습니다.

### AWS Route 53

도메인(dig-em.com) 관리는 Route 53을 계속 사용합니다. 도메인 비용은 연간 고정이라 월별 추가 비용이 발생하지 않습니다.

## 전환 결과

| 항목 | Step 2 | Step 3 |
|---|---|---|
| DB | S3 (파일 저장) | Supabase (PostgreSQL) |
| 프론트엔드 | - | Vercel (Next.js) |
| 크롤링 스케줄러 | AWS EventBridge | Vercel Cron Jobs |
| 월 운영비 | 소액 발생 | **0원** |

## FinOps 관점에서

AWS는 강력하지만, 개인 프로젝트에서 모든 것을 AWS로 해결하려 하면 비용 구조가 복잡해집니다. 워크로드의 규모와 사용 패턴에 맞는 플랫폼을 조합하는 것이 중요합니다.

이 프로젝트를 통해 배운 것은 **"AWS가 항상 정답이 아니다"** 라는 것입니다. Route 53처럼 AWS가 잘하는 영역(도메인 관리, 안정성)은 유지하고, DB와 배포처럼 Free Tier가 충분한 영역은 전문 플랫폼에 위임하는 하이브리드 전략이 개인 프로젝트에서는 훨씬 실용적이었습니다.

---

# 다음 편에서는

이 서비스의 핵심 기능인 AI 로컬라이징 파이프라인을 다룹니다. Gemini API로 영문 음악 평론을 자동 번역하고 아카이빙하는 전체 구조를 설명합니다.
