---
id: 20250509-learning-database-03
title: JOIN 활용과 데이터 모델링
date: 2025-05-09
category: learning
subCategory: Database
---
## 1. JOIN (테이블 결합)
> 데이터가 여러 테이블에 흩어져 있을 때, 이를 가로 방향으로 합쳐서 한 번에 조회하는 연산.

### 1.1 주요 JOIN 방식
* **EQUI JOIN (등가 조인)**: 두 테이블에서 공통된 의미를 가진 컬럼의 값이 정확히 일치하는 데이터만 합친다. 가장 일반적으로 사용되는 방식이다.
* **NON EQUI JOIN**: `=` 연산자가 아닌 `BETWEEN`, `>`, `<` 등의 연산자를 사용하여 조인한다. 예를 들어 급여 수치를 기준으로 급여 등급 테이블과 매칭할 때 사용한다.
* **SELF JOIN**: 하나의 테이블을 두 번 불러와서 조인한다. 사원 테이블에서 '사원의 이름'과 '그 사원의 관리자 이름'을 한 줄에 보고 싶을 때처럼, 자기 참조가 필요한 경우에 활용한다. 이때는 반드시 테이블에 별명을 붙여 구분해야 한다.
* **OUTER JOIN (외부 조인)**: 조인 조건에 맞지 않아 버려지는 데이터까지 포함하여 조회한다.
    - **LEFT OUTER JOIN**: 왼쪽 테이블의 데이터는 조건에 맞지 않아도 무조건 출력한다.
    - **FULL OUTER JOIN**: 양쪽 테이블의 모든 데이터를 출력한다. (MariaDB는 이를 직접 지원하지 않아 합집합 연산인 UNION을 사용하여 구현한다.)

#### 예제
```
EMP: 사원명, 부서번호(DEPTNO), 급여(SAL), 관리자번호(MGR_ID)
DEPT: 부서번호(DEPTNO), 부서명
SAL_GRADE: 등급, 최소급여, 최대급여
```

- EQUI JOIN (등가 조인): 사원명과 그 사원이 속한 부서명을 함께 조회합.

``` SQL
SELECT E.ENAME, D.DNAME
FROM EMP E
JOIN DEPT D ON E.DEPTNO = D.DEPTNO;
```

- NON EQUI JOIN (비등가 조인): 사원의 급여가 급여등급 테이블의 어느 범위에 속하는지 확인하여 등급을 조회.

``` SQL
SELECT E.ENAME, E.SAL, S.GRADE
FROM EMP E
JOIN SAL_GRADE S ON E.SAL BETWEEN S.MIN_SAL AND S.MAX_SAL;
```

- SELF JOIN (셀프 조인): 사원 테이블을 두 번 사용하여 사원 이름과 해당 사원의 관리자 이름을 조회.

``` SQL
SELECT E1.ENAME AS "사원명", E2.ENAME AS "관리자명"
FROM EMP E1
LEFT JOIN EMP E2 ON E1.MGR_ID = E2.EMPNO;
```

- OUTER JOIN (외부 조인): 부서원이 없는 부서 정보까지 모두 포함하여 조회.

``` SQL
-- 모든 사원을 출력하며, 부서가 배정되지 않은 사원도 포함
SELECT E.ENAME, D.DNAME
FROM EMP E
LEFT OUTER JOIN DEPT D ON E.DEPTNO = D.DEPTNO;
FULL OUTER JOIN (MariaDB/MySQL 방식)
```

#### ANSI 표준 JOIN 문법
표준 SQL 문법을 사용하면 가독성이 좋아진다.
* **INNER JOIN**: `FROM 테이블1 INNER JOIN 테이블2 ON 조인조건` 형식으로 작성한다.
* **NATURAL JOIN**: 조인할 두 테이블의 컬럼 이름이 완전히 같을 때, 조건을 생략하고 자동으로 연결한다.

### 1.2 DDL과 데이터베이스 설계
테이블을 만들 때 발생할 수 있는 문제를 방지하기 위해 체계적인 설계가 필요하다.

#### ① 이상 현상 (Anomaly)
잘못된 설계로 인해 데이터 중복이 발생하면 다음과 같은 문제가 생긴다.
* **삽입 이상**: 데이터를 넣고 싶은데 불필요한 정보까지 함께 넣어야 하거나, 넣지 못하는 현상.
* **삭제 이상**: 특정 정보를 지울 때 지워지면 안 되는 유용한 정보까지 함께 삭제되는 현상.
* **변경 이상**: 데이터를 수정할 때 미처 변경하지 못한 부분이 생기는 현상.

#### ② 정규화 (Normalization)
데이터의 중복을 최소화하고 유연한 구조를 만들기 위해 테이블을 분해하는 과정이다. 굉장히 다양하지만 일단 3NF까지만 설명.
* **제1정규형(1NF)**: 모든 칸에는 하나의 값(원자값)만 들어있어야 한다.

| 주문번호 (PK) | 고객명 | 주문상품 |
| :--- | :--- | :--- |
| 101 | 김철수 | 사과, 포도 |

* **제2정규형(2NF)**: 기본키의 일부분에만 의존하는 속성을 분리한다. (부분 함수적 종속 제거)

| 주문번호 (PK) | 상품ID (PK) | 주문수량 | 상품명 |
| :--- | :--- | :--- | :--- |
| 101 | P001 | 2 | 사과 |

* **제3정규형(3NF)**: 기본키가 아닌 컬럼들끼리 서로 의존하는 관계를 분리한다. (이행적 함수적 종속 제거)

| 주문번호 (PK) | 고객번호 | 등급 |
| :--- | :--- | :--- |
| 101 | C01 | Gold |

#### ③ 반 정규화 (De-normalization)
정규화를 너무 많이 하면 조회할 때마다 수많은 조인이 발생해 성능이 떨어짐. 이를 해결하기 위해 의도적으로 테이블을 합치거나 중복 데이터를 추가하여 성능을 높이는 기법이다.

---

## 3. 테이블 관리 명령어
테이블을 생성하고 구조를 변경하는 핵심 명령어다.

* **테이블 생성 (CREATE)**: `CREATE TABLE` 뒤에 컬럼명과 자료형, 제약 조건을 나열한다.
    - **CHAR vs VARCHAR**: CHAR는 고정된 공간을 차지하고, VARCHAR는 데이터 크기에 따라 효율적으로 공간을 조절한다.
* **테이블 수정 (ALTER)**: 
    - **컬럼 추가**: `ADD` 명령어를 사용한다.
    - **컬럼 삭제**: `DROP` 명령어를 사용한다.
    - **컬럼 수정**: 이름과 타입을 바꿀 때는 `CHANGE`, 타입만 바꿀 때는 `MODIFY`를 쓴다.
* **테이블 삭제 (DROP vs TRUNCATE)**: 
    - **DROP**: 테이블 자체를 아예 없애버린다.
    - **TRUNCATE**: 테이블의 틀은 남겨두고 안의 데이터만 전체 삭제한다.

---

## 4. 제약 조건 (Constraints)
데이터의 정확성과 신뢰성을 지키기 위한 규칙이다.

* **NOT NULL**: 데이터를 반드시 입력해야 한다.
* **UNIQUE**: 중복된 값을 허용하지 않는다. (단, NULL은 여러 개 들어갈 수 있다.)
* **CHECK**: 들어오는 데이터의 값을 검사한다. (예: 성별은 '남' 또는 '여'만 가능.)
* **PRIMARY KEY (기본키)**: 데이터를 유일하게 식별하는 키로, `NOT NULL`과 `UNIQUE`의 성격을 모두 가진다. 테이블당 하나만 설정 가능하다.
* **FOREIGN KEY (외래키)**: 다른 테이블을 참조하는 연결 고리다.
    - **옵션**: `ON DELETE CASCADE`를 설정하면 부모 테이블의 데이터가 삭제될 때 이를 참조하던 자식 데이터도 자동으로 함께 삭제된다.

``` sql
-- 부모 테이블: 부서 (DEPT)
CREATE TABLE DEPT (
    DEPTNO INT PRIMARY KEY,         -- PRIMARY KEY: 중복 불가, 빈 값 불가
    DNAME VARCHAR(20) NOT NULL      -- NOT NULL: 부서명 필수 입력
);

-- 자식 테이블: 사원 (EMP)
CREATE TABLE EMP (
    EMP_ID INT PRIMARY KEY,         -- PRIMARY KEY: 사원 식별자
    EMAIL VARCHAR(50) UNIQUE,       -- UNIQUE: 이메일 중복 불가 (단, NULL 허용)
    GENDER CHAR(1) CHECK (GENDER IN ('M', 'F')), -- CHECK: M 또는 F만 입력 가능
    DEPTNO INT,
    
    -- FOREIGN KEY: DEPT 테이블의 DEPTNO를 참조
    -- ON DELETE CASCADE: 부서가 사라지면 소속 사원 정보도 자동 삭제
    FOREIGN KEY (DEPTNO) REFERENCES DEPT(DEPTNO) ON DELETE CASCADE
);
```
