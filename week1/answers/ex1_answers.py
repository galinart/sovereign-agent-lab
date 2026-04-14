"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_A_XML_ANSWER      = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT    = True
PART_A_XML_CORRECT      = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
All three formatting conditions produced correct answers on the Llama-3.3-70B model with
the clean baseline dataset. However, the plain condition chose The Haymarket Vaults while
the XML and sandwich conditions both chose The Albanach. Both venues satisfy all three
constraints (capacity >= 160, vegan options, available tonight), so all answers are correct,
but the formatting influenced which valid venue the model selected.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_B_XML_ANSWER      = "The Albanach"
PART_B_SANDWICH_ANSWER = "The Albanach"

PART_B_PLAIN_CORRECT    = True
PART_B_XML_CORRECT      = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
The Holyrood Arms is the harder distractor because it matches two of the three constraints
(capacity=160 and vegan=yes) and only fails on availability (status=full). A model could
easily latch onto the matching attributes and overlook the status field, especially in a
plain text format where the "full" status is not visually prominent.
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True

PART_C_PLAIN_ANSWER    = "Haymarket Vaults"
PART_C_XML_ANSWER      = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Part C ran the same distractor dataset on Gemma 2 2B, a much smaller model. Surprisingly,
all three conditions still produced correct answers. Unlike the 70B model which split between
Albanach and Haymarket depending on format, the 2B model consistently chose Haymarket Vaults
across all conditions. The small model did not exhibit the expected structural sensitivity on
this dataset, though it dropped the article "The" in the plain condition, suggesting less
precise extraction even when the core answer was correct.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the signal-to-noise ratio is low — for example, when
the context contains many near-miss distractors, when the relevant information is buried in
the middle of a long prompt, or when you are using a smaller, less capable model. In this
experiment, the strong 70B model handled all conditions correctly, but even it showed
sensitivity to formatting by choosing different valid answers depending on the structure.
For production agent systems, structured formatting (XML tags, sandwich prompts) provides
a safety margin that becomes critical as tasks grow more complex and models are pushed
closer to their limits.
"""
