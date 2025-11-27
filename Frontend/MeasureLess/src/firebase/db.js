import { doc, setDoc, updateDoc, deleteField, getDoc } from "firebase/firestore";
import { auth, db } from "./firebase.js";

// save ONE measurement set to profile
export const doSaveToProfile = async (measurements) => {
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

export const getMeasurementsFromDB = async () => {
    const user = auth.currentUser;
    // if not logged in
    if (!user) throw new Error("No auth");
    // if guest user
    if (user.isAnonymous) {
        throw new Error("Must Sign in");
    }

    const userRef = doc(db, "users", user.uid);
    const docSnap = await getDoc(userRef);

    // if data return measurements or empty
    if (docSnap.exists()) {
        const data = docSnap.data();
        return data.measurements || null;
    }else{
        // if no data return null
        return null;
    }
}