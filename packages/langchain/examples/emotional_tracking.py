"""
Emotional Tracking Example
==========================
Demonstrates PACT's emotional awareness in a coaching/therapy context.

Part of PACT by NeurobloomAI
https://github.com/neurobloomai/pact-hx

Run:
    python examples/emotional_tracking.py
"""

import os
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from pact_langchain import PACTMemory


# Custom prompt that uses emotional context
COACHING_PROMPT = PromptTemplate(
    input_variables=["history", "input", "emotional_state"],
    template="""You are an empathetic life coach.

Conversation history:
{history}

Current emotional state: {emotional_state}

Adjust your tone based on emotional state.