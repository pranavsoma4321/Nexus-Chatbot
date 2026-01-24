# NexusBot - Quick Start Guide

## ⚡ 5-Minute Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Modern web browser
- Firebase project (free account)

### Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run Flask server
python app.py

# 3. Open browser
http://localhost:5000
```

**That's it!** You're ready to go.

---

## 🔐 First Time Setup

### 1. Create Firebase Project
1. Go to https://firebase.google.com
2. Click "Get Started"
3. Create a new project (free)
4. Copy your config values

### 2. Update Firebase Config
Edit `static/firebase-config.js`:
```javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT.appspot.com",
  messagingSenderId: "YOUR_ID",
  appId: "YOUR_APP_ID"
};
```

### 3. Set Flask Secret Key
Edit `app.py` line 8:
```python
app.secret_key = "choose-a-random-secret-key-here"
```

---

## 🎮 Quick Test

### Create a Test Account
1. Go to http://localhost:5000
2. Click "Sign Up"
3. Enter: 
   - Email: `test@example.com`
   - Username: `testuser`
   - Password: `password123`
4. Click "Sign Up"

### Try Each Feature

#### 1. Templates Page (No upload needed)
```
Home → Templates → Sales Dashboard → Start Exploring
Ask: "Show all products"
```

#### 2. Create Custom Bot
```
Home → Create Bot → Upload CSV file → Chat with data
```

#### 3. My Bots Dashboard
```
Home → My Bots → See all your saved bots
```

#### 4. Create Assignment
```
Home → Assignments → + Create Assignment
Title: "Test Assignment"
Data: Sales Dashboard
Due: Tomorrow
```

---

## 📁 File Structure

```
Chatbot-main/
├── app.py                    ← Flask app (main entry point)
├── requirements.txt          ← Python dependencies
├── templates/
│   ├── home.html            ← Dashboard
│   ├── bot_builder.html     ← Chat interface
│   ├── templates.html       ← Pre-made datasets
│   ├── my_bots.html         ← Bot management
│   ├── assignments.html     ← Create assignments
│   └── ...
├── static/
│   ├── firebase-config.js   ← Firebase settings
│   ├── firebase-auth.js     ← Auth service
│   └── style.css            ← Styling
└── README.md
```

---

## 🔧 Customization

### Add More Templates
Edit `templates/templates.html` - Add to `templates` object:
```javascript
templates.chemistry = {
  name: 'Chemistry Lab',
  data: [
    { compound: 'H2O', moles: 1.5, mass: 27 },
    // ... more data
  ]
}
```

### Change Colors
Search `bg-sky-500` → Replace with:
- `bg-blue-600` (Blue)
- `bg-purple-600` (Purple)
- `bg-green-600` (Green)
- `bg-red-600` (Red)

### Add More Questions
In `assignments.html`, add to question options:
```javascript
<option value="medical">Medical Records</option>
<option value="weather">Weather Data</option>
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
```bash
pip install -r requirements.txt
```

### "Firebase is not initialized"
- Check `firebase-config.js` has correct credentials
- Verify project ID is correct in Firebase console

### "Port 5000 already in use"
```bash
python app.py --port 5001
```

### Chat is not working
- Check browser console (F12)
- Ensure you're logged in
- Try uploading data first
- Check Firebase Firestore rules are set to public read

---

## 📊 Sample Data Files

### CSV Format
```csv
name,price,category
Milk,50,Dairy
Butter,150,Dairy
Bread,35,Bakery
```

### JSON Format
```json
[
  {"name": "Milk", "price": 50, "category": "Dairy"},
  {"name": "Butter", "price": 150, "category": "Dairy"}
]
```

---

## 🎯 Demo Script (5 minutes)

1. **Show Home** (30 sec)
   - Clean dashboard
   - Quick navigation buttons

2. **Click Templates** (1 min)
   - Show 6 available datasets
   - Click "Sales Dashboard"

3. **Ask Questions** (2 min)
   - "Show me all products"
   - "What brands are available?"
   - "Find price > 100"

4. **Export Chat** (30 sec)
   - Click "Export PDF"
   - Show downloaded file

5. **Create Assignment** (1 min)
   - Assignments → + Create
   - Fill form
   - Copy link

---

## 📱 Mobile Testing

```bash
# Get your computer IP
ipconfig getifaddr en0  # Mac
ipconfig              # Windows

# Open on phone
http://YOUR_IP:5000
```

---

## 🚀 Deployment

### To Deploy on Heroku:
```bash
# Install Heroku CLI
# Login: heroku login
# Create app
heroku create your-app-name
# Deploy
git push heroku main
```

### To Deploy on Replit:
1. Go to https://replit.com
2. Click "Import from GitHub"
3. Paste your repo URL
4. Run
5. Share link

---

## ✅ Checklist Before Presentation

- [ ] Flask server running (`python app.py`)
- [ ] Firebase credentials updated
- [ ] Can sign up / login
- [ ] Templates page loads with 6 datasets
- [ ] Can chat with Sales Dashboard
- [ ] Export PDF button works
- [ ] Can create assignment
- [ ] My Bots dashboard shows saved bots
- [ ] Mobile view looks good (test on phone)
- [ ] No console errors (F12)

---

## 📚 Next Steps

1. **Test with Real Data**
   - Upload your own CSV
   - Verify columns are detected
   - Test search algorithm

2. **Customize for Your Class**
   - Add subject-specific templates
   - Create sample assignments
   - Prepare datasets

3. **Share with Teachers**
   - Send demo link
   - Explain workflow
   - Answer questions

4. **Gather Feedback**
   - What features would help?
   - What's missing?
   - Any bugs?

---

## 💬 Getting Help

1. **Check console logs** - F12 → Console tab
2. **Read error messages** - They're usually helpful
3. **Check Firebase rules** - May need to allow public access
4. **Test with template data first** - Easier to debug
5. **Review FEATURES.md** - Detailed documentation

---

**You're all set!** Start by exploring templates, then create your first assignment. Good luck! 🚀
