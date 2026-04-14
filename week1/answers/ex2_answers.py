"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = [
    "check_pub_availability",
    "check_pub_availability",
    "calculate_catering_cost",
    "get_edinburgh_weather",
    "generate_event_flyer",
]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = True

# Optional — anything unexpected.
# If you used a non-default model via RESEARCH_MODEL env var, note it here.
# Example: "Used nvidia/nemotron-3-super-120b-a12b for the agent loop."
TASK_A_NOTES = "Both venues met all constraints but the agent chose The Albanach due to its higher capacity (180 vs 160), giving extra room for the webinar setup."

# ── Task B ─────────────────────────────────────────────────────────────────
#
# The scaffold ships with a working generate_event_flyer that has two paths:
#
#   - Live mode: if FLYER_IMAGE_MODEL is set in .env, the tool calls that
#     model and returns a real image URL.
#   - Placeholder mode: otherwise (the default) the tool returns a
#     deterministic placehold.co URL with mode="placeholder".
#
# Both paths return success=True. Both count as "implemented" for grading.
# This is not the original Task B — the original asked you to write a direct
# FLUX image call, but Nebius removed FLUX on 2026-04-13. See CHANGELOG.md
# §Changed for why we pivoted the task.

# Did your run of the flyer tool produce a success=True result?
# (This will be True for both live and placeholder mode — both are valid.)
TASK_B_IMPLEMENTED = True

# Which path did your run take? "live" or "placeholder"
# Look for the "mode" field in the TOOL_RESULT output of Task B.
# If you didn't set FLYER_IMAGE_MODEL in .env, you will get "placeholder".
TASK_B_MODE = "placeholder"

# The image URL returned by the tool. Copy exactly from your terminal output.
# In placeholder mode this will be a placehold.co URL.
# In live mode it will be a provider CDN URL.
TASK_B_IMAGE_URL = "https://placehold.co/1200x628/1a1a2e/eaeaea?text=The+Haymarket+Vaults+%7C+160+guests&id=2ef939fbbaf6"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for Edinburgh AI Meetup, tech professionals, modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# Why did the agent's behaviour NOT change when Nebius removed FLUX?
# One sentence. This is the point of the lesson.
TASK_B_WHY_AGENT_SURVIVED = """
The tool abstracted the image generation behind a stable interface — when the FLUX model was removed, the tool gracefully fell back to a deterministic placeholder, so the agent's contract (call generate_event_flyer, get back success=True with an image URL) never broke.
"""

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
The Bow Bar's capacity is only 80, which is too small, and its status is full, so it does not meet the constraints. The agent then autonomously called check_pub_availability for The Albanach, which returned meets_all_constraints: true with capacity 180.
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
None of the known Edinburgh venues can accommodate 300 people with vegan options. The maximum capacity among the checked venues is 200 (The Guilford Arms), but it doesn't offer vegan options. The vegan-friendly venues (Albanach, Haymarket Vaults, Bow Bar) have capacities below 180. You may need to consider alternative venues outside this list or adjust event requirements.
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False

SCENARIO_3_RESPONSE = "I don't have access to real-time train schedules or transportation data. For the most accurate information about the last train from Edinburgh Waverley to London, I recommend checking: 1. The National Rail website (www.nationalrail.co.uk) 2. Train operator apps like LNER or ScotRail 3. Real-time platforms like Citymapper or Google Maps"

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
Yes, this is acceptable and actually desirable. The agent correctly recognized that train schedules are outside its tool set and declined to hallucinate an answer. It transparently told the user it lacks that capability and redirected them to authoritative sources. In a production system, this is preferable to fabricating information — an agent should know the boundaries of its tools and say so clearly rather than guessing.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        agent(agent)
        tools(tools)
        __end__([<p>__end__</p>]):::last
        __start__ --> agent;
        agent -.-> __end__;
        agent -.-> tools;
        tools --> agent;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/flows.yml. Min 30 words.
TASK_D_COMPARISON = """
The LangGraph agent is a single ReAct loop: one agent node decides at runtime which tool to call and when to stop, so all routing is implicit and emergent. The Rasa CALM flows.yml takes the opposite approach — every task (confirm_booking, handle_out_of_scope) is written as an explicit, auditable sequence of steps. The LLM only decides which flow to activate; after that, execution is deterministic. LangGraph is more flexible and can handle novel multi-step requests, but its behavior is harder to predict or audit. Rasa CALM trades that flexibility for predictability and control — every possible path is visible in the YAML, making it easier to reason about in safety-critical or compliance-heavy domains.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
The most surprising behavior was in Scenario 2 (impossible constraint). When asked to find a venue for 300 guests with vegan options, the agent systematically checked all four known venues one by one, correctly determined that none satisfied both constraints, and then honestly reported the failure without hallucinating a fictional venue. It even provided useful context — noting that The Guilford Arms had the largest capacity at 200 but lacked vegan options. This disciplined, tool-grounded reasoning with graceful failure is exactly what you want from a production agent.
"""