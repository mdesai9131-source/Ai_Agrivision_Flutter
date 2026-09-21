const express = require('express');
const router = express.Router();
const { getNearbyAgroSupport } = require('../controllers/agroController');
const { protectWithGuestFallback } = require('../middleware/authMiddleware');

router.use(protectWithGuestFallback);

router.get('/nearby', getNearbyAgroSupport);

module.exports = router;
