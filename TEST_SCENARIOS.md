🧪 NexusBot - Test Scenarios & Validation

## Pre-Demo Testing Checklist

Run through this checklist before your presentation to ensure everything works.

---

## Test 1: Application Startup ✅

**Goal**: Verify Flask starts correctly

```bash
# Step 1: Start Flask
python app.py

# Expected Output:
# * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
# * Restarting with reloader
# * Debugger is active!

# Step 2: Open browser
http://localhost:5000

# Expected: Redirected to signup page
# Shows: "NexusBot" logo, signup form
```

**Pass/Fail**: ___

---

## Test 2: User Registration ✅

**Goal**: Create test account

```
1. Click "Sign Up" (if not already on signup page)
2. Fill form:
   - Email: test@nexusbot.com
   - Username: testuser
   - Password: Test12345
   - Confirm: Test12345
3. Click "Sign Up"

Expected:
✅ Account created successfully
✅ Redirected to login page
✅ Can see "Welcome back to your AI assistant"
```

**Pass/Fail**: ___

---

## Test 3: User Login ✅

**Goal**: Login with test account

```
1. Enter email: test@nexusbot.com
2. Enter password: Test12345
3. Click "Login"

Expected:
✅ Login successful message
✅ Redirected to /home (dashboard)
✅ See "Welcome, testuser" in navbar
✅ Show feature cards (Create Bot, Templates)
```

**Pass/Fail**: ___

---

## Test 4: Templates Page ✅

**Goal**: Verify all 6 templates load

```
1. Click "Templates" in navbar
2. Expected to see 6 cards:
   ✅ Sales Dashboard (blue)
   ✅ Student Records (purple)
   ✅ Lab Experiment (green)
   ✅ Economic Data (red)
   ✅ Health Data (yellow)
   ✅ Survey Results (indigo)

3. For each template, verify:
   ✅ Title shows
   ✅ Icon displays
   ✅ Description visible
   ✅ "Start Exploring" button present
```

**Pass/Fail**: ___

---

## Test 5: Load Template Data ✅

**Goal**: Load Sales Dashboard and verify data

```
1. Click "Start Exploring" on Sales Dashboard
2. Wait 2-3 seconds

Expected:
✅ Page redirects to /bot_builder?template=true
✅ Data loads in preview table
✅ See products: Amul Milk, Butter, Bread, etc.
✅ See columns: product, category, price, quantity, brand
✅ Chat input enabled (not greyed out)
✅ "Bot Status: Loaded: Sales Dashboard"
```

**Pass/Fail**: ___

---

## Test 6: Chat with Data ✅

**Goal**: Test bot search algorithm

```
Test 1: Show all products
Input: "Show all products"
Expected: List of 10 products with names and prices

Test 2: Search by price
Input: "price 50"
Expected: Products with price = 50

Test 3: Search by brand
Input: "Amul"
Expected: Find "Amul Milk 1L"

Test 4: Filter query
Input: "Find products > 100"
Expected: Show products with price > 100

Test 5: Complex query
Input: "Dairy products under 100"
Expected: Smart search finds matching items
```

**Results**:
- Test 1: ___
- Test 2: ___
- Test 3: ___
- Test 4: ___
- Test 5: ___

---

## Test 7: Export PDF ✅

**Goal**: Export chat history

```
1. After chatting, click "📄 Export PDF" button
2. Expected: Download dialog appears
3. Save file as chat-export.txt
4. Open file in text editor
5. Verify content:
   ✅ Contains "Chat History Export"
   ✅ Shows timestamp
   ✅ Shows "Sales Dashboard"
   ✅ Lists all chat messages
   ✅ Shows Q&A pairs
```

**Pass/Fail**: ___

---

## Test 8: Save Bot ✅

**Goal**: Save current bot to Firestore

```
1. In bot_builder, click "Save Bot" button
2. Expected: Popup for bot name
3. Enter: "My Sales Bot"
4. Click "Save"

Expected:
✅ "Bot saved successfully" message
✅ Status updates to "Saved"
✅ Can view in /my_bots
```

**Pass/Fail**: ___

---

## Test 9: My Bots Dashboard ✅

**Goal**: View saved bots

```
1. Click "My Bots" in navbar
2. Expected to see:
   ✅ Stats at top:
      - Total Bots: 1
      - Total Conversations: X
      - Shared Bots: 0
      - Starred by Others: 0

3. Bot card showing:
   ✅ Bot name: "My Sales Bot"
   ✅ Creation date
   ✅ Data rows: 10
   ✅ Conversation count
   ✅ Filename
   ✅ Buttons: Open, Share, Delete

4. Click "Open Bot" → Returns to bot_builder
5. Click "Share" → Bot becomes public
```

**Pass/Fail**: ___

---

## Test 10: Create Assignment ✅

**Goal**: Create assignment for students

```
1. Click "Assignments" in navbar
2. Click "+ Create Assignment"
3. Fill form:
   - Title: "Sales Data Analysis"
   - Description: "Analyze the sales dataset"
   - Data Source: Sales Dashboard
   - Audience: Students
   - Due Date: Tomorrow
   - Questions:
     * "What brands are available?"
     * "Find highest priced item"
     * "How many Dairy products?"

4. Click "Create Assignment"

Expected:
✅ "Assignment created successfully"
✅ Returns to assignments list
✅ New assignment appears in list
```

**Pass/Fail**: ___

---

## Test 11: View Assignment as Student ✅

**Goal**: Simulate student experience

```
1. In assignments list, find the one you created
2. Click "Share Link"
3. Copy the link: /assignment/<id>
4. Expected message: "Share link copied to clipboard!"

5. Open the assignment link in NEW TAB/BROWSER
6. Expected to see:
   ✅ Assignment title
   ✅ Description
   ✅ 4 stat boxes (Due Date, Questions, Submissions, Status)
   ✅ 3 questions listed as cards
   ✅ "Start Assignment" button
   ✅ Status: Pending
```

**Pass/Fail**: ___

---

## Test 12: Start Assignment ✅

**Goal**: Complete assignment flow

```
1. On assignment page, click "Start Assignment"
2. Expected: Redirected to /templates
3. Select "Sales Dashboard"
4. Expected: bot_builder loads with data
5. Chat and answer questions:
   - "What brands are available?"
   - "Find highest priced item"
   - "How many Dairy products?"
6. Click "Export PDF"
7. Download transcript as proof

Expected:
✅ Can explore data
✅ Get answers to questions
✅ Export chat for submission
```

**Pass/Fail**: ___

---

## Test 13: Mobile Responsiveness ✅

**Goal**: Verify mobile layout

```
1. Press F12 to open Developer Tools
2. Click responsive design mode icon
3. Set to iPhone 12 (390x844)

For each page, verify:
   ✅ home.html - Menu collapses, readable
   ✅ templates.html - Cards stack, clickable
   ✅ bot_builder.html - Layout adapts
   ✅ my_bots.html - Data readable
   ✅ assignments.html - Form fits screen
   ✅ assignment_detail.html - Questions clear

Expected: All pages readable and functional on mobile
```

**Pass/Fail**: ___

---

## Test 14: Navigation ✅

**Goal**: Test all navbar links

```
From home.html, click each navbar item:

1. "Create Bot" → /bot_builder ✅
2. "Templates" → /templates ✅
3. "My Bots" → /my_bots ✅
4. "Assignments" → /assignments ✅
5. "Home" → /home ✅
6. Logo → /home ✅

From any page:
7. Login button → /login ✅
8. Logout button → /logout ✅
```

**Results**: ___

---

## Test 15: Error Handling ✅

**Goal**: Verify graceful error handling

```
Test 1: Invalid assignment ID
- Go to /assignment/invalid123
- Expected: "Assignment not found"

Test 2: Chat with no data
- Go to bot_builder (no upload)
- Try to chat
- Expected: Input disabled

Test 3: Export with no chat
- Upload data but don't chat
- Click Export PDF
- Expected: Alert "No chat history to export"

Test 4: Browser console
- Press F12
- Check Console tab
- Expected: No red errors
- OK: Warnings about Firebase, etc.
```

**Pass/Fail**: ___

---

## 📊 Overall Test Results

| Test | Status | Notes |
|------|--------|-------|
| 1. Startup | ✅/❌ | |
| 2. Register | ✅/❌ | |
| 3. Login | ✅/❌ | |
| 4. Templates | ✅/❌ | |
| 5. Load Data | ✅/❌ | |
| 6. Chat | ✅/❌ | |
| 7. Export | ✅/❌ | |
| 8. Save Bot | ✅/❌ | |
| 9. My Bots | ✅/❌ | |
| 10. Create Assignment | ✅/❌ | |
| 11. View Assignment | ✅/❌ | |
| 12. Start Assignment | ✅/❌ | |
| 13. Mobile | ✅/❌ | |
| 14. Navigation | ✅/❌ | |
| 15. Errors | ✅/❌ | |

**Overall Result**: _______________

---

## 🎬 Demo Script Timing

Run through your actual demo script and time it:

```
Minute 0:00 - 0:30
[ ] Show Templates page
[ ] Time: _____ sec

Minute 0:30 - 1:30
[ ] Click "Sales Dashboard"
[ ] Data loads
[ ] Time: _____ sec

Minute 1:30 - 3:00
[ ] Chat demo (3-4 questions)
[ ] Time: _____ sec

Minute 3:00 - 3:30
[ ] Export PDF
[ ] Time: _____ sec

Minute 3:30 - 4:30
[ ] Create assignment
[ ] Fill form
[ ] Time: _____ sec

Minute 4:30 - 5:00
[ ] Q&A / Close

TOTAL TIME: _____ min
TARGET: 5 minutes
```

---

## 🚨 Critical Issues to Fix

If any test fails, list it here:

```
Issue 1: _______________________________
Fix: _________________________________

Issue 2: _______________________________
Fix: _________________________________

Issue 3: _______________________________
Fix: _________________________________
```

---

## ✅ Final Checklist

Before presenting:

- [ ] All 15 tests pass
- [ ] No console errors
- [ ] Mobile layout looks good
- [ ] Demo script is timed correctly
- [ ] Can answer common questions
- [ ] Have backup laptop/phone for demo
- [ ] Presentation slides ready
- [ ] Backup demo video prepared
- [ ] Have college pitch deck
- [ ] Dressed professionally

---

## 🎉 Ready to Present!

Once all tests pass, you're ready to:
1. Show college stakeholders
2. Gather feedback
3. Answer questions
4. Discuss implementation
5. Plan deployment

**Good luck with your presentation! You've built something amazing!** 🚀
