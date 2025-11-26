import { doc, setDoc, updateDoc, deleteField } from "firebase/firestore";
import { auth, db } from "./firebase.js";

// save ONE measurement set to profile
export const doSaveToProfile = async (measurements: any) => {
    const user = auth.currentUser;
    // if not logged in
    if (!user) throw new Error("No auth");
    // if guest user
    if (user.isAnonymous) {
        throw new Error("Must Sign in");
    }

    const userRef = doc(db, "users", user.uid);

    //merges with past (change for multiple please)
    await setDoc(userRef, { measurements }, { merge: true });
};

export const deleteFromProfile = async () => {
    const user = auth.currentUser;
    // if not logged in
    if (!user) throw new Error("No auth");
    // if guest user
    if (user.isAnonymous) {
        throw new Error("Must Sign in");
    }

    const userRef = doc(db, "users", user.uid);

    //merges with past (change for multiple please)
    await updateDoc(userRef, { measurements: deleteField() });

}