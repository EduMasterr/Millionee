// Firebase Configuration and Initialization
const firebaseConfig = {
    apiKey: "AIzaSyCZu1z-QNPaV6coFAXg9MwU0gvWcI_tM5E",
    authDomain: "million-journey-5ae07.firebaseapp.com",
    databaseURL: "https://million-journey-5ae07-default-rtdb.firebaseio.com", // Usually required for Realtime DB
    projectId: "million-journey-5ae07",
    storageBucket: "million-journey-5ae07.firebasestorage.app",
    messagingSenderId: "730981110023",
    appId: "1:730981110023:web:9bebe4dcb6446c8fbc35a2"
};

// Initialize Firebase only if it hasn't been initialized yet
if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
}

// Global database reference
const db = firebase.database();
