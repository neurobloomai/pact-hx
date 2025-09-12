const express = require('express');
const router = express.Router();

module.exports = (integrationServer) => {
  // Trigger manual adaptation
  router.post('/trigger', async (req, res) => {
    try {
      const adaptation = await integrationServer.adaptationEngine.processAdaptationRequest(req.body);
      res.json({
        success: true,
        adaptation,
        message: '🎨 Magical adaptation created!'
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: '😅 Adaptation magic needs a moment!',
        error: error.message
      });
    }
  });

  return router;
};
