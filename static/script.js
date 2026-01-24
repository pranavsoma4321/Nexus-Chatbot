// Import Firebase Auth Service
import authService from './firebase-auth.js';

// Intersection Observer to trigger fade-in animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

// Observe all section-fade-in elements
document.querySelectorAll('.section-fade-in').forEach(el => {
  observer.observe(el);
});

// Login/Logout Button Functionality
const loginBtn = document.getElementById('loginBtn');
const loginBtnMobile = document.getElementById('loginBtnMobile');
const logoutBtn = document.getElementById('logoutBtn');
const logoutBtnMobile = document.getElementById('logoutBtnMobile');
const usernameDisplay = document.getElementById('usernameDisplay');

// Function to update button visibility based on auth state
function updateAuthButtons() {
  const user = authService.getCurrentUser();
  console.log('Auth state check - User:', user);
  if (user) {
    // User is logged in - show logout, hide login
    if (loginBtn) {
      loginBtn.style.display = 'none';
    }
    if (loginBtnMobile) {
      loginBtnMobile.style.display = 'none';
    }
    if (logoutBtn) {
      logoutBtn.style.display = 'block';
    }
    if (logoutBtnMobile) {
      logoutBtnMobile.style.display = 'block';
    }
    
    // Display username
    if (usernameDisplay) {
      authService.getUserData(user.uid).then(userData => {
        if (userData && userData.username) {
          usernameDisplay.textContent = `Welcome, ${userData.username}!`;
          usernameDisplay.style.display = 'block';
        }
      });
    }
  } else {
    // User is logged out - show login, hide logout
    if (loginBtn) {
      loginBtn.style.display = 'block';
    }
    if (loginBtnMobile) {
      loginBtnMobile.style.display = 'block';
    }
    if (logoutBtn) {
      logoutBtn.style.display = 'none';
    }
    if (logoutBtnMobile) {
      logoutBtnMobile.style.display = 'none';
    }
    if (usernameDisplay) {
      usernameDisplay.style.display = 'none';
    }
  }
}

// Update buttons on page load with a slight delay to ensure Firebase is ready
setTimeout(() => {
  updateAuthButtons();
}, 500);

// Listen for auth state changes
authService.initAuthListener(() => {
  updateAuthButtons();
});

if (loginBtn) {
  loginBtn.addEventListener('click', () => {
    window.location.href = '/login';
  });
}

if (loginBtnMobile) {
  loginBtnMobile.addEventListener('click', () => {
    window.location.href = '/login';
  });
}

if (logoutBtn) {
  logoutBtn.addEventListener('click', async () => {
    await authService.signOut();
    window.location.href = '/login';
  });
}

if (logoutBtnMobile) {
  logoutBtnMobile.addEventListener('click', async () => {
    await authService.signOut();
    window.location.href = '/login';
  });
}

// Mobile Menu Toggle
const mobileMenuButton = document.getElementById('mobile-menu-button');
const mobileMenu = document.getElementById('mobile-menu');

if (mobileMenuButton && mobileMenu) {
  mobileMenuButton.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
  });

  // Close menu when a link is clicked
  mobileMenu.querySelectorAll('a, button').forEach(el => {
    el.addEventListener('click', () => {
      mobileMenu.classList.add('hidden');
    });
  });
}

// Smooth scroll behavior for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href !== '#' && document.querySelector(href)) {
      e.preventDefault();
      document.querySelector(href).scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});
