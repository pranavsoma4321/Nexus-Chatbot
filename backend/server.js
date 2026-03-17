const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const mongoose = require('mongoose');
const User = require('./models/User');

const app = express();

// MongoDB Connection
mongoose.connect("mongodb+srv://pranavsoma2912_db_user:SpNf6gaC46mAL7Zf@cluster0.x887ggp.mongodb.net/nexuschatbot?retryWrites=true&w=majority")
.then(()=> console.log("MongoDB Connected"))
.catch(err => console.log(err));

// Middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Serve static files
app.use(express.static('static'));

app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: true
}));

// EJS setup
app.set('view engine', 'ejs');
app.set('views', './templates');


// LOGIN PAGE
app.get("/login", (req, res) => {
  res.render("login");
});

// SIGNUP PAGE
app.get("/signup", (req, res) => {
  res.render("signup");
});


// LOGIN ROUTE
app.post('/login', async (req, res) => {

  const { email, password } = req.body;

  try {

    const user = await User.findOne({ email });

    if (!user) {
      return res.send("Invalid email or password");
    }

    const passwordMatch = await bcrypt.compare(password, user.password);

    if (!passwordMatch) {
      return res.send("Invalid email or password");
    }

    req.session.user = user;

    res.redirect("/home");

  } catch (error) {

    res.status(500).send("Server error");

  }

});


// SIGNUP ROUTE
app.post('/signup', async (req, res) => {

  const { email, password } = req.body;

  try {

    const existingUser = await User.findOne({ email });

    if (existingUser) {
      return res.send("User already exists");
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const newUser = new User({
      email,
      password: hashedPassword
    });

    await newUser.save();

    res.redirect("/login");

  } catch (error) {

    res.status(500).send("Server error");

  }

});


// LOGOUT
app.get('/logout', (req, res) => {

  req.session.destroy(() => {
    res.redirect("/login");
  });

});

// Helper function to get auth data
const getAuthData = (req) => {
  if (req.session.user) {
    return {
      username: req.session.user.email.split('@')[0],
      isLoggedIn: true
    };
  } else {
    return {
      username: null,
      isLoggedIn: false
    };
  }
};

// HOME PAGE (with authentication)
app.get("/home", (req, res) => {
  const authData = getAuthData(req);
  if (authData.isLoggedIn) {
    res.render("home", authData);
  } else {
    res.redirect("/login");
  }
});

// ROOT PAGE
app.get("/", (req, res) => {
  const authData = getAuthData(req);
  res.render("home", authData);
});

app.get("/customize_upload", (req, res) => {
  const authData = getAuthData(req);
  res.render("customize_upload", authData);
});

app.get("/choose_model", (req, res) => {
  const authData = getAuthData(req);
  res.render("choose_model", authData);
});

app.get("/customize_chatbot", (req, res) => {
  const authData = getAuthData(req);
  res.render("customize_chatbot", authData);
});

app.get("/bot_builder", (req, res) => {
  const authData = getAuthData(req);
  res.render("bot_builder", authData);
});

app.get("/templates", (req, res) => {
  const authData = getAuthData(req);
  res.render("templates", authData);
});

app.get("/my_bots", (req, res) => {
  const authData = getAuthData(req);
  res.render("my_bots", authData);
});

app.get("/assignments", (req, res) => {
  const authData = getAuthData(req);
  res.render("assignments", authData);
});

app.get("/assignment/:id", (req, res) => {
  const authData = getAuthData(req);
  res.render("assignment_detail", { 
    assignment_id: req.params.id,
    ...authData 
  });
});

// SERVER
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});