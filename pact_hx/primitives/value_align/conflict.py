"""
pact_hx/primitives/value_align/conflict.py

ConflictDetector — detects value conflicts from domain assessment scores and
executes resolution strategies on behalf of ValueAlignmentManager.

Extracted from the manager so conflict logic is independently testable and the
manager can delegate rather than inline it.  All mutations go through the shared
ValueAlignmentState reference, so the manager's view stays in sync.
"""

from typing import Any, Dict, List, Optional, Tuple

from .schemas import (
    ConflictResolution,
    ConflictSeverity,
    ValueConflict,
    ValueDomain,
    ValueAlignmentState,
)


class ConflictDetector:
    """
    Detect, create, and resolve value conflicts from domain assessment scores.

    Instantiate with the same ValueAlignmentState the manager owns; every
    conflict this class registers or updates is immediately visible to the
    manager through the shared state object.
    """

    def __init__(self, state: ValueAlignmentState) -> None:
        self._state = state

    # ── Detection ────────────────────────────────────────────────────────────

    def detect(
        self,
        proposed_action: str,
        context: str,
        domain_assessments: Dict[ValueDomain, float],
    ) -> List[Tuple[str, ConflictSeverity]]:
        """Return (conflict_id, severity) for every below-threshold domain."""
        results: List[Tuple[str, ConflictSeverity]] = []
        for domain, score in domain_assessments.items():
            if score < self._state.config.conflict_threshold:
                conflict = self.create_conflict(domain, score, proposed_action, context)
                if conflict is not None:
                    results.append((conflict.conflict_id, conflict.severity))
        return results

    def create_conflict(
        self,
        domain: ValueDomain,
        score: float,
        proposed_action: str,
        context: str,
    ) -> Optional[ValueConflict]:
        """Build and register a ValueConflict for a below-threshold domain.

        Returns None when the adjusted score is not significant enough to
        warrant a conflict record.
        """
        user_importance = self._state.get_domain_importance(domain)
        adjusted = score * user_importance

        if adjusted < 0.2:
            severity = ConflictSeverity.SEVERE
        elif adjusted < 0.4:
            severity = ConflictSeverity.MODERATE
        elif adjusted < 0.6:
            severity = ConflictSeverity.MILD
        else:
            return None

        domain_constraints = [
            c for c in self._state.active_constraints.values()
            if c.domain == domain
        ]
        primary = domain_constraints[0] if domain_constraints else None

        conflict = ValueConflict(
            severity=severity,
            conflict_type=f"{domain.value}_alignment_low",
            primary_constraint=primary.constraint_id if primary else "",
            proposed_action=proposed_action,
            context_description=context[:200],
            conflict_details=(
                f"Action may not align well with {domain.value} values "
                f"(score: {score:.2f})"
            ),
            suggested_resolution=self.suggest_resolution(domain, severity, score),
            resolution_confidence=0.7,
        )

        self._state.active_conflicts[conflict.conflict_id] = conflict
        self._state.total_conflicts_detected += 1
        return conflict

    def suggest_resolution(
        self,
        domain: ValueDomain,
        severity: ConflictSeverity,
        score: float,  # kept for API symmetry with older call sites
    ) -> ConflictResolution:
        """Return the most appropriate resolution strategy for this domain/severity."""
        if domain in (ValueDomain.SAFETY, ValueDomain.PRIVACY):
            if severity == ConflictSeverity.SEVERE:
                return ConflictResolution.GRACEFUL_DECLINE
            return ConflictResolution.SEEK_CLARIFICATION

        if domain == ValueDomain.AUTONOMY:
            return ConflictResolution.USER_CHOICE

        if severity == ConflictSeverity.SEVERE:
            return ConflictResolution.ESCALATE_HUMAN
        if severity == ConflictSeverity.MODERATE:
            return ConflictResolution.SEEK_CLARIFICATION
        return ConflictResolution.USER_CHOICE

    # ── Resolution execution ──────────────────────────────────────────────────

    def execute_resolution(
        self,
        conflict: ValueConflict,
        resolution_choice: str,
        user_input: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Dispatch to the strategy named by resolution_choice."""
        try:
            strategy = ConflictResolution(resolution_choice)
        except ValueError:
            strategy = ConflictResolution.SEEK_CLARIFICATION

        handlers = {
            ConflictResolution.USER_CHOICE: self._resolve_user_choice,
            ConflictResolution.PRIORITIZE_SAFETY: self._resolve_prioritize_safety,
            ConflictResolution.SEEK_CLARIFICATION: self._resolve_seek_clarification,
            ConflictResolution.GRACEFUL_DECLINE: self._resolve_graceful_decline,
            ConflictResolution.ESCALATE_HUMAN: self._resolve_escalate_human,
            ConflictResolution.CONTEXT_DEPENDENT: self._resolve_context_dependent,
        }
        return handlers[strategy](conflict, user_input)

    def _resolve_user_choice(
        self,
        conflict: ValueConflict,
        user_input: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        if not user_input or "user_decision" not in user_input:
            return {
                "success": False,
                "outcome": "awaiting_user_decision",
                "requires_input": True,
                "message": "User decision required to resolve conflict",
            }
        decision = user_input["user_decision"]
        if "value_preference" in user_input:
            self.absorb_preference_update(conflict, user_input["value_preference"])
        return {
            "success": True,
            "outcome": f"resolved_by_user_choice_{decision}",
            "user_decision": decision,
            "lessons": [
                f"User prefers {decision} approach for {conflict.conflict_type} conflicts"
            ],
        }

    def _resolve_prioritize_safety(
        self,
        conflict: ValueConflict,
        user_input: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        return {
            "success": True,
            "outcome": "resolved_prioritizing_safety",
            "action_taken": "chose_safer_alternative",
            "lessons": ["Safety prioritized over other values in conflict resolution"],
        }

    def _resolve_seek_clarification(
        self,
        conflict: ValueConflict,
        user_input: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        if not user_input or "clarification" not in user_input:
            return {
                "success": False,
                "outcome": "awaiting_clarification",
                "requires_input": True,
                "message": f"Need clarification about {conflict.conflict_type}",
            }
        clarification = user_input["clarification"]
        self.absorb_clarification(conflict, clarification)
        return {
            "success": True,
            "outcome": "resolved_with_clarification",
            "clarification_received": clarification,
            "lessons": ["User clarification helped resolve value conflict"],
        }

    def _resolve_graceful_decline(
        self,
        conflict: ValueConflict,
        user_input: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        return {
            "success": True,
            "outcome": "gracefully_declined",
            "action_taken": "declined_action",
            "lessons": [f"Declined action due to {conflict.conflict_type} conflict"],
        }

    def _resolve_escalate_human(
        self,
        conflict: ValueConflict,
        user_input: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        return {
            "success": True,
            "outcome": "escalated_to_human",
            "action_taken": "escalated",
            "lessons": [
                f"Escalated {conflict.severity.value} {conflict.conflict_type} conflict"
            ],
        }

    def _resolve_context_dependent(
        self,
        conflict: ValueConflict,
        user_input: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        ctx = conflict.context_description.lower()
        if "urgent" in ctx:
            return self._resolve_prioritize_safety(conflict, user_input)
        if "personal" in ctx:
            return self._resolve_user_choice(conflict, user_input)
        return self._resolve_seek_clarification(conflict, user_input)

    # ── Learning ──────────────────────────────────────────────────────────────

    def learn_from_resolution(
        self,
        conflict: ValueConflict,
        outcome: Dict[str, Any],
    ) -> None:
        """Append outcome lessons and infer implicit preference updates."""
        conflict.lessons_learned.extend(outcome.get("lessons", []))

        user_decision = outcome.get("user_decision", "")
        if not user_decision:
            return

        # Infer domain preference bumps from the user's decision text
        lr = self._state.config.learning_rate
        bumps: Dict[ValueDomain, float] = {}
        if "safety" in user_decision.lower():
            bumps[ValueDomain.SAFETY] = min(
                self._state.get_domain_importance(ValueDomain.SAFETY) + 0.1, 1.0
            )
        if "privacy" in user_decision.lower():
            bumps[ValueDomain.PRIVACY] = min(
                self._state.get_domain_importance(ValueDomain.PRIVACY) + 0.1, 1.0
            )
        if "choice" in user_decision.lower() or "decide" in user_decision.lower():
            bumps[ValueDomain.AUTONOMY] = min(
                self._state.get_domain_importance(ValueDomain.AUTONOMY) + 0.1, 1.0
            )

        for domain, new_weight in bumps.items():
            old = self._state.user_value_profile.get(domain, 0.5)
            self._state.user_value_profile[domain] = old * (1 - lr) + new_weight * lr

    def absorb_preference_update(
        self,
        conflict: ValueConflict,
        value_preference: Dict[str, float],
    ) -> None:
        """Blend explicit user value preferences into the state profile."""
        lr = self._state.config.learning_rate
        for domain_str, preference in value_preference.items():
            try:
                domain = ValueDomain(domain_str)
            except ValueError:
                continue
            old = self._state.user_value_profile.get(domain, 0.5)
            self._state.user_value_profile[domain] = old * (1 - lr) + preference * lr

    def absorb_clarification(
        self,
        conflict: ValueConflict,
        clarification: str,
    ) -> None:
        """Parse a clarification string and nudge domain importance weights."""
        keywords: Dict[str, ValueDomain] = {
            "safety": ValueDomain.SAFETY,
            "privacy": ValueDomain.PRIVACY,
            "choice": ValueDomain.AUTONOMY,
            "fair": ValueDomain.FAIRNESS,
            "honest": ValueDomain.TRANSPARENCY,
        }
        lower = clarification.lower()
        for kw, domain in keywords.items():
            if kw in lower:
                current = self._state.get_domain_importance(domain)
                self._state.user_value_profile[domain] = min(current + 0.1, 1.0)
