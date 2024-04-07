const express = require('express');
const exphbs = require('express-handlebars'); // updated to 6.0.X
//const bodyParser = require('body-parser');  // Remove
//const mysql = require('mysql'); // Remove
const session = require('express-session')
const path = require('path');

require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// Parsing middleware
// Parse application/x-www-form-urlencoded
// app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.urlencoded({extended: true}), session({secret: 'your_secret_key_here', resave: false, saveUninitialized: true})); // New

// Parse application/json
// app.use(bodyParser.json());
app.use(express.json()); // New

// Static Files
app.use(express.static('public'));

// Templating engine
// app.engine('hbs', exphbs({ extname: '.hbs' })); // v5.3.4
// app.set('view engine', 'hbs'); // v5.3.4

// Update to 6.0.X
const handlebars = exphbs.create({ 
    extname: '.hbs',
    defaultLayout: 'main',
    // Specify the directory where your partials are located
    partialsDir: path.join(__dirname, 'views/partials'),
    });
app.engine('.hbs', handlebars.engine);
app.set('view engine', '.hbs');

// Connection Pool
// You don't need the connection here as we have it in userController
// let connection = mysql.createConnection({
//   host: process.env.DB_HOST,
//   user: process.env.DB_USER,
//   password: process.env.DB_PASS,
//   database: process.env.DB_NAME
// });

// Display the login form
// app.get('/login', (req, res) => {
//     res.render('login');
// });

// Handle login
// app.post('/login', (req, res) => {
//     const { username, password } = req.body;
//     // Hardcoded user for demonstration. Replace with database lookup in real application.
//     const USER = {
//         username: 'admin',
//         password: 'password'
//     };

//     if (username === USER.username && password === USER.password) {
//         req.session.loggedin = true;
//         req.session.username = username;
//         res.redirect('/dashboard');
//     } else {
//         res.send('Incorrect Username and/or Password!');
//     }
// });
const authRoutes = require('./server/routes/auth');
app.use('/', authRoutes);
const routes = require('./server/routes/report');
app.use('/report', routes);

app.listen(port, () => console.log(`Listening on port ${port}`));