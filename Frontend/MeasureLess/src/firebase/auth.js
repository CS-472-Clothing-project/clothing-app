import { auth } from "./firebase.js";
import { createUserWithEmailAndPassword, GoogleAuthProvider, signInWithEmailAndPassword, signInWithPopup, signInAnonymously } from "firebase/auth"

// email register
export const doCreateUserWithEmailAndPassword = async (email, password) => {
    return createUserWithEmailAndPassword(auth, email, password);
};

// email sign in
export const doSignInWithEmailAndPassword = async (email, password) => {
    return signInWithEmailAndPassword(auth, email, password);
};

// Google signin
export const doSignInWithGoogle = async () => {
    const provider = new GoogleAuthProvider();
    const result = await signInWithPopup(auth, provider);
    // save user info in fire store
    // todo

    return result;
};

// Guest Login
export const doSignInAnonymously = async () => {
    return signInAnonymously(auth);
};


export const doSignOut = () => {
  return auth.signOut();
};

