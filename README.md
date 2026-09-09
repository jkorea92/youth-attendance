# 퍼스백양장로교회 청년부 온라인 출석체크

GitHub Pages + Firebase Authentication + Cloud Firestore 기반의 청년부 출석관리 웹앱입니다.

## 기능
- 관리자/셀리더 이메일 로그인
- 셀 이름, 리더, 헬퍼, 셀원 관리
- 날짜별 출석/지각/결석
- 여러 기기 실시간 동기화
- 전체/셀별 최근 출석률
- Excel용 CSV 다운로드

## Firebase 연결
1. Firebase Console에서 프로젝트를 생성합니다.
2. Authentication > Sign-in method에서 Email/Password를 활성화합니다.
3. Authentication > Users에서 사용할 계정을 생성합니다.
4. Firestore Database를 생성합니다.
5. Firestore > Rules에서 이 저장소의 `firestore.rules` 내용을 적용합니다.
6. Project settings > General > Your apps > Web app을 등록합니다.
7. 표시되는 `firebaseConfig` 값을 이 저장소의 `firebase-config.js`에 입력합니다.

## GitHub Pages
Repository Settings > Pages에서 `Deploy from a branch`, `main`, `/ (root)`를 선택하면 됩니다.

예상 주소: `https://jkorea92.github.io/youth-attendance/`

> 실제 출석 데이터는 GitHub가 아니라 Firestore에 저장됩니다. 비로그인 접근은 Firestore Security Rules로 차단합니다.
