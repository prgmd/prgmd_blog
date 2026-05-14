---
id: 20250901-learning-restapi-01
title: REST API
date: 2025-09-01
category: learning
subCategory: []
---
## 1. REST API
### 1.1 API란?
> Application Programming Interface. 두 소프트웨어가 서로 **통신**할 수 있게 하는 **메커니즘**.

클라이언트와 서버처럼 서로 다른 프로그램에서 정보를 요청하거나 응답할 때, 서로 이해할 수 있는 공통된 규칙과 형식이 필요한데, 이 역할을 하는 것이 바로 API다. 

현대 웹 개발은 직접 모든 것을 개발하기보다 누구나 접근할 수 있도록 공개된 여러 **Open API**를 활용하는 추세. YouTube, Google Map, Naver Papago, Kakao Map 등이 대표적인 Third Party Open API다. 

#### Third Party
직접 개발하지 않은 외부 서비스나 소프트웨어를 제공하거나 활용하는 주체.

#### 예시
스마트폰 날씨 앱에서 기상청 서버의 기상 데이터를 필요로 할 때, 기상청 서버에 작성된 '지정된 형식(API 매뉴얼)'이 있고 형식에 맞춰 요청하면 정보를 주는 시스템.

#### API 사용 이유
- 바퀴를 다시 발명할 필요 없다 = 모든 기능을 직접 처음부터 개발할 필요가 없음. 이미 잘 만들어진 기능을 가져다 쓰기만 하면 됨.
- 정의된 입력값만 넣으면 원하는 결과를 얻음. 내부 로직은 몰라도 됨.
- 서로 다른 프로그래밍 언어도 공통 규격 사용 가능.
- API가 허용한 특정 데이터와 기능만 접근할 수 있도록 제한 가능.
  - 또한 누가, 언제, 얼마나 데이터를 가져가는지 통제할 수 있음. 

---

## 2. REST API
### 2.1 REST란?
> Representational State Transfer. API Server를 개발하기 위한 일종의 **소프트웨어 설계 방법론**. (꼭 지켜야 하는 건 아니다. 그저 **누구나 예측 가능한 방식**으로 통신할 수 있도록 API 설계 기준을 제안한 것)

프로젝트의 상황이나 팀의 규모에 따라 REST의 원칙 중 일부만 채택하거나, 상황에 맞게 변형해서 사용하는 경우도 많다. (오히려 전부 지키는 게 비효율적일 때가 많음) REST 원리를 따르는 시스템을 **RESTful** 하다고 부름.

### 2.2 REST API
API를 RESTful하게 적는 방법은 3가지만 기억하면 된다. 이 3가지만 잘 지켜도 RESTful하다는 평가를 받음. (더 들어가면 Stateless, Cacheable 등이 있음)

1. 식별 (뭐 다룰거임?) → **URI**
2. 행위 (어떻게 다룰 거?) → **HTTP Methods**
3. 표현 (어떤 형식으로 주고 받을 거?) → **JSON**

### 2.3 URI
> 통합 자원 식별자. 인터넷에서 **리소스(자원)를 식별하는 문자열**을 의미한다. 대표적으로는 URL이 있음.

#### 자원
웹에서 고유한 주소를 통해 접근할 수 있는 데이터, 혹은 기능의 대상. 모든 자원은 고유한 이름(주소)를 가진다.
- 설계 원칙은 '**명사를 사용하며, 계층 구조를 가지는 것**'
  - `/movies` (영화 목록), `/movies/1` (1번 영화)

### 2.4 URL
통합 자원 위치. 웹에서 주어진 **리소스의 주소**. 네트워크상 리소스가 어디에 있는지 알려주기 위한 약속이다.

`http://www.example.com:80/path/to/myfile.html?key1=value1&key2=value2#SomewhereInTheDocument`

#### ① Schema (or Protocol)
브라우저가 리소스를 요청하는 데 사용해야 하는 규약. URL의 첫 부분은 **브라우저가 어떤 규약을 사용하는지를 나타낸다**. 기본적으로 웹은 http(s)를 요구한다. (물론 `mailto:` (메일), `ftp:` (파일 전송) 등 다른 프로토콜도 존재)

#### ② Domain Name
요청 중인 웹 서버. 주로 도메인 이름을 사용. (예: `google.com`의 IP는 `142.251.42.142`)

#### ③ Port
웹 서버의 리소스에 접근하는 데 사용되는 기술적인 문(Gate).
- **표준 포트만 작성 시 생략 가능**. (표준 포트: HTTP - 80 / HTTPS - 443. 그래서 `https://google.com`인 이유) 

#### ④ Path
웹 서버의 리소스 경로. 초기에는 실제 파일의 물리적 위치를 나타냈으나, 오늘날은 **실제 위치가 아닌 추상화된 형태의 구조를 표현**. (예: `/articles/create/`가 실제 폴더 구조를 의미하지는 않음)

#### ⑤ Parameters
웹 서버에 제공하는 추가 데이터. `?` 이후 시작되는 구문이며, 그 뒤로 파라미터가 추가될 때마다 `&` 기호로 이어 붙이는 key-value 쌍 목록이다. 서버는 리소스를 응답하기 전에 이 파라미터를 사용하여 추가 작업을 수행할 수 있습니다.

#### ⑥ Anchor
일종의 '북마크'. 브라우저 해당 지점에 있는 콘텐츠를 표시한다. 브라우저가 페이지 내의 특정 지점으로 이동할 수 있도록 돕는 역할을 한다. `#` (fragment identifier, 부분 식별자) 이후 부분은 서버에 전송되지 않는다. 

### 2.4 HTTP Methods = CRUD
리소스에 대해 수행하려는 동작을 정의하는 과정이다.
- 이 주소로 물건 좀 보내주세요 → **POST**
- 방금 보낸 물건 도착했나요? → **GET**
- 그 물건 취소할게요 → **DELETE**
- 받는 사람 전화번호 바뀌었어요 → **PUT**

#### 주요 종류
- **GET:** 리소스 표현 요청 (데이터 검색용)
- **POST:** 데이터를 지정된 리소스에 제출해 **서버 상태 변경**
- **PUT:** 요청한 주소의 리소스 수정 (전체 교체)
- **DELETE:** 지정된 리소스 삭제

#### HTTP Response Status Codes
> 특정 HTTP 요청이 **성공적으로 완료되었는지 여부**를 숫자로 나타낸 신호. 클라이언트는 이 코드를 보고 서버에서 어떤 일이 일어났는지 판단한다. 

* **100-199 (Informational):** 요청 계속 진행 중 (중간 응답)
* **200-299 (Successful):** 정상 처리 완료
* **300-399 (Redirection):** 요청한 리소스가 다른 위치로 옮겨짐
* **400-499 (Client error):** **클라이언트 요청에 문제가 있음**
* **500-599 (Server error):** **서버 내 문제가 있음. 요청 처리 실패**

### 2.5 JSON
> JavaScript Object Notation. 데이터를 **구조화된 텍스트 형태**로 표현하는 형식으로, 어떤 클라이언트와도 **언어와 플랫폼에 독립적으로 통신할 수 있게 해준다.**

- 과거에는 XML을 많이 썼으나, 현재 REST API의 표준은 JSON.
- 텍스트 기반이며 가볍고, 사람이 읽기 쉬우며 대부분의 프로그래밍 언어에서 처리가 쉽다.

#### 응답 데이터 타입의 변화의 역사
- 전통적 방식 (MTV 구조)
  - Django 서버가 직접 템플릿을 렌더링한 **HTML** 페이지를 반환.
  - 클라이언트는 화면(View)이 완성된 상태의 데이터를 받는다.
- **현대적 방식 (Front-end/Back-end 분리)**
  - Django는 더 이상 화면을 그리지 않고, 오직 데이터(**JSON**)만을 응답하는 **API 서버**로 역할이 변함.
  - 화면은 **Vue**나 **React** 같은 Front-end Framework가 전담.
  - HTML 대신 JSON 데이터만 전달 → 응답 용량이 줄어들고 처리 속도가 빨라짐.

#### Python으로 JSON 데이터 처리하기

```python
import requests
from pprint import pprint

response = requests.get('데이터 링크')

# json을 python 타입으로 변환
result = response.json()
pprint(result)
```

- **migrate**: 모델 구조를 데이터베이스에 반영하는 명령어
- **fixtures**: 초기 데이터를 자동으로 불러오기 위한 JSON 형식의 데이터 파일

---

## 3. DRF

### 3.1 DRF(Django REST framework)
> Django에서 RESTful API 서버를 쉽게 구축할 수 있도록 도와주는 **오픈소스 라이브러리**.

일종의 **조립식 가구**. 가구를 직접 만들려면 톱, 망치, 설계도 등 많은 재료가 필요하지만, 조립식 가구는 드라이버 하나만 있으면 되기 때문. 복잡한 API 서버 개발 과정을 표준화하고 자동화하여, 초보자도 빠르고 안정적으로 RESTful 구조를 구현할 수 있도록 도와주는 개발 도구 세트다.

### 3.2 Postman
> API 개발 및 테스트를 위한 서비스. 요청 데이터 구성, 응답 확인, 환경 설정, 자동화 테스트 등 다양한 기능을 제공한다.

- [Postman 다운로드 페이지](https://www.postman.com/downloads/)에서 자기 OS에 맞는 버전 설치.
- 'My Workspace'를 선택해 작업 공간 확보.

![](https://velog.velcdn.com/images/paramad/post/42415a4c-ba11-45cb-8f5f-b3532119b6ba/image.png)

#### 화면 구성
- **상단(빨간 영역):** 요청 URL 작성 (HTTP Method 선택 및 주소 입력)
- **중간(주황 영역):** 요청 시 필요한 데이터 작성 (Params, Body 등)
- **하단(초록 영역):** 응답 결과 출력 화면 (Status Code, JSON 결과 확인)

### 3.3 Serializer
> 데이터 구조나 객체 상태를 어떠한 언어나 환경에서도 다시 쉽게 사용할 수 있도록 **재구성 가능한 포맷으로 변환하는 과정**. JSON으로의 변환이 대표적.

#### 구조
* **Serializer Class 담당:** 데이터 구조나 객체 상태를 나중에 재구성할 수 있는 포맷(Serialized data)으로 변환하는 과정을 담당합니다. 프로젝트 내에 `serializers.py` 파일을 생성하여 작성합니다.
* **Serializer:** 직렬화 수행 로직을 담은 클래스. 단순한 포맷 변환 도구가 아닌, **값 검증, 데이터 구조 정의, 모델 연동**까지 담당하는 핵심 계층이다.
* **ModelSerializer:** Django 모델과 연결된 Serializer 클래스. 일반 Serializer와 달리 사용자 입력 데이터를 받아 **자동으로 모델 필드에 맞춰** Serialization을 진행한다.

####  ModelSerializer class 사용 예시
게시글 데이터 목록을 제공하기 위해 `Article` 모델을 토대로 직렬화를 수행하는 `ArticleSerializer` 예시. 참고로 `serializers.py`의 위치나 파일명은 자유롭게 작성 가능하다.

```python
# articles/serializers.py
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

```
