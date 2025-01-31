
  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-app.js";
  import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-analytics.js";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyA153OlUfWZGZH3N4542M5UseOVBY415So",
    authDomain: "cacaolink-8ed4a.firebaseapp.com",
    projectId: "cacaolink-8ed4a",
    storageBucket: "cacaolink-8ed4a.firebasestorage.app",
    messagingSenderId: "1081530669031",
    appId: "1:1081530669031:web:f59b97c4781642f9c84f42",
    measurementId: "G-3ZRRTS5N4F"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const analytics = getAnalytics(app);
