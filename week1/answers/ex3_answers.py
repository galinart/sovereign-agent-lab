"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  'calling to confirm a booking' → 160 guests → ~50 vegan → £200 deposit
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "confirmed"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  'calling to confirm a booking' → 160 guests → ~50 vegan → £400 deposit
Sorry, it seems the value you provided `~50` is not a valid number. Please provide a valid number in your response.
And how many of those guests will need vegan meals?
Your input ->  50
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £400 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

CONVERSATION_2_OUTCOME = "escalated"
CONVERSATION_2_REASON  = "a deposit of £400 exceeds the organiser's authorised limit of £300"

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  I am wondering if there is free parking next to the venue
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Is there anything else I can help you with?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM recognized the parking question as outside the booking confirmation scope and triggered the handle_out_of_scope flow. It responded with the pre-written utter_out_of_scope message, deflecting the user to contact the event organiser directly, then offered to continue helping with the booking.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
Rasa CALM routed the out-of-scope request to a pre-defined handle_out_of_scope flow and delivered a deterministic, pre-written response — always the same wording, always on-script. LangGraph's agent, by contrast, generated a free-form response: it reasoned about which tools were available, concluded none applied, and improvised a helpful reply suggesting National Rail, LNER, and Google Maps. The CALM approach is more predictable and auditable — you know exactly what the agent will say for any off-topic request. The LangGraph approach is more flexible and informative but could vary between runs or even hallucinate if the model is less capable.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
Uncommented the cutoff guard block in actions/actions.py and temporarily changed the condition to `if True:` to force it to trigger regardless of the current time. Retrained the model with `uv run rasa train`, restarted the action server, and ran a happy-path conversation ('calling to confirm a booking' with 160 guests, ~50 vegan, £200 deposit). The agent escalated with: "it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline." Confirmed the guard fires correctly, then restored the real time check.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
The LLM now handles slot extraction that previously required Python regex — parsing "about 160 people" or "one-sixty" into 160.0 happens automatically via from_llm mappings, eliminating the ValidateBookingConfirmationForm class entirely. The LLM also handles intent classification — no nlu.yml training examples needed. But Python still enforces the business rules (deposit limits, capacity checks, vegan ratio thresholds) in ActionValidateBooking. This is deliberate: business constraints must be deterministic and non-negotiable. An LLM might rationalize "£350 is close enough to £300" but Python simply checks deposit > 300 and escalates. The trade-off is that CALM depends on LLM reliability for extraction — if the LLM misparses a number, there's no regex fallback. The old approach was more brittle but more predictable in its parsing behavior.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
The Rasa CALM agent cannot improvise actions outside its defined flows — it cannot call a tool that isn't in flows.yml, cannot chain arbitrary API calls at runtime, and cannot generate novel multi-step plans the way the LangGraph agent did in Exercise 2. For the booking confirmation use case, this is a feature, not a limitation. The CALM agent's job is narrow and high-stakes: collect three numbers, validate them against business rules, and confirm or escalate. You want every possible path to be visible in the YAML and auditable. The setup cost (config.yml, domain.yml, flows.yml, endpoints.yml, training, two terminals, a licence) buys you that guarantee. LangGraph's single-file simplicity is faster to prototype, but for a production booking line where a wrong confirmation costs real money, the explicit flow structure is worth the overhead.
"""
