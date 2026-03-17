---
id: learning-database-04
title: "MariaDB 제약 조건과 MongoDB 기초"
date: "2025-05-12"
category: "learning"
subCategory: ["Database", "MongoDB"]
---

## 1. MariaDB 제약 조건 관리
데이터의 무결성을 보장하기 위해 테이블에 설정하는 규칙들을 관리하는 방법이다.

* **제약 조건 확인**: `information_schema.table_constraints` 테이블을 조회하여 현재 설정된 모든 제약 조건을 확인할 수 있다.
* **제약 조건 수정 및 추가**: `ALTER TABLE` 문을 사용한다. `MODIFY`는 기존 컬럼의 제약 조건을 변경할 때, `ADD`는 새로운 제약 조건을 추가할 때 사용한다.
* **제약 조건 삭제**: `DROP CONSTRAINT` 명령어를 사용한다. 제약 조건 생성 시 이름을 지정하지 않으면 DB가 임의로 이름을 부여하므로, 생성 시 `CONSTRAINT [이름]` 형식을 사용하는 것이 유지보수에 좋다.
* **기본값(Default)**: 값을 입력하지 않았을 때 자동으로 채워지는 값이다. `DEFAULT` 키워드로 설정하며, 삽입 시 해당 컬럼을 제외하거나 직접 `DEFAULT`를 명시하여 입력할 수 있다.

## 2. MongoDB 개요 및 특징
MongoDB는 스키마가 없는(Schema-less) 도큐먼트 지향 NoSQL 데이터베이스다.

* **주요 특징**:
    - **가벼움(Light Weight)**: 구조가 단순하여 설정과 운영이 상대적으로 가볍다.
    - **빠른 조회**: C언어의 Primitive 타입을 기반으로 데이터를 처리하며, BSON(Binary JSON) 형식을 사용해 검색 속도가 빠르다.
* **데이터 타입**: Double, String, Object, Array, Binary Data, Boolean, Date, Null 등을 지원한다.
* **ObjectID**: 데이터를 구분하기 위한 12바이트 바이너리 데이터로, `_id` 필드에 기본적으로 사용된다.

## 3. MongoDB 구조 이해
관계형 데이터베이스(RDBMS)와 대응되는 물리적 개념을 이해하는 것이 중요하다.

* **Database**: 서비스나 데이터 그룹을 나누는 물리적 단위다. 데이터베이스 수준에서 잠금(Lock)이 적용될 수 있어 성능에 영향을 미친다. `use [DB이름]` 명령어로 선택하며, 없으면 새로 생성된다.
* **Collection**: RDBMS의 '테이블'에 해당한다. MongoDB는 조인(JOIN)을 지원하지 않으므로 하나의 컬렉션에 데이터를 모으는 것이 유리할 수 있지만, 너무 커지면 메모리 효율이 떨어지므로 적절히 나누어 저장하는 것이 권장된다.
* **Document**: RDBMS의 '행(Row)'에 해당하며, 실제 데이터가 저장되는 단위다.

## 4. 데이터베이스 및 컬렉션 관리 명령
* **현재 DB 확인**: `db`
* **현재 DB 삭제**: `db.dropDatabase()`
* **컬렉션 정보 조회**: `db.getCollectionInfos()`
* **서버 및 통계 확인**: `db.serverStatus()`, `db.stats()`