import { auth } from "./firebase.js";
import { createUserWithEmailAndPassword, GoogleAuthProvider, signInWithEmailAndPassword, signInWithPopup } from "firebase/auth"

// email register
export const doCreateUserWithEmailAndPassword = async (email, password) => {
    return createUserWithEmailAndPassword(auth, email, password);
};

// email sign in
export const doLoginWithEmailAndPassword = async (email, password) => {
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
    return auth.signInAnonymously();
};


export const doSignOut = () => {
  return auth.signOut();
};

