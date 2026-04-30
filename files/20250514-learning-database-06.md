---
id: 20250514-learning-database-06
title: PyMongo 가이드
date: 2025-05-14
category: learning
subCategory:
  - Database
  - Python
---
# 1. Python MongoDB 연동
## 1.1 연동 개요
Python에서 DB를 연동하는 방식을 크게 두 개로 나뉨
- 드라이버(패키지) 직접 설치해 제어
  - MongoDB의 경우 `pymongo` 패키지 사용.
- ORM(Django, SQLAlchemy 등) 프레임워크를 사용

## 1.2 PyMongo
PyMongo는 파이썬에서 MongoDB를 쓸 수 있게 해주는 도구로, 파이썬의 간결함과 MongoDB의 유연함을 모두 갖춘 패키지.
- 별도 변환 과정 없이 딕셔너리와 리스트를 그대로 DB에 집어넣고 꺼낼 수 있다.
- 동적 스키마를 지원한다 (테이블 구조를 마음대로 넣어도 괜찮음)
- BSON 자동 변환 기능
- 커서 기반 조회
  - 실제로 데이터가 필요한 시점까지 통신을 늦춰 효율을 극대화하는 **지연 실행**을 지향
- PyMongo는 MongoClient 객체를 생성할 때 커넥션 풀을 자동으로 만들어 준다. Redis의 경우 `redis-py` 드라이버가 커넥션 풀 지원. 사실 대부분이 커넥션 풀을 지원하지만, PyMongo가 강력한 편. 
  - 이 덕분에 스레드로부터 안전함. 요즘 컴퓨터는 멀티 코어를 사용하기에 멀티 스레드가 기본인데, MongoDB는 **커넥션 풀과 잠금 매커니즘을 통해 여러 명이 동시에 같은 데이터를 건드려도 꼬이거나 망가지지 않게 안전 유지가 가능함**.
    - 어떻게? 각 스레드가 서로 간섭하지 않게 차례대로 or 독립된 통로로 데이터를 보내줌.
  - 웹 서버(Flask, Django, FastAPI) 환경에서 별도 복잡한 설정 없이 바로 사용하기 좋다.
- 다만 비동기 처리를 지원하지 않는다. 만약 `async/await` 방식을 쓰고 싶다면 `Motor`라는 별도 라이브러리를 사용해야 함.

### 커넥션 풀이란?
DB 연결 작업은 사실 굉장히 비싸고 무거운 작업임. 매번 필요시마다 연결을 생성해서 인증하고 데이터를 처리한 다음 연결을 종료하는 과정을 거친다면 서버가 금방 지친다. 그래서 미리 연결 통로를 만들어 수영장(Pool)에 띄워두고 필요할 때마다 꺼내 쓰고 다시 넣어두는 방식을 사용. 
- MongoClient 생성 → 내부적을호 여러 소켓 연결을 미리 맺어둠
- 스레드 A가 데이터를 저장해달라 요청하면 통제실은 Pool에서 놀고 있는 Idle 연결 하나를 꺼내 빌려줌.
- 스레드 A가 쓰는 동안 스레드 B가 그 통로를 쓰지 않도록 통제실이 제어함. 다른 연결을 받거나 잠시 대기.

### 잠금 매커니즘
PyMongo는 데이터 수정하는 아주 짧은 찰나에 잠금을 검. 이를 통해 동시에 두 명에게 같은 연결을 빌려주는 사고를 원천 봉쇄.

## 1.3 MongoDB 실습
``` python
from pymongo import MongoClient

# 1. 서버 접속 및 마트 DB 연결
con = MongoClient('127.0.0.1', 27017)
db = con.mart_db      # 마트 데이터베이스
products = db.products # 상품 컬렉션

# 2. 데이터 삽입 (비정형 데이터의 유연함)
products.insert_one({
    'name': '새우깡', 
    'price': 1500, 
    'category': '과자',
    'detail': {'weight': '120g', 'vendor': '농심'}
})

products.insert_many([
    {'name': '카스', 'price': 2500, 'category': '주류', 'info': {'abv': '4.5%'}},
    {'name': 'C타입 충전기', 'price': 8000, 'category': '생활용품', 'warranty': '1년'}
])

# 3. 가격이 5000원 이상인 프리미엄 상품 조회
print("--- 5000원 이상 상품 목록 ---")
cursor = products.find({'price': {'$gte': 5000}})
for item in cursor:
    print(f"상품명: {item['name']}, 가격: {item['price']}")

# 4. 재고 정리 (5000원 이상 상품 일괄 삭제)
products.delete_many({'price': {'$gte': 5000}})
```

보면 상품군마다 다른 정보를 자유롭게 담을 수 있다. 

## 1.4 MariaDB 실습

```
import pymysql

# 1. 마트 시스템 접속
con = pymysql.connect(
    host='127.0.0.1', port=3306, user='root', 
    passwd='password', db='mart_system', charset='utf8mb4'
)
cursor = con.cursor()

# 2. 신규 회원 등록 (Prepared Statement로 보안 강화)
# 회원아이디, 성함, 생년, 지역, 연락처, 가입일
sql = "INSERT INTO membertbl VALUES(%s, %s, %s, %s, %s, %s)"
member_data = ('mart_king', '강감찬', 1985, '서울', '010-1111-2222', '2026-04-28')

try:
    cursor.execute(sql, member_data)
    # RDBMS는 확정(Commit) 절차가 생명입니다!
    con.commit()
    print("회원 등록 완료")
except Exception as e:
    con.rollback() # 에러 시 되돌리기
    print(f"등록 실패: {e}")

# 3. 전체 회원 명부 조회
print("--- 전체 회원 명부 ---")
cursor.execute("SELECT * FROM membertbl")

# fetchall()로 모든 데이터를 가져와서 순회
datas = cursor.fetchall()
for data in datas:
    print(f"아이디: {data[0]}, 이름: {data[1]}, 가입지: {data[3]}")

# 연결 종료 (실무자의 매너)
con.close()
```

SQL 문에서 `%s`를 쓰고 `execute`의 두 번째 인자로 튜플을 넘기는 방식을 취하고 있는데, 이는 SQL 인젝션을 막기 위함. 또한 try-except 구조를 통해 결제가 실패하면 데이터를 다시 되돌리는 로직을 볼 수 있다.

## 1.5 프로시저와 BLOB
- 프로시저: DB 안에 이미 일련의 실행 코드 뭉치를 저장해두는 방식. 파이썬에서  함수를 만드는 것과 비슷하다 (근데 그 코드가 DB 안에 살고 있는 개념)
  - 만약 매일 밤 9시마다 모든 신선식품 가격을 30% 할인하고 재고를 체크해야 하는 복잡한 로직이 있다고 칠 때, 프로시저를 쓰지 않으면 `SELECT`를 가져와 계산하고 다시 `UPDATE` 쿼리를 수십 번 날려야 한다. 하지만 프로시저를 사용하면 `apply_night_sale()` 같은 코드 하나 저장해두고 `callproc('apply_night_sale')` 이런 식으로 한 줄만 보내면 모든 처리가 끝남.
- BLOB(Binary Large Object): 이진 데이터로 된 큰 덩어리. 일반적인 텍스트가 아니라 사진, 오디오, 비디오, PDF 등의 파일 데이터를 그대로 DB 칸에 집어넣을 때 사용한다.
  - 이미지를 DB에 직접 넣는 방식은 대체로 DB 용량이 커져 성능이 저하되는 편. 사실 실무에서는 BLOB 방식보다 이미지는 클라우드 저장소(S3 등)에 올리고, DB에는 주소(URL)만 저장하는 식을 더 선호한다.

``` python
# 'rb' (Read Binary) 모드가 핵심!
with open('apple_photo.jpg', 'rb') as f:
    photo_data = f.read() # 이미지 파일을 이진 데이터로 읽음
    
# DB에 삽입
sql = "INSERT INTO product_photos (p_id, photo) VALUES (%s, %s)"
cursor.execute(sql, (101, photo_data))
con.commit()
```
