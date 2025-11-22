const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

// 1. Set EJS as the templating engine
app.set('view engine', 'ejs');

// 2. Load "views" from the views directory
app.set('views', path.join(__dirname, 'views'));

// 3. Load static files (CSS/JS) from the "public" directory
// This allows you to link /css/style.css directly in your EJS
app.use(express.static(path.join(__dirname, 'public')));

// Route to render the landing page
app.get('/', (req, res) => {
    res.render('index'); // Looks for views/index.ejs
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});