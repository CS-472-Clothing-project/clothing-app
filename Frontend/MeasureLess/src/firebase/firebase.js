// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyDYfVmwx8D_lVO4W-yz6Ppt7oVNlffBIBg",
    authDomain: "measureless472.firebaseapp.com",
    projectId: "measureless472",
    storageBucket: "measureless472.firebasestorage.app",
    messagingSenderId: "689270413054",
    appId: "1:689270413054:web:9e4057e4b03d2ab00eb7af",
    measurementId: "G-L75RR0LWKF"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { app, auth , db};