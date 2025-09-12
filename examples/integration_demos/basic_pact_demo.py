#!/usr/bin/env python3
"""
Pact-HX Integration Demo
========================

A complete working system demonstrating Pact (agreements/contracts) 
with HTMX for dynamic web interactions.

This demo showcases:
- Creating and managing pacts (agreements)
- Real-time updates with HTMX
- User engagement tracking
- Simple contract negotiation flow
"""

from flask import Flask, render_template_string, request, jsonify
from datetime import datetime, timedelta
import json
import uuid
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from enum import Enum

app = Flask(__name__)

# ============================================================================
# Data Models
# ============================================================================

class PactStatus(Enum):
    DRAFT = "draft"
    PROPOSED = "proposed"
    NEGOTIATING = "negotiating"
    ACCEPTED = "accepted"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class PactTerm:
    """Individual term within a pact"""
    id: str
    description: str
    value: str
    negotiable: bool = True
    accepted: bool = False

@dataclass
class Pact:
    """Main pact/agreement structure"""
    id: str
    title: str
    description: str
    creator: str
    participant: Optional[str]
    terms: List[PactTerm]
    status: PactStatus
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None

@dataclass
class EngagementEvent:
    """Track user engagement events"""
    id: str
    pact_id: str
    user: str
    event_type: str  # view, edit, negotiate, accept, etc.
    timestamp: datetime
    metadata: Dict = None

# ============================================================================
# In-Memory Storage (In production, use proper database)
# ============================================================================

pacts_db: Dict[str, Pact] = {}
engagement_db: List[EngagementEvent] = []

# ============================================================================
# Business Logic
# ============================================================================

class PactManager:
    """Core business logic for managing pacts"""
    
    @staticmethod
    def create_pact(title: str, description: str, creator: str, terms_data: List[Dict]) -> Pact:
        """Create a new pact"""
        pact_id = str(uuid.uuid4())[:8]
        
        terms = []
        for term_data in terms_data:
            term = PactTerm(
                id=str(uuid.uuid4())[:8],
                description=term_data.get('description', ''),
                value=term_data.get('value', ''),
                negotiable=term_data.get('negotiable', True)
            )
            terms.append(term)
        
        pact = Pact(
            id=pact_id,
            title=title,
            description=description,
            creator=creator,
            participant=None,
            terms=terms,
            status=PactStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=30)
        )
        
        pacts_db[pact_id] = pact
        return pact
    
    @staticmethod
    def get_pact(pact_id: str) -> Optional[Pact]:
        """Retrieve a pact by ID"""
        return pacts_db.get(pact_id)
    
    @staticmethod
    def update_pact_status(pact_id: str, status: PactStatus, user: str) -> bool:
        """Update pact status"""
        pact = pacts_db.get(pact_id)
        if not pact:
            return False
        
        pact.status = status
        pact.updated_at = datetime.now()
        
        # Log engagement
        EngagementTracker.log_event(pact_id, user, f"status_change_{status.value}")
        return True
    
    @staticmethod
    def negotiate_term(pact_id: str, term_id: str, new_value: str, user: str) -> bool:
        """Negotiate a specific term"""
        pact = pacts_db.get(pact_id)
        if not pact:
            return False
        
        for term in pact.terms:
            if term.id == term_id and term.negotiable:
                term.value = new_value
                pact.status = PactStatus.NEGOTIATING
                pact.updated_at = datetime.now()
                
                EngagementTracker.log_event(pact_id, user, "negotiate_term", 
                                          {"term_id": term_id, "new_value": new_value})
                return True
        
        return False
    
    @staticmethod
    def get_all_pacts() -> List[Pact]:
        """Get all pacts"""
        return list(pacts_db.values())

class EngagementTracker:
    """Track and analyze user engagement"""
    
    @staticmethod
    def log_event(pact_id: str, user: str, event_type: str, metadata: Dict = None):
        """Log an engagement event"""
        event = EngagementEvent(
            id=str(uuid.uuid4())[:8],
            pact_id=pact_id,
            user=user,
            event_type=event_type,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        engagement_db.append(event)
    
    @staticmethod
    def get_pact_engagement(pact_id: str) -> List[EngagementEvent]:
        """Get all engagement events for a pact"""
        return [e for e in engagement_db if e.pact_id == pact_id]
    
    @staticmethod
    def get_engagement_summary(pact_id: str) -> Dict:
        """Get engagement summary for a pact"""
        events = EngagementTracker.get_pact_engagement(pact_id)
        
        event_counts = {}
        users = set()
        
        for event in events:
            event_counts[event.event_type] = event_counts.get(event.event_type, 0) + 1
            users.add(event.user)
        
        return {
            "total_events": len(events),
            "unique_users": len(users),
            "event_breakdown": event_counts,
            "last_activity": max([e.timestamp for e in events]) if events else None
        }

# ============================================================================
# Sample Data Setup
# ============================================================================

def setup_demo_data():
    """Create some sample pacts for the demo"""
    
    # Sample Pact 1: Service Agreement
    PactManager.create_pact(
        title="Website Development Contract",
        description="Agreement for building a modern website with HTMX integration",
        creator="alice",
        terms_data=[
            {"description": "Project Timeline", "value": "6 weeks", "negotiable": True},
            {"description": "Total Cost", "value": "$5,000", "negotiable": True},
            {"description": "Revisions Included", "value": "3 rounds", "negotiable": True},
            {"description": "Source Code Ownership", "value": "Client owns all code", "negotiable": False}
        ]
    )
    
    # Sample Pact 2: Partnership Agreement
    PactManager.create_pact(
        title="Marketing Partnership",
        description="Joint marketing campaign for Q4 product launch",
        creator="bob",
        terms_data=[
            {"description": "Campaign Duration", "value": "3 months", "negotiable": True},
            {"description": "Budget Split", "value": "50/50", "negotiable": True},
            {"description": "Lead Attribution", "value": "First touch", "negotiable": True},
            {"description": "Exclusivity", "value": "Non-exclusive", "negotiable": True}
        ]
    )
    
    # Add some engagement events
    pacts = list(pacts_db.values())
    if pacts:
        pact_id = pacts[0].id
        EngagementTracker.log_event(pact_id, "alice", "view")
        EngagementTracker.log_event(pact_id, "bob", "view")
        EngagementTracker.log_event(pact_id, "bob", "negotiate_term", {"term_id": "timeline"})

# ============================================================================
# Web Routes
# ============================================================================

@app.route('/')
def index():
    """Main dashboard"""
    pacts = PactManager.get_all_pacts()
    return render_template_string(INDEX_TEMPLATE, pacts=pacts)

@app.route('/pact/<pact_id>')
def view_pact(pact_id):
    """View individual pact"""
    pact = PactManager.get_pact(pact_id)
    if not pact:
        return "Pact not found", 404
    
    engagement = EngagementTracker.get_engagement_summary(pact_id)
    EngagementTracker.log_event(pact_id, request.args.get('user', 'anonymous'), 'view')
    
    return render_template_string(PACT_DETAIL_TEMPLATE, pact=pact, engagement=engagement)

@app.route('/pact/<pact_id>/negotiate', methods=['POST'])
def negotiate_term(pact_id):
    """HTMX endpoint for negotiating terms"""
    term_id = request.form.get('term_id')
    new_value = request.form.get('new_value')
    user = request.form.get('user', 'anonymous')
    
    success = PactManager.negotiate_term(pact_id, term_id, new_value, user)
    
    pact = PactManager.get_pact(pact_id)
    term = next((t for t in pact.terms if t.id == term_id), None) if pact else None
    
    if success and term:
        return render_template_string(TERM_COMPONENT, term=term, pact_id=pact_id)
    else:
        return "Failed to negotiate term", 400

@app.route('/pact/<pact_id>/status', methods=['POST'])
def update_status(pact_id):
    """HTMX endpoint for updating pact status"""
    new_status = request.form.get('status')
    user = request.form.get('user', 'anonymous')
    
    try:
        status_enum = PactStatus(new_status)
        success = PactManager.update_pact_status(pact_id, status_enum, user)
        
        if success:
            pact = PactManager.get_pact(pact_id)
            return render_template_string(STATUS_COMPONENT, pact=pact)
        else:
            return "Failed to update status", 400
    except ValueError:
        return "Invalid status", 400

@app.route('/engagement/<pact_id>')
def get_engagement(pact_id):
    """HTMX endpoint for real-time engagement updates"""
    engagement = EngagementTracker.get_engagement_summary(pact_id)
    return render_template_string(ENGAGEMENT_COMPONENT, engagement=engagement)

@app.route('/api/pacts')
def api_pacts():
    """JSON API for pacts (for external integrations)"""
    pacts = PactManager.get_all_pacts()
    return jsonify([asdict(p) for p in pacts])

# ============================================================================
# HTML Templates (Using Jinja2 template strings for simplicity)
# ============================================================================

INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Pact-HX Integration Demo</title>
    <script src="https://unpkg.com/htmx.org@1.9.6"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .pact-card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .status { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .status.draft { background: #e3f2fd; color: #1976d2; }
        .status.active { background: #e8f5e8; color: #2e7d32; }
        .status.negotiating { background: #fff3e0; color: #f57c00; }
        h1 { color: #333; }
        .btn { padding: 8px 16px; margin: 4px; border: none; border-radius: 4px; cursor: pointer; }
        .btn-primary { background: #1976d2; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤝 Pact-HX Integration Demo</h1>
        <p>Dynamic agreement management with real-time updates</p>
        
        <div class="pact-list">
            {% for pact in pacts %}
            <div class="pact-card">
                <h3>{{ pact.title }}</h3>
                <p>{{ pact.description }}</p>
                <p><strong>Creator:</strong> {{ pact.creator }}</p>
                <span class="status {{ pact.status.value }}">{{ pact.status.value.title() }}</span>
                <p><strong>Terms:</strong> {{ pact.terms|length }} items</p>
                <a href="/pact/{{ pact.id }}?user=demo_user" class="btn btn-primary">View Details</a>
            </div>
            {% endfor %}
        </div>
        
        {% if not pacts %}
        <div class="pact-card">
            <h3>No pacts available</h3>
            <p>The demo data hasn't been loaded yet. Restart the server to initialize sample data.</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

PACT_DETAIL_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ pact.title }} - Pact Details</title>
    <script src="https://unpkg.com/htmx.org@1.9.6"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .term { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 4px; }
        .term.negotiable { border-left: 4px solid #4caf50; }
        .term.non-negotiable { border-left: 4px solid #f44336; }
        .status { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .status.draft { background: #e3f2fd; color: #1976d2; }
        .status.negotiating { background: #fff3e0; color: #f57c00; }
        .btn { padding: 8px 16px; margin: 4px; border: none; border-radius: 4px; cursor: pointer; }
        .btn-primary { background: #1976d2; color: white; }
        .btn-success { background: #4caf50; color: white; }
        .engagement { background: #f8f9fa; padding: 10px; border-radius: 4px; }
        input[type="text"] { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        .back-link { color: #1976d2; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-link">← Back to Dashboard</a>
        
        <div class="card">
            <h1>{{ pact.title }}</h1>
            <p>{{ pact.description }}</p>
            
            <div id="status-container">
                <p><strong>Status:</strong> <span class="status {{ pact.status.value }}">{{ pact.status.value.title() }}</span></p>
            </div>
            
            <p><strong>Creator:</strong> {{ pact.creator }}</p>
            <p><strong>Created:</strong> {{ pact.created_at.strftime('%Y-%m-%d %H:%M') }}</p>
            {% if pact.expires_at %}
            <p><strong>Expires:</strong> {{ pact.expires_at.strftime('%Y-%m-%d') }}</p>
            {% endif %}
        </div>
        
        <div class="card">
            <h2>Terms & Conditions</h2>
            <div id="terms-container">
                {% for term in pact.terms %}
                <div id="term-{{ term.id }}" class="term {{ 'negotiable' if term.negotiable else 'non-negotiable' }}">
                    <h4>{{ term.description }}</h4>
                    <p><strong>Value:</strong> <span id="term-value-{{ term.id }}">{{ term.value }}</span></p>
                    {% if term.negotiable %}
                    <div style="margin-top: 10px;">
                        <input type="text" id="new-value-{{ term.id }}" value="{{ term.value }}" placeholder="Enter new value">
                        <button class="btn btn-primary" 
                                hx-post="/pact/{{ pact.id }}/negotiate"
                                hx-vals='{"term_id": "{{ term.id }}", "user": "demo_user"}'
                                hx-include="#new-value-{{ term.id }}"
                                hx-target="#term-{{ term.id }}"
                                hx-swap="outerHTML">
                            Negotiate
                        </button>
                    </div>
                    <small style="color: #4caf50;">✓ Negotiable</small>
                    {% else %}
                    <small style="color: #f44336;">✗ Non-negotiable</small>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="card">
            <h2>Actions</h2>
            {% if pact.status.value == 'draft' %}
            <button class="btn btn-primary"
                    hx-post="/pact/{{ pact.id }}/status"
                    hx-vals='{"status": "proposed", "user": "demo_user"}'
                    hx-target="#status-container"
                    hx-trigger="click">
                Propose Pact
            </button>
            {% elif pact.status.value == 'proposed' %}
            <button class="btn btn-success"
                    hx-post="/pact/{{ pact.id }}/status"
                    hx-vals='{"status": "accepted", "user": "demo_user"}'
                    hx-target="#status-container">
                Accept Pact
            </button>
            <button class="btn btn-primary"
                    hx-post="/pact/{{ pact.id }}/status"
                    hx-vals='{"status": "negotiating", "user": "demo_user"}'
                    hx-target="#status-container">
                Start Negotiation
            </button>
            {% endif %}
        </div>
        
        <div class="card">
            <h2>Engagement Analytics</h2>
            <div id="engagement-container" 
                 hx-get="/engagement/{{ pact.id }}" 
                 hx-trigger="load, every 5s">
                <div class="engagement">
                    <p><strong>Total Events:</strong> {{ engagement.total_events }}</p>
                    <p><strong>Unique Users:</strong> {{ engagement.unique_users }}</p>
                    {% if engagement.last_activity %}
                    <p><strong>Last Activity:</strong> {{ engagement.last_activity.strftime('%Y-%m-%d %H:%M:%S') }}</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

TERM_COMPONENT = '''
<div id="term-{{ term.id }}" class="term negotiable">
    <h4>{{ term.description }}</h4>
    <p><strong>Value:</strong> <span id="term-value-{{ term.id }}">{{ term.value }}</span> <em style="color: #4caf50;">(Updated!)</em></p>
    <div style="margin-top: 10px;">
        <input type="text" id="new-value-{{ term.id }}" value="{{ term.value }}" placeholder="Enter new value">
        <button class="btn btn-primary" 
                hx-post="/pact/{{ pact_id }}/negotiate"
                hx-vals='{"term_id": "{{ term.id }}", "user": "demo_user"}'
                hx-include="#new-value-{{ term.id }}"
                hx-target="#term-{{ term.id }}"
                hx-swap="outerHTML">
            Negotiate
        </button>
    </div>
    <small style="color: #4caf50;">✓ Negotiable</small>
</div>
'''

STATUS_COMPONENT = '''
<p><strong>Status:</strong> <span class="status {{ pact.status.value }}">{{ pact.status.value.title() }}</span> <em style="color: #4caf50;">(Updated!)</em></p>
'''

ENGAGEMENT_COMPONENT = '''
<div class="engagement">
    <p><strong>Total Events:</strong> {{ engagement.total_events }}</p>
    <p><strong>Unique Users:</strong> {{ engagement.unique_users }}</p>
    {% if engagement.last_activity %}
    <p><strong>Last Activity:</strong> {{ engagement.last_activity.strftime('%Y-%m-%d %H:%M:%S') }}</p>
    {% endif %}
    {% if engagement.event_breakdown %}
    <p><strong>Event Breakdown:</strong></p>
    <ul>
    {% for event_type, count in engagement.event_breakdown.items() %}
        <li>{{ event_type.replace('_', ' ').title() }}: {{ count }}</li>
    {% endfor %}
    </ul>
    {% endif %}
</div>
'''

# ============================================================================
# Main Application Entry Point
# ============================================================================

if __name__ == '__main__':
    # Set up demo data
    setup_demo_data()
    
    print("🚀 Starting Pact-HX Integration Demo...")
    print("📊 Sample pacts created")
    print("🌐 Visit: http://localhost:5000")
    print("🔗 API available at: http://localhost:5000/api/pacts")
    print("\n" + "="*50)
    print("Demo Features:")
    print("• View pacts with real-time status")
    print("• Negotiate terms with HTMX updates")
    print("• Track engagement analytics")
    print("• Dynamic status transitions")
    print("="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
