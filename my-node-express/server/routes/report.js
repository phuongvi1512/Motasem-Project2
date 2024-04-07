const express = require('express');
const router = express.Router();
const reportController = require('../controllers/reportController');

// Routes
router.get('/', reportController.view);
router.get('/addreport', reportController.form);
router.post('/addreport', reportController.create);
  
module.exports = router;