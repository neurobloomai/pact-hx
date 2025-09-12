const express = require('express');
const router = express.Router();

module.exports = (integrationServer) => {
  // Get classroom analytics
  router.get('/classroom/:classId', async (req, res) => {
    try {
      const analytics = await integrationServer.orchestrator.getClassroomOverview(req.params.classId);
      res.json({
        success: true,
        analytics,
        message: `📊 Classroom ${req.params.classId} analytics ready!`
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: '😅 Analytics crystal ball is a bit cloudy!',
        error: error.message
      });
    }
  });

  return router;
};
