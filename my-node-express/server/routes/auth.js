// server/routes/authRoutes.js

const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');

router.get('/', authController.showLogin);
router.get('/login', authController.showLogin);
router.post('/login', authController.login);
router.get('/logout', authController.logout);
router.get('/dashboard', authController.dashboard);

module.exports = router;
