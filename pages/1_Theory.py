## pages/1_CasePrep.py
import streamlit as st

st.set_page_config(page_title="Case Prep Guide", layout="wide")

st.title("Case Interview Preparation Guide")
st.write(
    "This section provides a comprehensive guide on how to approach case interviews. "
    "Learn how to **structure problems**, communicate effectively, apply **mental models** and frameworks, "
    "and prepare for **personal fit** questions."
)

# Structuring and Problem Solving
st.header("Structuring the Case & Problem Solving")
st.write(
    "A successful case interview starts with a clear **structure**. Begin by understanding the problem and asking clarifying questions. "
    "Then break the problem into logical components (ensure your structure is **MECE**: Mutually Exclusive, Collectively Exhaustive). "
    "Prioritize the areas likely to have the biggest impact on the solution."
)
st.markdown(
    "- **Clarify the Problem:** Restate the objective to ensure understanding.\n"
    "- **Decompose the Issues:** Lay out an issue tree or framework covering all key areas (e.g., market, competition, financials).\n"
    "- **Hypothesis-Driven:** Form a hypothesis and identify what to analyze first to test it.\n"
    "- **Analyze Deeply:** Work through each branch of your structure, diving deeper based on findings.\n"
    "- **Synthesize:** Summarize insights and provide a clear recommendation addressing the question."
)

# Communication strategies
st.header("Communication Strategies")
st.write(
    "Communicating clearly and confidently is essential. Speak in a structured manner and keep the interviewer engaged in your thought process:"
)
st.markdown(
    "- **Structure Your Talk:** Start with a roadmap of your approach (e.g., \"First, I'll examine X, then Y...\").\n"
    "- **Think Aloud:** Verbalize your reasoning. This shows your logic and allows guidance if needed.\n"
    "- **Be Concise:** Get to the point. Avoid rambling; use clear, succinct explanations.\n"
    "- **Use Data:** When discussing numbers or analysis, explain what they mean (e.g., \"Profits fell 10%, indicating...\").\n"
    "- **Summarize:** After analysis, state the insight or decision before moving on."
)

# Mental models and tools
st.header("Mental Models & Problem-Solving Tools")
st.write(
    "Leverage proven **mental models** to tackle problems effectively. These are general thinking frameworks that can apply to many cases:"
)
st.markdown(
    "- **80/20 Rule:** Focus on the 20% of factors that drive 80% of the results (prioritize what matters most).\n"
    "- **Benchmarking:** Compare against competitors or standards to identify gaps or opportunities.\n"
    "- **Cost-Benefit Analysis:** Weigh expected benefits vs. costs to prioritize initiatives.\n"
    "- **Root Cause Analysis (5 Whys):** Ask \"Why?\" repeatedly to drill down to the underlying cause of a problem.\n"
    "- **First Principles:** Break complex problems into basic elements and reason from the ground up."
)

# Business frameworks
st.header("Business Frameworks")
st.write(
    "Frameworks provide a starting blueprint for cases. Use them as guides, but **adapt to the case context**:"
)
st.markdown(
    "- **Profitability:** Breakdown Profit = Revenue – Cost. Examine revenue (price × volume) and costs (fixed vs variable) to find issues.\n"
    "- **Market Entry:** Consider market attractiveness (size, growth, competition), entry strategy options, and risks.\n"
    "- **4 Ps (Marketing):** Analyze Product, Price, Place, Promotion for market strategy or product launch cases.\n"
    "- **Porter’s Five Forces:** Assess industry competitiveness via forces (rivalry, supplier power, buyer power, threat of entry/substitutes).\n"
    "- **M&A Framework:** Look at standalone value of target, synergies, integration challenges, and costs of acquisition."
)
st.write("*(Always tailor frameworks to the specific case—no one-size-fits-all solution!)*")

# Personal fit questions
st.header("Personal Fit & Behavioral Questions")
st.write(
    "Consulting interviews also include personal fit questions. Practice common behavioral questions using the **STAR method** (Situation, Task, Action, Result):"
)
st.markdown(
    "- **Leadership Example:** *\"Tell me about a time you led a team through a challenging situation.\"*\n"
    "- **Teamwork Example:** *\"Describe a successful team project and your contribution.\"*\n"
    "- **Conflict Resolution:** *\"Give an example of a conflict you resolved within a team.\"*\n"
    "- **Failure & Learning:** *\"Tell me about a failure. What did you learn from it?\"*\n"
    "- **Time Management:** *\"How do you prioritize multiple competing deadlines?\"*"
)
st.write(
    "For each, set up the **Situation** and **Task**, explain the **Action** you took, and highlight the **Result**. "
    "Be specific about your role and what you learned. Use a structured story to convey your points."
)
st.info("💡 *Tip:* Prepare 2-3 stories that demonstrate leadership, teamwork, problem-solving, and resilience. Practice delivering them confidently.")
