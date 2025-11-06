# Using AX Substrate: Story Keeper

**Document Location:** `pact-hx/primitives/memory/using_ax_substrate.md`

**Audience:** HX layer developers building user-facing primitives

**Purpose:** Guide for using Story Keeper (AX substrate) to build Memory primitive and other HX capabilities

---

## Overview

The Memory primitive in HX layer provides user-facing relationship continuity. Rather than building memory from scratch, it leverages **Story Keeper** from the AX layer as its substrate.

This document shows you how to use Story Keeper to build robust HX primitives.

---

## Why Use AX Substrate?

### Benefits

1. **Shared Foundation:** User and agent coordination share same narrative
2. **Consistency:** No sync issues between layers
3. **Integration:** User sees agent coordination naturally
4. **Efficiency:** Don't rebuild what AX already provides

### What Story Keeper Provides

From AX layer, Story Keeper gives you:

- ✅ Narrative continuity across all interactions
- ✅ Event storage with timestamps and metadata
- ✅ Flexible querying by layer, type, time
- ✅ Event subscription for reactive updates

You build on top of this to create user-facing experiences.

---

## Basic Usage Pattern

### 1. Import and Initialize

```python
from pact_ax.primitives import StoryKeeper

class UserMemory:
    """HX primitive for user relationship memory"""
    
    def __init__(self, story_keeper):
        # Use existing Story Keeper instance
        self.story = story_keeper
        
        # Subscribe to relevant events
        self.story.register_listener("hx", self._on_hx_event)
```

### 2. Write User-Facing Events

```python
class UserMemory:
    def remember_preference(self, preference, category=None):
        """
        Store user preference in narrative
        
        User-facing method that writes to Story Keeper
        """
        self.story.add_event(
            event=f"User preference: {preference}",
            layer="hx",  # Mark as HX layer event
            event_type="preference",
            metadata={
                'preference': preference,
                'category': category,
                'confidence': 1.0,  # Explicitly stated
                'source': 'user_direct'
            }
        )
    
    def remember_interaction(self, interaction_summary):
        """Record significant user interaction"""
        self.story.add_event(
            event=interaction_summary,
            layer="hx",
            event_type="interaction",
            metadata={
                'timestamp': now(),
                'session_id': self.session_id
            }
        )
```

### 3. Read User Context

```python
class UserMemory:
    def recall_preferences(self, category=None):
        """
        Retrieve stored user preferences
        
        User-facing method that reads from Story Keeper
        """
        # Get all HX preference events
        events = self.story.get_narrative(
            filter_layer="hx",
            filter_type="preference"
        )
        
        # Filter by category if specified
        if category:
            events = [e for e in events 
                     if e['metadata'].get('category') == category]
        
        # Extract preferences
        preferences = [e['metadata']['preference'] for e in events]
        return preferences
    
    def get_recent_context(self, limit=10):
        """Get recent user interaction history"""
        events = self.story.get_narrative(
            filter_layer="hx",
            filter_type="interaction",
            limit=limit
        )
        return events
```

---

## Advanced Patterns

### Pattern 1: Reactive Updates

Subscribe to Story Keeper events to update HX primitive state.

```python
class UserMemory:
    def __init__(self, story_keeper):
        self.story = story_keeper
        self.preference_cache = {}
        
        # React to new preference events
        self.story.register_listener("hx", self._on_hx_event)
    
    def _on_hx_event(self, layer, event_type):
        """Called whenever HX event added to Story Keeper"""
        if event_type == "preference":
            # Update cache immediately
            self._refresh_preference_cache()
    
    def _refresh_preference_cache(self):
        """Rebuild preference cache from Story Keeper"""
        prefs = self.story.get_narrative(
            filter_layer="hx",
            filter_type="preference"
        )
        
        for event in prefs:
            category = event['metadata'].get('category', 'general')
            pref = event['metadata']['preference']
            
            if category not in self.preference_cache:
                self.preference_cache[category] = []
            self.preference_cache[category].append(pref)
```

---

### Pattern 2: Cross-Layer Awareness

Use both HX and AX events to provide richer user experience.

```python
class UserMemory:
    def get_full_context_for_user(self):
        """
        Show user BOTH their preferences AND agent coordination
        
        This creates transparency and trust
        """
        # Get user preferences (HX layer)
        preferences = self.story.get_narrative(
            filter_layer="hx",
            filter_type="preference"
        )
        
        # Get agent coordination events (AX layer)
        agent_events = self.story.get_narrative(
            filter_layer="ax",
            filter_type="coordination"
        )
        
        # Combine for user-facing display
        return {
            'your_preferences': self._format_for_user(preferences),
            'how_agents_coordinated': self._format_for_user(agent_events),
            'message': 'Here's how the system adapted to you'
        }
    
    def _format_for_user(self, events):
        """Convert technical events to user-friendly format"""
        return [
            {
                'when': event['timestamp'],
                'what': event['event'],
                'why': self._explain_significance(event)
            }
            for event in events
        ]
```

---

### Pattern 3: Learning from Patterns

Analyze Story Keeper narrative to infer implicit preferences.

```python
class UserMemory:
    def infer_implicit_preferences(self):
        """
        Learn preferences from interaction patterns
        
        Not explicitly stated, but evident from behavior
        """
        # Get all user interactions
        interactions = self.story.get_narrative(
            filter_layer="hx",
            filter_type="interaction"
        )
        
        # Analyze patterns
        patterns = self._analyze_interaction_patterns(interactions)
        
        # Store inferred preferences
        for pattern in patterns:
            if pattern['confidence'] > 0.7:  # High confidence only
                self.remember_preference(
                    preference=pattern['preference'],
                    category='inferred'
                )
    
    def _analyze_interaction_patterns(self, interactions):
        """Detect patterns in user behavior"""
        patterns = []
        
        # Example: User always interacts in morning
        morning_count = sum(1 for i in interactions 
                          if self._is_morning(i['timestamp']))
        
        if morning_count / len(interactions) > 0.8:
            patterns.append({
                'preference': 'prefers morning interactions',
                'confidence': morning_count / len(interactions),
                'evidence': f'{morning_count}/{len(interactions)} interactions in morning'
            })
        
        return patterns
```

---

## Integration with Other HX Primitives

### Example: Memory + Tone Adapt

Memory primitive informs tone adaptation.

```python
# memory.py (HX primitive)
class UserMemory:
    def get_emotional_history(self):
        """Get user emotional state history"""
        return self.story.get_narrative(
            filter_layer="hx",
            filter_type="emotional_state"
        )

# tone_adapt.py (HX primitive)
class ToneAdapter:
    def __init__(self, story_keeper, user_memory):
        self.story = story_keeper
        self.memory = user_memory
    
    def adapt_response(self, content, current_state):
        """
        Adapt tone based on user's emotional history
        
        Uses Memory primitive which uses Story Keeper
        """
        # Get emotional context from memory
        history = self.memory.get_emotional_history()
        
        # User recently stressed? Be more supportive
        recent_stress = any(e['metadata'].get('state') == 'stressed' 
                          for e in history[-5:])
        
        if recent_stress:
            content = self._make_more_supportive(content)
        
        # Record the adaptation
        self.story.add_event(
            event=f"Adapted tone: supportive (user stress detected)",
            layer="hx",
            event_type="adaptation",
            metadata={'reason': 'recent_stress'}
        )
        
        return content
```

---

## Complete Example: Memory Primitive

```python
# pact-hx/primitives/memory/memory.py

from pact_ax.primitives import StoryKeeper
from datetime import datetime

class UserMemory:
    """
    HX Layer: User relationship memory
    
    Built on Story Keeper (AX substrate)
    """
    
    def __init__(self, story_keeper: StoryKeeper):
        """
        Initialize with Story Keeper instance
        
        Args:
            story_keeper: Existing Story Keeper from AX layer
        """
        self.story = story_keeper
        self.preference_cache = {}
        
        # Subscribe to HX events
        self.story.register_listener("hx", self._on_hx_event)
        
        # Initialize cache
        self._refresh_preference_cache()
    
    # === User-Facing API ===
    
    def remember(self, what, category="general"):
        """
        Remember something about the user
        
        User-facing method for storing preferences/facts
        """
        self.story.add_event(
            event=f"User: {what}",
            layer="hx",
            event_type="preference",
            metadata={
                'content': what,
                'category': category,
                'confidence': 1.0,
                'source': 'explicit'
            }
        )
    
    def recall(self, category=None):
        """
        Recall what we know about the user
        
        User-facing method for retrieving memory
        """
        if category:
            return self.preference_cache.get(category, [])
        else:
            return self.preference_cache
    
    def show_to_user(self):
        """
        Generate user-facing summary of what system remembers
        
        This creates transparency
        """
        summary = []
        
        for category, prefs in self.preference_cache.items():
            summary.append({
                'category': category,
                'what_we_remember': prefs,
                'how_many': len(prefs)
            })
        
        return {
            'memory_summary': summary,
            'total_preferences': sum(len(p) for p in self.preference_cache.values()),
            'message': 'Here's what I remember about you'
        }
    
    # === Internal Methods ===
    
    def _on_hx_event(self, layer, event_type):
        """React to new HX events in Story Keeper"""
        if event_type == "preference":
            self._refresh_preference_cache()
    
    def _refresh_preference_cache(self):
        """Rebuild cache from Story Keeper narrative"""
        events = self.story.get_narrative(
            filter_layer="hx",
            filter_type="preference"
        )
        
        self.preference_cache = {}
        for event in events:
            metadata = event['metadata']
            category = metadata.get('category', 'general')
            content = metadata.get('content', event['event'])
            
            if category not in self.preference_cache:
                self.preference_cache[category] = []
            
            self.preference_cache[category].append(content)

# === Usage Example ===

# Initialize with Story Keeper
story = StoryKeeper()
memory = UserMemory(story)

# User interaction
memory.remember("I prefer morning reflections", category="timing")
memory.remember("I like data-first explanations", category="communication")

# Later retrieval
timing_prefs = memory.recall(category="timing")
# → ["I prefer morning reflections"]

# Show to user
summary = memory.show_to_user()
# → User sees what system remembers about them
```

---

## Best Practices

### 1. Always Tag with "hx" Layer

```python
# ✅ Good: Clearly marked as HX
self.story.add_event(
    "User preference",
    layer="hx",  # Explicit
    event_type="preference"
)

# ❌ Bad: Default layer might be "ax"
self.story.add_event(
    "User preference",
    event_type="preference"
)
```

### 2. Use Descriptive Event Types

```python
# ✅ Good: Clear event types
event_type="preference"      # User preference
event_type="interaction"     # User interaction
event_type="emotional_state" # Emotional state

# ❌ Bad: Generic types
event_type="default"
event_type="other"
```

### 3. Include Rich Metadata

```python
# ✅ Good: Rich context
metadata={
    'preference': "morning interactions",
    'category': "timing",
    'confidence': 0.9,
    'source': 'inferred',
    'evidence': "8/10 interactions before 10am"
}

# ❌ Bad: Minimal metadata
metadata={'pref': "morning"}
```

### 4. Cache for Performance

```python
# ✅ Good: Cache frequently accessed data
class UserMemory:
    def __init__(self, story_keeper):
        self.story = story_keeper
        self.cache = self._build_cache()
    
    def _build_cache(self):
        # Build cache once
        pass

# ❌ Bad: Query Story Keeper every time
class UserMemory:
    def recall(self):
        return self.story.get_narrative(...)  # Slow on every call
```

---

## Testing

```python
def test_memory_uses_story_keeper():
    """Memory primitive correctly uses Story Keeper substrate"""
    story = StoryKeeper()
    memory = UserMemory(story)
    
    # Store preference
    memory.remember("likes detailed explanations")
    
    # Verify it's in Story Keeper (HX layer)
    hx_events = story.get_narrative(filter_layer="hx")
    assert len(hx_events) == 1
    assert "detailed explanations" in hx_events[0]['event']
    
    # Verify memory can retrieve it
    prefs = memory.recall()
    assert "likes detailed explanations" in prefs['general']

def test_memory_isolates_hx_layer():
    """Memory only sees HX events, not AX events"""
    story = StoryKeeper()
    memory = UserMemory(story)
    
    # Add AX event (agent coordination)
    story.add_event("Agent handoff", layer="ax")
    
    # Add HX event (user preference)
    memory.remember("user preference")
    
    # Memory should only see HX events
    prefs = memory.recall()
    assert len(prefs['general']) == 1
    assert "Agent handoff" not in str(prefs)
```

---

## Troubleshooting

### Issue: Events Not Appearing

**Problem:** Added event but can't retrieve it

**Solution:** Check layer filtering

```python
# Make sure you're filtering correctly
events = story.get_narrative(filter_layer="hx")  # Specify layer!
```

### Issue: Performance Problems

**Problem:** Slow retrieval with many events

**Solution:** Use caching and limit queries

```python
# Cache frequently accessed data
self.cache = self._build_cache()

# Limit query size
recent = story.get_narrative(filter_layer="hx", limit=100)
```

### Issue: Events Mixing Between Layers

**Problem:** Seeing AX events in HX queries

**Solution:** Always specify layer filter

```python
# ✅ Good: Explicit filtering
events = story.get_narrative(filter_layer="hx")

# ❌ Bad: No filtering (gets all layers)
events = story.get_narrative()
```

---

## Related Documentation

- **Architecture Overview:** `pact/docs/architecture/hx_ax_integration.md`
- **Story Keeper Docs:** `pact-ax/primitives/story_keeper/README.md`
- **AX Extension Guide:** `pact-ax/primitives/story_keeper/extending_to_hx.md`

---

## Key Takeaways

1. **HX primitives build on AX substrate (Story Keeper)**
2. **Always tag events with "hx" layer**
3. **Use event types and metadata richly**
4. **Cache for performance**
5. **Subscribe to events for reactivity**
6. **Show transparency to users (cross-layer awareness)**

---

**Document Version:** 1.0  
**Last Updated:** November 2025  
**Maintainer:** PACT-HX Team
