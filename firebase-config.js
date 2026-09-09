// Firebase Console > Project settings > Your apps > Web app에서 받은 설정값으로 교체하세요.
// Firebase 웹 API 키 자체는 비밀키가 아닙니다. 실제 데이터 접근은 Authentication + Firestore Rules로 보호합니다.
export const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.firebasestorage.app",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};
