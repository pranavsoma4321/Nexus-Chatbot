// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-analytics.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { getFirestore, doc, setDoc, getDoc } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDYlgdPz-BfimEy0AzctOuOxIl6oaxeDFg",
  authDomain: "chatbot-51009.firebaseapp.com",
  databaseURL: "https://chatbot-51009-default-rtdb.firebaseio.com",
  projectId: "chatbot-51009",
  storageBucket: "chatbot-51009.firebasestorage.app",
  messagingSenderId: "732513092097",
  appId: "1:732513092097:web:e6911eef3b895bec7c7600",
  measurementId: "G-LMCB9F1F49"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const db = getFirestore(app);

// Export Firebase services
export { auth, db, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged, doc, setDoc, getDoc };
