# 🗺️ NexusBot - Application Architecture & Workflow

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Web Browser                              │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐  │
│  │  home.html   │templates.html│ my_bots.html │assignments.│  │
│  │  (Dashboard) │ (Datasets)   │ (Manager)    │ (Teacher)  │  │
│  └──────────────┴──────────────┴──────────────┴──────────────┘  │
│                            ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         bot_builder.html (Chat Interface)               │  │
│  │  ┌────────────────┐  ┌──────────────────────────────┐  │  │
│  │  │ Data Preview   │  │  Chat Messages               │  │  │
│  │  │ Table          │  │  • Export PDF                │  │  │
│  │  │                │  │  • Save Bot                  │  │  │
│  │  └────────────────┘  └──────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │        assignment_detail.html (Student View)            │  │
│  │  • View questions                                       │  │
│  │  • Start assignment                                     │  │
│  │  • Track progress                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                     Flask Backend (app.py)                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Routes                                                  │  │
│  │  GET  /              → home                              │  │
│  │  GET  /templates     → templates                         │  │
│  │  GET  /bot_builder   → bot_builder                       │  │
│  │  GET  /my_bots       → my_bots                           │  │
│  │  GET  /assignments   → assignments                       │  │
│  │  GET  /assignment/:id → assignment_detail               │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Firebase Services                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐  │
│  │   Firebase Auth  │  │  Firestore DB    │  │  Storage    │  │
│  │                  │  │                  │  │             │  │
│  │ • signup         │  │ • bots/          │  │ • Backups   │  │
│  │ • login          │  │ • assignments/   │  │             │  │
│  │ • logout         │  │ • users/         │  │             │  │
│  │ • reset password │  │                  │  │             │  │
│  └──────────────────┘  └──────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## User Journeys

### 🎓 Student Workflow

```
Login
  ↓
Home Dashboard
  ├─ Click "Templates"
  │   ├─ Browse 6 datasets
  │   ├─ Click "Start Exploring"
  │   ├─ Load data → bot_builder
  │   ├─ Chat with data
  │   ├─ Ask questions
  │   └─ Export chat
  │
  ├─ Click "My Bots"
  │   ├─ See saved bots
  │   └─ Open previous bots
  │
  └─ Receive Assignment Link
      ├─ Open /assignment/<id>
      ├─ See questions
      ├─ Click "Start Assignment"
      ├─ Use bot to answer
      ├─ Export transcript
      └─ Submit to teacher
```

### 👨‍🏫 Teacher Workflow

```
Login
  ↓
Home Dashboard
  ├─ Click "Create Bot"
  │   ├─ Upload data (CSV/JSON)
  │   ├─ Test with chatbot
  │   ├─ Save as bot
  │   └─ Use for future classes
  │
  ├─ Click "My Bots"
  │   ├─ View all bots
  │   ├─ Make public/private
  │   ├─ Share with students
  │   └─ Track usage
  │
  └─ Click "Assignments"
      ├─ Click "+ Create Assignment"
      ├─ Fill form:
      │   ├─ Title
      │   ├─ Description
      │   ├─ Select data (template or bot)
      │   ├─ Set due date
      │   └─ Add questions
      ├─ Create → Save to Firestore
      ├─ Copy share link
      ├─ Send to students
      └─ Monitor submissions
```

### 👥 Admin/Institution Workflow

```
Dashboard View
  ├─ See all users
  ├─ See all bots created
  ├─ See all assignments
  ├─ Track engagement stats
  └─ Generate reports
```

---

## Data Models

### Users Collection
```
users/{uid}/
├── username: string
├── email: string
├── createdAt: timestamp
└── botCount: number
```

### Bots Collection
```
bots/{botId}/
├── userId: string
├── name: string
├── fileName: string
├── data: array<object>
├── createdAt: timestamp
├── messageCount: number
├── isPublic: boolean
└── metadata: object
```

### Assignments Collection
```
assignments/{assignmentId}/
├── title: string
├── description: string
├── dataSource: string
├── dueDate: date
├── questions: array<string>
├── createdBy: string
├── createdAt: timestamp
├── submissions: number
└── isPublished: boolean
```

---

## Feature Matrix

| Feature | Student | Teacher | Admin | Public |
|---------|---------|---------|-------|--------|
| View Templates | ✅ | ✅ | ✅ | ✅ |
| Create Bot | ✅ | ✅ | ✅ | ❌ |
| Save Bot | ✅ | ✅ | ✅ | ❌ |
| View My Bots | ✅ | ✅ | ❌ | ❌ |
| Share Bot | ❌ | ✅ | ✅ | ❌ |
| Create Assignment | ❌ | ✅ | ✅ | ❌ |
| View Assignment | ✅ | ✅ | ✅ | ✅ |
| Complete Assignment | ✅ | ❌ | ❌ | ✅ |
| Export Chat | ✅ | ✅ | ✅ | ✅ |
| View Statistics | ❌ | ✅ | ✅ | ❌ |

---

## Page Navigation Map

```
┌─────────────────────────────────────────────────┐
│                    home.html                    │
│            (Main Dashboard - Always)            │
└──────────┬──────────┬──────────┬────────────────┘
           │          │          │
     ┌─────▼─┐  ┌─────▼─────┐  └──────────┐
     │Create │  │Templates  │             │
     │  Bot  │  │  (Browse) │             │
     └──┬────┘  └─────┬─────┘             │
        │             │                   │
        │         ┌───▼──────────┐        │
        │         │ Load Template │        │
        └────────►│ in bot_builder│◄──────┘
                  └───┬──────────┘
                      │
              ┌───────┴─────────┐
              │                 │
         ┌────▼──────┐    ┌─────▼──────────┐
         │ my_bots   │    │ assignments    │
         │(Manage)   │    │(Create/Manage) │
         └────┬──────┘    └────┬───────────┘
              │                │
              │          ┌─────▼──────────────┐
              └─────────►│ assignment_detail  │
                         │   (Student View)   │
                         └────────────────────┘
```

---

## Data Flow Examples

### Template Loading Flow
```
Home → Click "Templates"
  ↓
Load templates.html
  ↓
User clicks "Sales Dashboard"
  ↓
Set sessionStorage:
  - templateData = array of products
  - templateName = "Sales Dashboard"
  ↓
Navigate to /bot_builder?template=true
  ↓
bot_builder.html:
  - Detect ?template=true in URL
  - Load from sessionStorage
  - Display data preview
  - Enable chat input
  ↓
User chats with data
```

### Assignment Creation Flow
```
Home → Click "Assignments"
  ↓
Load assignments.html
  ↓
Click "+ Create Assignment"
  ↓
Modal opens with form:
  - Title
  - Description
  - Data source
  - Due date
  - Questions
  ↓
User fills & clicks "Create"
  ↓
Firebase addDoc():
  - Save to assignments/ collection
  - Store userId, timestamp, etc.
  ↓
Firestore triggers:
  - Add to teacher's list
  - Generate shareable link
  ↓
Teacher gets: /assignment/<docId>
  ↓
Teacher sends to students
```

### Assignment Completion Flow
```
Student receives /assignment/<id> link
  ↓
assignment_detail.html loads
  ↓
Show assignment details + questions
  ↓
Student clicks "Start Assignment"
  ↓
Redirect to /templates
  ↓
Select data source
  ↓
Load bot_builder with data
  ↓
Chat with data to answer questions
  ↓
Click "Export PDF"
  ↓
Download chat transcript
  ↓
Submit to teacher (via email/form)
  ↓
Teacher grades submission
```

---

## Technology Stack

```
Frontend:
  ├─ HTML5
  ├─ Tailwind CSS 2.x (Utility-first styling)
  ├─ JavaScript ES6 modules
  ├─ Firebase Web SDK v10.7.1
  └─ sessionStorage for data passing

Backend:
  ├─ Flask 2.3.3 (Python web framework)
  ├─ Jinja2 (Template rendering)
  └─ SQLAlchemy (Legacy, for session)

Database:
  ├─ Firestore (Real-time NoSQL)
  ├─ Firebase Auth (User management)
  └─ SQLite (Flask sessions)

Deployment Ready:
  ├─ Heroku
  ├─ AWS
  ├─ Google Cloud
  └─ Self-hosted
```

---

## Feature Interaction Diagram

```
┌────────────────────────────────────────────────────┐
│                  Core Features                     │
├────────────────────────────────────────────────────┤
│                                                    │
│  Templates  ←──────┐                              │
│      ↓            │                              │
│  bot_builder ◄────┴─── my_bots                   │
│      │                    │                      │
│      ├─ Chat          ├─ Create                  │
│      ├─ Export        ├─ Share                   │
│      └─ Save          └─ Delete                  │
│                           │                      │
│  assignments ◄────────────┘                      │
│      ├─ Create by teacher                        │
│      ├─ Share with students                      │
│      └─ Complete by students                     │
│                                                    │
│  assignment_detail                               │
│      └─ View + Start assignment                  │
│                                                    │
└────────────────────────────────────────────────────┘
           ↓
      Firestore Database
      (Persistent Storage)
```

---

## Security Model

```
┌─────────────────────────────────┐
│      User Authentication        │
│  (Firebase Email/Password)      │
└──────────┬──────────────────────┘
           │
           ↓
┌─────────────────────────────────┐
│    Firestore Security Rules     │
├─────────────────────────────────┤
│ ✅ Users can read own data      │
│ ✅ Users can write own bots     │
│ ✅ Public bots readable by all  │
│ ✅ Assignments by creator only  │
│ ✅ Students can read shared     │
└─────────────────────────────────┘
           │
           ↓
┌─────────────────────────────────┐
│    Session Management           │
│  (Flask sessions + Firebase)    │
└─────────────────────────────────┘
```

---

## Scalability

```
Low Volume (100 students):
  └─ Single Firebase project
     └─ Firestore free tier
     └─ Flask on localhost

Medium Volume (1000 students):
  └─ Firebase project
  └─ Firestore free tier + usage monitoring
  └─ Flask on Heroku free tier

High Volume (10,000+ students):
  └─ Firebase Blaze plan (pay per use)
  └─ Firestore indexed queries
  └─ Flask on Cloud Run / AWS ECS
  └─ Cloud Storage for large files
  └─ CDN for static files
```

---

## Monitoring & Analytics

```
Track:
  ├─ User signups (Firebase Analytics)
  ├─ Bot usage (messageCount field)
  ├─ Assignment completions
  ├─ Chat patterns (query types)
  ├─ Export frequency
  └─ Feature adoption

Display:
  ├─ Dashboard stats (home page)
  ├─ My Bots stats
  ├─ Assignment metrics
  └─ Student progress
```

---

## Future Enhancements Roadmap

```
Phase 1 (Current) ✅
  ├─ Templates
  ├─ Bot creation
  ├─ Assignments
  └─ Chat export

Phase 2 (Planned)
  ├─ Real PDF export
  ├─ Advanced visualizations
  ├─ Auto-grading
  └─ Leaderboards

Phase 3 (Future)
  ├─ Mobile app
  ├─ API marketplace
  ├─ Collaborative bots
  └─ AI-powered insights
```

---

This architecture provides a scalable, user-friendly platform for educational data exploration! 🚀
