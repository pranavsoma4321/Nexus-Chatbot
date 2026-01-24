import { auth, db, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged, doc, setDoc, getDoc } from './firebase-config.js';

// Authentication Service
class FirebaseAuthService {
    constructor() {
        this.user = null;
        this.authCallback = null;
        this.retryCount = 0;
        this.maxRetries = 3;
        this.initAuthListener();
        this.setupNetworkMonitoring();
    }

    // Setup network status monitoring
    setupNetworkMonitoring() {
        window.addEventListener('online', () => {
            console.log('Network connection restored');
            this.retryCount = 0;
        });
        
        window.addEventListener('offline', () => {
            console.warn('Network connection lost');
            this.showNetworkStatus('offline');
        });
    }

    // Show network status to user
    showNetworkStatus(status) {
        const existing = document.getElementById('network-status');
        if (existing) existing.remove();

        const statusDiv = document.createElement('div');
        statusDiv.id = 'network-status';
        statusDiv.className = `fixed top-20 left-1/2 transform -translate-x-1/2 z-50 px-6 py-3 rounded-lg text-white font-medium ${
            status === 'offline' ? 'bg-red-600' : 'bg-green-600'
        }`;
        statusDiv.textContent = status === 'offline' 
            ? '⚠️ You are offline. Some features may not work.' 
            : '✅ Connection restored';
        
        document.body.appendChild(statusDiv);
        
        if (status === 'online') {
            setTimeout(() => statusDiv.remove(), 3000);
        }
    }

    // Listen to authentication state changes
    initAuthListener(callback) {
        onAuthStateChanged(auth, (user) => {
            this.user = user;
            
            // Call custom callback if provided
            if (callback) {
                callback(user);
            }
            
            if (user) {
                console.log('User is signed in:', user.displayName);
                // Update UI to show logged in state
                this.updateUIForLoggedInUser(user);
            } else {
                console.log('User is signed out');
                // Update UI to show logged out state
                this.updateUIForLoggedOutUser();
            }
        });
    }

    // Sign up new user
    async signUp(email, password, username) {
        try {
            // Create user with email and password
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;

            // Update user profile with username
            await this.saveUserData(user.uid, username, email);

            return { success: true, user };
        } catch (error) {
            console.error('Signup error:', error);
            return { success: false, error: error.message };
        }
    }

    // Sign in existing user
    async signIn(email, password) {
        try {
            const userCredential = await signInWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;
            
            return { success: true, user };
        } catch (error) {
            console.error('Signin error:', error);
            return { success: false, error: error.message };
        }
    }

    // Sign out user
    async signOut() {
        try {
            await signOut(auth);
            return { success: true };
        } catch (error) {
            console.error('Signout error:', error);
            return { success: false, error: error.message };
        }
    }

    // Save user data to Firestore
    async saveUserData(userId, username, email) {
        try {
            await setDoc(doc(db, 'users', userId), {
                username: username,
                email: email,
                createdAt: new Date().toISOString(),
                lastLogin: new Date().toISOString()
            });
            return { success: true };
        } catch (error) {
            console.error('Error saving user data:', error);
            return { success: false, error: error.message };
        }
    }

    // Get user data from Firestore
    async getUserData(userId) {
        try {
            // Check network connectivity
            if (!navigator.onLine) {
                console.warn('Device is offline - using cached data if available');
                return { success: false, error: 'Device is offline. Please check your internet connection.' };
            }

            const docRef = doc(db, 'users', userId);
            const docSnap = await getDoc(docRef);
            
            if (docSnap.exists()) {
                return { success: true, data: docSnap.data() };
            } else {
                return { success: false, error: 'User data not found' };
            }
        } catch (error) {
            console.error('Error getting user data:', error);
            
            // Handle specific Firebase errors
            if (error.code === 'unavailable' || error.message.includes('offline')) {
                // Retry logic for network errors
                if (this.retryCount < this.maxRetries) {
                    this.retryCount++;
                    console.log(`Retrying... Attempt ${this.retryCount} of ${this.maxRetries}`);
                    
                    // Wait before retrying (exponential backoff)
                    await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, this.retryCount - 1)));
                    return this.getUserData(userId);
                } else {
                    return { success: false, error: 'Connection failed after multiple attempts. Please check your internet connection and refresh the page.' };
                }
            } else if (error.code === 'permission-denied') {
                return { success: false, error: 'Permission denied. Please check Firebase security rules.' };
            } else {
                return { success: false, error: error.message };
            }
        }
    }

    // Update UI for logged in user
    updateUIForLoggedInUser(user) {
        // Update username displays
        const usernameElements = document.querySelectorAll('.username-display');
        usernameElements.forEach(element => {
            element.textContent = user.displayName || user.email;
        });

        // Show/hide login/logout buttons
        const loginBtns = document.querySelectorAll('.login-btn');
        const logoutBtns = document.querySelectorAll('.logout-btn');
        
        loginBtns.forEach(btn => btn.classList.add('hidden'));
        logoutBtns.forEach(btn => btn.classList.remove('hidden'));
    }

    // Update UI for logged out user
    updateUIForLoggedOutUser() {
        // Reset username displays
        const usernameElements = document.querySelectorAll('.username-display');
        usernameElements.forEach(element => {
            element.textContent = 'Guest';
        });

        // Show/hide login/logout buttons
        const loginBtns = document.querySelectorAll('.login-btn');
        const logoutBtns = document.querySelectorAll('.logout-btn');
        
        loginBtns.forEach(btn => btn.classList.remove('hidden'));
        logoutBtns.forEach(btn => btn.classList.add('hidden'));
    }

    // Get current user
    getCurrentUser() {
        return this.user;
    }
}

// Create and export auth service instance
const authService = new FirebaseAuthService();
export default authService;
