# **영화 별점 예측 서비스**

> Neural Collaborative Filtering 기반 영화 추천 모델을 FastAPI로 서빙하고 웹 UI로 시각화한 프로젝트

![Python](https://img.shields.io/badge/Python-3.12-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green) ![PyTorch](https://img.shields.io/badge/PyTorch-2.2-red) ![Docker](https://img.shields.io/badge/Docker-ready-blue)

---

## 프로젝트 소개

유저 ID와 영화 ID를 입력하면 딥러닝 모델이 예상 별점(0~5)을 예측해주는 웹 서비스입니다.

단순한 모델 실험에서 끝내지 않고, **실제 서비스처럼 API 서버와 UI까지 연결**하는 전체 파이프라인을 구축하는 것을 목표로 했습니다.  

오류 발생 시 환경 문제인지 코드 문제인지를 먼저 분리하여 판단하는 방식으로 문제를 해결하며 배포까지 완성했습니다.  

---

## 서비스 화면

> `localhost:8000` 접속 시 나타나는 UI
> <img width="1568" height="728" alt="image" src="https://github.com/user-attachments/assets/16885aa3-2acd-4ec1-9174-131da4934df3" />

  
- 유저/영화 ID 입력 → 별점 예측
- 세션 통계 (평균·최고·최저 별점)
- 예측 히스토리 (최근 30건)
- 모델 구조 정보 표시

---

## 기술 스택

| 분류 | 기술 |
|------|------|
| 모델 | PyTorch, NCF (Neural Collaborative Filtering) |
| 백엔드 | FastAPI, Pydantic, Uvicorn |
| 프론트엔드 | HTML / CSS / Vanilla JS |
| 컨테이너 | Docker |
| 패키지 관리 | Poetry |

---

## 모델 선택 이유 — 왜 NCF인가?

### NCF (Neural Collaborative Filtering) 구조

```
유저 ID ──→ Embedding ──┐
                        ├──→ MLP (32→32) ──→
영화 ID ──→ Embedding ──┘                   ├──→ FC → sigmoid → 별점
                                            │
유저 × 영화 (GMF) ─────────────────────────┘
```

### 선택 이유

기존 Matrix Factorization(MF) 방식은 유저-아이템 관계를 **선형**으로만 모델링합니다. NCF는 MLP를 결합해 **비선형 상호작용**을 포착할 수 있고, 사전 학습된 가중치 파일(`.pth`)을 그대로 불러와 빠르게 서빙할 수 있어 실험 목적에 적합했습니다.

### 모델 하이퍼파라미터

```
Embedding dim : 64
MLP layers    : (32, 32)
Dropout       : 0.2
Users         : 671
Items         : 163,949
Output        : sigmoid × 5 → 0.5 단위 반올림
```

---

## 프로젝트 구조

```
movie_recommendation_part1/
└── app/
    └── src/
        ├── main.py          # FastAPI 앱 진입점 (CORS, Static, Router)
        ├── settings.py      # 환경변수 설정 (pydantic-settings)
        ├── model/
        │   ├── model.py     # NCF 모델 정의 및 가중치 로드
        │   ├── router.py    # /predict/ 엔드포인트
        │   ├── schemas.py   # Request / Response 스키마
        │   └── artifacts/
        │       └── model.pth  # 학습된 가중치 (git 제외)
        └── static/
            └── index.html   # 웹 UI
```

---

## 실행 방법

### 로컬 실행 (Poetry)

```bash
# 1. 의존성 설치
poetry install

# 2. src 폴더로 이동
cd src

# 3. 서버 실행
poetry run python main.py

# 4. 브라우저 접속
# http://localhost:8000
```

### Docker 실행

```bash
# 이미지 빌드
docker build -t cinematch .

# 컨테이너 실행
docker run -p 8000:8000 cinematch

# 브라우저 접속
# http://localhost:8000
```

---

## API 명세

### `POST /predict/`

영화 별점을 예측합니다.

**Request**
```json
{
  "userId": 1,
  "movieId": 318
}
```

**Response**
```json
{
  "userId": 1,
  "movieId": 318,
  "predictedRating": 4.0
}
```

---

## 배운 것 / 회고

### 전체 파이프라인 흐름 이해

```
모델 학습 → 가중치 저장(.pth)
    → FastAPI로 API 서버 구축
    → HTML/JS로 UI 연결
    → Docker로 컨테이너화
    → (다음 단계) 클라우드 배포
```

### 핵심 개념 정리

- **GET vs POST**: GET은 페이지 요청, POST는 데이터를 보내며 처리 요청
- **async/await**: 동시 요청을 효율적으로 처리하기 위한 비동기 처리
- **CORS**: 브라우저가 다른 출처의 API를 호출할 때 필요한 보안 설정
- **StaticFiles**: FastAPI에서 HTML/CSS/JS 같은 정적 파일을 서빙하는 방법
- **Docker**: 실행 환경을 통째로 포장해 어디서든 동일하게 실행 가능하게 함

---

## 다음 목표

- [ ] AWS EC2/ECS 배포 → 공개 URL로 누구나 접속 가능하게
- [ ] LLM 기반 영화 설명/추천 이유 생성 기능 추가
- [ ] 금융 데이터 적용 (신용 리스크, 이상 거래 탐지 등)
- [ ] CI/CD 파이프라인 구축 (GitHub Actions)
