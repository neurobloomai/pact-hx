const express = require('express');
const router = express.Router();

module.exports = (integrationServer) => {
  // GET participant profile
  router.get('/:participantId/profile', async (req, res) => {
    try {
      const profile = await integrationServer.dataCoordinator.getUnifiedParticipantProfile(req.params.participantId);
      res.json({
        success: true,
        profile,
        message: `✨ Here's ${req.params.participantId}'s learning profile!`
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
