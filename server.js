const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = 3000;

// Hashmap to store user data
const users = new Map();

app.use(bodyParser.json());

// Serve static files from the 'pages' directory
app.use(express.static(path.join(__dirname, 'pages')));

// Pages
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'pages', 'index.html'));
});
app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'pages', 'login.html'));
});
app.get('/register', (req, res) => {
    res.sendFile(path.join(__dirname, 'pages', 'register.html'));
});
app.get('/home', (req, res) => {
    res.sendFile(path.join(__dirname, 'pages', 'home.html'));
});

app.post('/register', (req, res) => {
    const { username, password } = req.body;
    users.set(username, password);
    res.sendStatus(200);
});

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    if (users.has(username) && users.get(username) === password) {
        res.sendStatus(200);
    } else {
        res.sendStatus(401);
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

