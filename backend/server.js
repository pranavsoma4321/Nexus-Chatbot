const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const User = require('./models/user');

const app = express();

// Middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(
  session({
    secret: 'your-secret-key',
    resave: false,
    saveUninitialized: true,
    store: new session.MemoryStore(), // You can use other session stores like MongoDB or Redis
  })
);

// Routes
app.get('/login', (req, res) => {
  res.render('login');
});

app.post('/login', async (req, res) => {
  const { email, password } = req.body;

  try {
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(401).json({ error: 'Invalid email or password' });
    }

    const passwordMatch = await bcrypt.compare(password, user.password);
    if (!passwordMatch) {
      return res.status(401).json({ error: 'Invalid email or password' });
    }

    req.session.user = user;
    return res.json({ message: 'Login successful' });
  } catch (error) {
    return res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/profile', (req, res) => {
  if (req.session.user) {
    return res.json({ user: req.session.user });
  }
  return res.status(401).json({ error: 'Unauthorized' });
});

// Other routes...

// Set up view engine
app.set('view engine', 'ejs');
app.set('views', './templates');

// Start the server
app.listen(3000, () => {
  console.log('Server is running on port 3000');
});