const express = require('express');
const router = express.Router();

module.exports = (integrationServer) => {
  // GET student profile
  router.get('/:studentId/profile', async (req, res) => {
    try {
      const profile = await integrationServer.dataCoordinator.getUnifiedStudentProfile(req.params.studentId);
      res.json({
        success: true,
        profile,
        message: `✨ Here's ${req.params.studentId}'s learning profile!`
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: '😅 Profile loading hit a small snag!',
        error: error.message
      });
    }
  });

  return router;
};
