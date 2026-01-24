# Quick Reference Guide - Project Structure

## 📁 Directory Tree

```
static/
├── css/
│   ├── global.css              # Global styles for entire app
│   ├── bot-builder.css         # Bot builder page styles
│   └── [future-page].css       # More pages as needed
├── js/
│   ├── bot-builder.js          # Bot builder main script (entry point)
│   ├── modules/
│   │   ├── data-processor.js   # CSV parsing, data display, search
│   │   ├── response-generator.js # Chat response logic
│   │   ├── chart-handler.js    # Charts and visualizations
│   │   └── ui-handler.js       # UI updates and interactions
│   ├── utils/
│   │   ├── helpers.js          # Formatting, debouncing, utilities
│   │   └── validators.js       # Email, password, file validation
│   ├── firebase-auth.js        # Firebase authentication
│   ├── firebase-config.js      # Firebase initialization
│   └── [future-module].js      # More scripts as needed
├── img/
│   ├── logos/
│   ├── icons/
│   └── [other-categories]/
└── README.md                   # Static assets documentation
```

## 🚀 Quick Tasks

### Need to Style the Bot Builder Page?
→ Edit `static/css/bot-builder.css`

### Need to Change Chat Logic?
→ Edit `static/js/modules/response-generator.js`

### Need to Parse Different Data?
→ Edit `static/js/modules/data-processor.js`

### Need to Add Validation?
→ Add to `static/js/utils/validators.js`

### Need a Helper Function?
→ Add to `static/js/utils/helpers.js`

### Need to Change Charts?
→ Edit `static/js/modules/chart-handler.js`

### Need to Modify UI Display?
→ Edit `static/js/modules/ui-handler.js`

## 📝 Module Functions

### data-processor.js
- `parseCSV(content)` - Parse CSV string
- `displayDataPreview(data)` - Show data in table
- `searchData(query, currentData)` - Search data
- `getFieldValue(row, fieldNames)` - Get field value
- `getProductName(row)` - Extract product name

### response-generator.js
- `generateResponse(query, results)` - Generate chat response

### chart-handler.js
- `createBarChart(data, columnName, oldChart)` - Create bar chart
- `createPieChart(data, columnName, oldChart)` - Create pie chart
- `generateChartColors(count)` - Generate chart colors
- `displayTableComparison(data)` - Show comparison table

### ui-handler.js
- `addChatMessage(sender, message)` - Add message to chat
- `showVisualizationSection()` - Show charts section
- `updateBotStatus(status)` - Update status text
- `clearChat()` - Clear chat history

### helpers.js
- `escapeHtml(text)` - Escape HTML chars
- `debounce(func, wait)` - Debounce function
- `formatNumber(num)` - Format with locale
- `formatCurrency(amount)` - Format as currency
- `sleep(ms)` - Sleep/delay
- Plus 10+ more utilities

### validators.js
- `validateEmail(email)` - Validate email
- `validatePassword(password)` - Check password strength
- `validateUsername(username)` - Validate username
- `validateCsvFile(file)` - Validate CSV file
- `validateJsonFile(file)` - Validate JSON file
- Plus 10+ more validators

## 🔗 How Pages Connect to Assets

```
bot_builder.html (Template)
    ↓
    Links: global.css, bot-builder.css, bot-builder.js
    ↓
bot-builder.js (Main Script)
    ↓
    Imports: modules/*, utils/*, firebase-config.js, firebase-auth.js
    ↓
    Executes: All bot builder functionality
```

## 📋 Checklist for New Features

- [ ] Does it need CSS? → Add to `css/page-name.css`
- [ ] Does it process data? → Add to `modules/data-processor.js`
- [ ] Does it generate responses? → Add to `modules/response-generator.js`
- [ ] Does it need validation? → Add to `utils/validators.js`
- [ ] Does it need helpers? → Add to `utils/helpers.js`
- [ ] Does it update UI? → Use `modules/ui-handler.js` functions
- [ ] Does it need charts? → Use `modules/chart-handler.js` functions

## 🎯 Import Examples

```javascript
// Import data processing
import { parseCSV, searchData } from './modules/data-processor.js';

// Import response generation
import { generateResponse } from './modules/response-generator.js';

// Import UI updates
import { addChatMessage, updateBotStatus } from './modules/ui-handler.js';

// Import validation
import { validateEmail, validatePassword } from './utils/validators.js';

// Import helpers
import { formatNumber, debounce } from './utils/helpers.js';
```

## 📊 File Sizes (Approximate)

| File | Size | Purpose |
|------|------|---------|
| global.css | 2-3 KB | Global styles |
| bot-builder.css | 3-4 KB | Page styles |
| bot-builder.js | 8-10 KB | Main script |
| data-processor.js | 3 KB | Data logic |
| response-generator.js | 4 KB | Chat logic |
| chart-handler.js | 4 KB | Chart logic |
| ui-handler.js | 2 KB | UI logic |
| helpers.js | 3 KB | Utilities |
| validators.js | 4 KB | Validation |

## 🔧 Common Operations

### Add New Global Style
```css
/* In global.css */
.my-class {
  color: #fff;
}
```

### Add New Validator
```javascript
// In validators.js
export function validateMyThing(value) {
  return value.length > 3;
}
```

### Add New Helper
```javascript
// In helpers.js
export function myHelper(param) {
  return param.toUpperCase();
}
```

### Use New Validator
```javascript
// In bot-builder.js or modules
import { validateMyThing } from './utils/validators.js';

if (validateMyThing(input)) {
  // Valid
}
```

### Add Chart
```javascript
// In chart-handler.js
export function createLineChart(data, columnName, oldChart) {
  // Create and return chart
}
```

## 📚 Documentation Files

- `PROJECT_STRUCTURE.md` - Complete project overview
- `RESTRUCTURING_SUMMARY.md` - What was changed and why
- `static/README.md` - Static assets detailed documentation
- This file - Quick reference

## ✅ Best Practices

1. ✓ Keep modules small and focused
2. ✓ Export only what's needed
3. ✓ Use descriptive function names
4. ✓ Add JSDoc comments to functions
5. ✓ Avoid global variables
6. ✓ Use CSS classes for styling
7. ✓ Validate user input
8. ✓ Escape HTML for security

## 🚦 Status

- ✅ CSS separated
- ✅ JavaScript modularized
- ✅ Utilities created
- ✅ Validators created
- ✅ Documentation complete
- ⏳ Ready for other pages
- ⏳ Ready for build tool integration

## 🆘 Need Help?

1. Check `PROJECT_STRUCTURE.md` for detailed explanations
2. Check `RESTRUCTURING_SUMMARY.md` for what changed
3. Check `static/README.md` for asset guidelines
4. Check JSDoc comments in module files
5. Review imports in `bot-builder.js` for examples

---
**Version**: 1.0
**Last Updated**: 2026-01-23
**Status**: Complete ✓
