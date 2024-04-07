exports.showLogin = (req, res) => {
    res.render('login');
};

exports.login = (req, res) => {
    const { username, password } = req.body;
    const USER = { username: 'admin', password: 'password' };

    if (username === USER.username && password === USER.password) {
        req.session.loggedin = true;
        req.session.username = username;
        res.redirect('/dashboard');
    } else {
        res.send('Incorrect Username and/or Password!');
    }
};

exports.dashboard = (req, res) => {
    if (req.session.loggedin) {
        res.render('dashboard', { username: req.session.username });
    } else {
        res.send('Please login to view this page!');
    }
};

exports.logout = (req, res) => {
    req.session.destroy(() => {
        res.redirect('/');
    });
};