# 🔌 PACT API Specification v1.0

## Base URL
```
Production: https://api.neurobloom.ai/pact/v1
Staging:    https://api-staging.neurobloom.ai/pact/v1
```

---

## Authentication

All endpoints require API key in header:
```http
Authorization: Bearer sk_test_abc123...
```

---

## API Endpoints

### 1. Create Session

**Create a new conversation session**

```http
POST /sessions
```

**Request:**
```json
{
  "metadata": {
    "user_id": "optional_user_id",
    "application": "optional_app_name"
  }
}
```

**Response:** `201 Created`
```json
{
  "session_id": "sess_abc123xyz",
  "created_at": "2025-11-10T10:30:00Z",
  "status": "active"
}
```

---

### 2. Get Context

**Retrieve conversation context with emotional metadata**

```http
GET /sessions/{session_id}/context
```

**Query Parameters:**
- `max_tokens` (int, optional) - Max tokens to return (default: 2000)
- `include_emotional` (bool, optional) - Include emotional data (default: true)

**Response:** `200 OK`
```json
{
  "session_id": "sess_abc123xyz",
  "messages": [
    {
      "id": "msg_001",
      "role": "user",
      "content": "I'm really frustrated with this issue",
      "timestamp": "2025-11-10T10:31:00Z",
      "emotional_metadata": {
        "detected_emotion": "frustrated",
        "confidence": 0.87
      }
    },
    {
      "id": "msg_002",
      "role": "assistant",
      "content": "I understand your frustration. Let's solve this together.",
      "timestamp": "2025-11-10T10:31:05Z"
    }
  ],
  "emotional_state": "frustrated",
  "consolidated_summary": "User is experiencing frustration with a technical issue",
  "token_count": 156
}
```

---

### 3. Save Interaction

**Save a conversation turn (user message + AI response)**

```http
POST /sessions/{session_id}/interactions
```

**Request:**
```json
{
  "user_message": "I'm really frustrated with this issue",
  "ai_message": "I understand your frustration. Let's solve this together.",
  "track_emotion": true,
  "consolidate": true
}
```

**Response:** `201 Created`
```json
{
  "interaction_id": "int_xyz789",
  "emotional_analysis": {
    "user_emotion": "frustrated",
    "valence": 0.25,
    "arousal": 0.72,
    "trend": "negative"
  },
  "consolidation_triggered": false,
  "token_count": 23
}
```

---

### 4. Get Emotional State

**Get current emotional analysis for session**

```http
GET /sessions/{session_id}/emotional_state
```

**Response:** `200 OK`
```json
{
  "session_id": "sess_abc123xyz",
  "current_emotion": "frustrated",
  "valence": 0.25,
  "arousal": 0.72,
  "trend": "negative",
  "key_emotions": [
    {"emotion": "frustrated", "intensity": 0.87},
    {"emotion": "confused", "intensity": 0.45}
  ],
  "emotional_history": [
    {"timestamp": "2025-11-10T10:30:00Z", "emotion": "neutral"},
    {"timestamp": "2025-11-10T10:31:00Z", "emotion": "frustrated"}
  ]
}
```

---

### 5. Get Memory Graph

**Get conversation memory as node/edge graph**

```http
GET /sessions/{session_id}/graph
```

**Response:** `200 OK`
```json
{
  "session_id": "sess_abc123xyz",
  "nodes": [
    {
      "id": "node_msg_001",
      "type": "message",
      "content": "I'm frustrated with this issue",
      "importance": 0.85,
      "emotional_tag": "frustrated"
    },
    {
      "id": "node_topic_001",
      "type": "topic",
      "content": "technical issue",
      "importance": 0.92
    }
  ],
  "edges": [
    {
      "from": "node_msg_001",
      "to": "node_topic_001",
      "type": "mentions",
      "weight": 0.88
    }
  ],
  "metadata": {
    "total_nodes": 15,
    "total_edges": 23,
    "depth": 4
  }
}
```

---

### 6. Force Consolidation

**Manually trigger context consolidation**

```http
POST /sessions/{session_id}/consolidate
```

**Request:** (empty body)

**Response:** `200 OK`
```json
{
  "session_id": "sess_abc123xyz",
  "consolidation_result": {
    "messages_before": 24,
    "messages_after": 8,
    "tokens_saved": 1532,
    "consolidated_summary": "User discussed technical issues with authentication, experienced frustration, then found solution and expressed relief.",
    "preserved_highlights": [
      "Authentication problem identified",
      "Solution implemented successfully"
    ]
  },
  "timestamp": "2025-11-10T10:35:00Z"
}
```

---

### 7. Set Context Priority

**Set priority level for a topic**

```http
POST /sessions/{session_id}/priority
```

**Request:**
```json
{
  "topic": "authentication_issue",
  "priority": "high"
}
```

**Response:** `200 OK`
```json
{
  "session_id": "sess_abc123xyz",
  "topic": "authentication_issue",
  "priority": "high",
  "updated_at": "2025-11-10T10:36:00Z"
}
```

---

### 8. Delete Session

**Delete a session and all associated data**

```http
DELETE /sessions/{session_id}
```

**Response:** `204 No Content`

---

### 9. Health Check

**Check API health**

```http
GET /health
```

**Response:** `200 OK`
```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2025-11-10T10:30:00Z",
  "services": {
    "database": "healthy",
    "cache": "healthy",
    "llm_api": "healthy"
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": {
    "code": "invalid_request",
    "message": "Missing required field: user_message",
    "details": {
      "field": "user_message",
      "received": null
    }
  }
}
```

### 401 Unauthorized
```json
{
  "error": {
    "code": "unauthorized",
    "message": "Invalid API key"
  }
}
```

### 404 Not Found
```json
{
  "error": {
    "code": "not_found",
    "message": "Session not found: sess_abc123"
  }
}
```

### 429 Too Many Requests
```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Try again in 60 seconds.",
    "retry_after": 60
  }
}
```

### 500 Internal Server Error
```json
{
  "error": {
    "code": "internal_error",
    "message": "An unexpected error occurred",
    "request_id": "req_xyz789"
  }
}
```

---

## Rate Limits

### By Plan:

| Plan | Requests/Minute | Requests/Hour | Requests/Day |
|------|----------------|---------------|--------------|
| Free | 10 | 100 | 1,000 |
| Starter | 60 | 1,000 | 10,000 |
| Pro | 300 | 10,000 | 100,000 |
| Team | 1,000 | 50,000 | Unlimited |

**Rate Limit Headers:**
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1699612800
```

---

## WebSocket API (Future)

**For real-time updates:**

```javascript
ws://api.neurobloom.ai/pact/v1/sessions/{session_id}/stream

// Subscribe to emotional state changes
{
  "type": "subscribe",
  "events": ["emotional_state_changed", "consolidation_triggered"]
}
```

---

## SDK Examples

### Python
```python
from pact_client import PACTClient

client = PACTClient(api_key="sk_test_...")
session = client.create_session()

client.save_interaction(
    session_id=session.id,
    user_message="I'm frustrated",
    ai_message="I understand"
)

state = client.get_emotional_state(session.id)
print(state.current_emotion)  # "frustrated"
```

### JavaScript/TypeScript
```typescript
import { PACTClient } from '@neurobloom/pact-client';

const client = new PACTClient({ apiKey: 'sk_test_...' });
const session = await client.createSession();

await client.saveInteraction(session.id, {
  userMessage: "I'm frustrated",
  aiMessage: "I understand"
});

const state = await client.getEmotionalState(session.id);
console.log(state.currentEmotion); // "frustrated"
```

---

## Implementation Notes

### Emotional Analysis

**Models to Use:**
- Primary: OpenAI GPT-3.5-turbo (fast, cheap)
- Alternative: Anthropic Claude Haiku
- Fallback: Local sentiment model (BERT-based)

**Prompt Template:**
```
Analyze the emotional content of this message:
"{user_message}"

Return JSON:
{
  "emotion": "primary emotion (frustrated, happy, sad, etc.)",
  "valence": float between 0-1 (negative to positive),
  "arousal": float between 0-1 (calm to excited),
  "confidence": float between 0-1
}
```

### Context Consolidation

**When to Trigger:**
- After N messages (configurable, default: 10)
- When token count exceeds threshold (configurable, default: 2000)
- Manual trigger via API

**How to Consolidate:**
1. Extract key topics
2. Identify emotional highlights
3. Summarize with LLM
4. Preserve high-importance messages
5. Archive originals to S3

---

## Testing

### Test API Keys

```
Development: sk_test_dev_abc123...
Staging:     sk_test_staging_xyz789...
Production:  sk_prod_real_key...
```

### Test Session

```bash
curl -X POST https://api.neurobloom.ai/pact/v1/sessions \
  -H "Authorization: Bearer sk_test_dev_abc123" \
  -H "Content-Type: application/json"
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-10 | Initial specification |

---

**Ready for implementation! 🚀**

Next: [AWS Deployment Checklist](./AWS_DEPLOYMENT_CHECKLIST.md)
