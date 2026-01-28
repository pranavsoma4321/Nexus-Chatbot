// Import Firebase Auth Service
import authService from './firebase-auth.js';
import { db } from './firebase-config.js';
import { collection, getDocs, query, where } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';

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

    renderRecentBots(user.uid);
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

    const recentBotsSection = document.getElementById('recentBotsSection');
    const recentBotsList = document.getElementById('recentBotsList');
    if (recentBotsSection) recentBotsSection.classList.add('hidden');
    if (recentBotsList) recentBotsList.innerHTML = '';
  }
}

async function renderRecentBots(userId) {
  const recentBotsSection = document.getElementById('recentBotsSection');
  const recentBotsList = document.getElementById('recentBotsList');
  if (!recentBotsSection || !recentBotsList) return;

  try {
    const botsQuery = query(collection(db, 'bots'), where('userId', '==', userId));
    const snapshot = await getDocs(botsQuery);

    const bots = [];
    snapshot.forEach(docSnap => {
      bots.push({ id: docSnap.id, ...docSnap.data() });
    });

    const toMillis = (v) => {
      if (!v) return 0;
      if (typeof v === 'string') {
        const t = Date.parse(v);
        return Number.isNaN(t) ? 0 : t;
      }
      if (typeof v?.toDate === 'function') return v.toDate().getTime();
      if (typeof v?.seconds === 'number') return v.seconds * 1000;
      return 0;
    };

    bots.sort((a, b) => {
      const bTime = Math.max(toMillis(b.updatedAt), toMillis(b.createdAt));
      const aTime = Math.max(toMillis(a.updatedAt), toMillis(a.createdAt));
      return bTime - aTime;
    });

    const topBots = bots.slice(0, 3);
    if (topBots.length === 0) {
      recentBotsSection.classList.add('hidden');
      recentBotsList.innerHTML = '';
      return;
    }

    recentBotsSection.classList.remove('hidden');
    recentBotsList.innerHTML = topBots.map(bot => {
      const name = bot.name || 'Untitled Bot';
      const rows = Array.isArray(bot.data) ? bot.data.length : 0;
      const chats = bot.messageCount || 0;
      return `
        <a href="/bot_builder?botId=${bot.id}" class="block rounded-xl border border-gray-800 bg-black/30 hover:bg-black/50 transition-colors p-4">
          <div class="flex items-start justify-between gap-3">
            <div class="min-w-0">
              <div class="text-white font-semibold truncate">${name}</div>
              <div class="text-xs text-gray-400 mt-1">${rows} rows • ${chats} chats</div>
            </div>
            <div class="text-sky-400 text-sm font-semibold">Open</div>
          </div>
        </a>
      `;
    }).join('');
  } catch (e) {
    console.error('Failed to load recent bots:', e);
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
