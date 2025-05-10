import streamlit as st

# Set page configuration and logo
st.set_page_config(
    page_title="Case Interview Preparation Guide",
    page_icon="🎓",
    layout="wide"
)
st.logo("data/sabta_logo.png", size="large")

# Hauptüberschrift
st.title("🎓 Case Interview Preparation Guide")

# Einführungstext
st.write("Preparing for consulting and finance interviews requires structured thinking and practice. This page covers key strategies and tips to help you excel in interviews.")

# Abschnitt: Strukturierung & Problemlösung
st.header('Structuring & Problem Solving')
st.markdown('''
- **Clarify the problem:** Ask questions to ensure you understand the objective and constraints.
- **Structure your approach:** Break down the problem using a top-down or hypothesis-driven approach (MECE principle).
- **Use issue trees:** Identify key drivers (e.g. profit = revenue - cost) and branch into sub-components (fixed vs variable costs, price vs volume).
- **Support with data:** Interpret charts or numbers by noting top-level trends and outliers before drawing conclusions.
- **Stay MECE and logical:** Make sure your breakdown is mutually exclusive and collectively exhaustive.
- **Summarize and check:** Restate your final answer and confirm it addresses the main question.
- **Be hypothesis-driven:** Start with a likely solution path and confirm or adjust it as you gather information.
- **Quantify assumptions:** Attach rough numbers or percentages to ideas to make analysis concrete.
''')
st.info('**Tipp:** Pause to plan your answer structure before diving into calculations or details.')
st.info('**Tipp:** Always double-check with the interviewer if your solution direction matches their expectations.')

# Abschnitt: Communication Strategies
st.header('Communication Strategies')
comm_tab1, comm_tab2 = st.tabs(['Answering', 'Interaction'])

with comm_tab1:
    st.subheader('Answering Questions')
    st.markdown('''
    - **Be concise:** Structure your answers clearly; avoid irrelevant details.
    - **Use examples:** Support points with brief relevant examples or analogies.
    - **Clarity:** Speak clearly at a moderate pace; use pauses to think if needed.
    ''')
    st.info('Stay on point and summarize your main answer before adding details.')

with comm_tab2:
    st.subheader('Interacting with Interviewer')
    st.markdown('''
    - **Active listening:** Pay attention to the question and clarify if anything is unclear.
    - **Engagement:** Maintain eye contact, nod, and use a friendly but professional tone.
    - **Body language:** Sit upright, smile naturally, and project confidence in your posture.
    ''')
    st.info('Ask the interviewer if they need more details or if your answer addresses the question.')

# Abschnitt: Mental Models
st.header('Mental Models')
st.markdown('''
- **80/20 Rule (Pareto):** Focus on the factors that have the largest impact on the problem.
- **First Principles:** Break problems into fundamental parts and build up logic from the ground up.
- **Analogy:** Apply a solution from a similar problem or industry as a starting point.
- **Opportunity vs Sunk Cost:** Consider only relevant future costs/benefits; ignore sunk costs.
- **Simplicity:** Use simple calculations or round numbers for quick estimates.
- **Check Sanity:** After solving, always double-check if your answer is reasonable.
- **Compare scenarios:** Think of best-case, worst-case, and most-likely outcomes to test assumptions.
''')
st.info('**Tipp:** Wenn du stecken bleibst, versuche, das Problem in kleinere Teile zu zerlegen oder Annahmen zu vereinfachen.')

# Abschnitt: Business Frameworks
st.header('Business Frameworks')
st.write('Using well-known business frameworks can help organize your analysis. The tabs below cover common frameworks in various categories.')

profit_tab, market_tab, marketing_tab, mna_tab, other_tab = st.tabs(['Profitability', 'Market & Growth', 'Marketing Mix (4P)', 'M&A & Strategy', 'Other Frameworks'])

# Gewinnspanne und Kostensenkung
with profit_tab:
    st.subheader('Profitability Analysis')
    st.markdown('''
    - **Profit = Revenue - Costs:** Analyze all revenue streams (price × volume) and break down costs (fixed vs variable).
    - **Price & Volume:** Check if changes in price or sales volume could improve profit.
    - **Cost Components:** Identify major fixed costs (rent, salaries) and variable costs (materials, commissions).
    - **Product Mix:** Determine which products or services are most or least profitable.
    ''')
    st.info('Eine Faustregel: Profit = Preis × Menge – Kosten. Untersuche jede Komponente auf Probleme oder Verbesserungsmöglichkeiten.')

# Marktanalyse und Wachstum
with market_tab:
    st.subheader('Market & Growth Framework')
    st.markdown('''
    - **Market Size:** Estimate the total market size and growth rate (current and projected).
    - **Customer Segments:** Identify different customer groups and their specific needs or willingness to pay.
    - **Competition:** Analyze main competitors (market share, strengths, weaknesses).
    - **Barriers to Entry:** Consider regulatory, financial, or technological barriers for new entrants.
    ''')
    st.info('Beim Markteintritt oder Wachstum denke an Nachfrage, Zielkunden und den Wettbewerbsumfeld.')

# Marketing-Mix
with marketing_tab:
    st.subheader('Marketing Mix (4P Framework)')
    st.markdown('''
    - **Product:** What are the features and benefits? Is there product differentiation?
    - **Price:** How is the product priced compared to alternatives? Is there discounting or premium pricing?
    - **Place:** Which distribution channels are used? (Online, retail, etc.)
    - **Promotion:** What marketing or sales strategies are used? (Advertising, promotions, etc.)
    ''')
    st.info('Das 4P-Framework hilft, ein Angebot systematisch zu analysieren (Produkt, Preis, Vertrieb, Werbung).')

# M&A und Strategie
with mna_tab:
    st.subheader('M&A and Strategic Analysis')
    st.markdown('''
    - **Strategic Fit:** Assess how the target fits with the company’s strategy (product overlap, capabilities).
    - **Synergies:** Identify potential cost or revenue synergies (e.g., economies of scale, cross-selling).
    - **Valuation:** Compare standalone value vs. combined value (based on cash flows, growth rates).
    - **Risks:** Consider integration challenges and financial risks (cultural fit, debt burden).
    ''')
    st.info('In M&A-Fällen vergleiche den Wert und die möglichen Synergien mit den Kosten und Risiken.')

# Andere Rahmenwerke
with other_tab:
    st.subheader('Other Frameworks')
    st.markdown('''
    - **SWOT Analysis:** Strengths, Weaknesses, Opportunities, Threats.
    - **PESTEL:** Political, Economic, Social, Technological, Environmental, Legal factors.
    - **Porter’s Five Forces:** Industry attractiveness model (buyer power, supplier power, etc.).
    - **Value Chain:** Breakdown of primary and support activities to find efficiency gains.
    - **Break-even Analysis:** Calculate the sales volume or price needed to cover all costs.
    ''')
    st.info('Verwende andere Frameworks, wenn der Kontext es erfordert (z.B. SWOT für Strategie, Porter für Branche).')

# Abschnitt: Verhaltensfragen
st.header('Behavioral Questions')
behavioral_tab1, behavioral_tab2 = st.tabs(['Common Questions', 'Answer Strategy (STAR)'])

with behavioral_tab1:
    st.subheader('Common Behavioral Questions')
    st.markdown('''
    - **Tell me about yourself:** Brief career overview focusing on relevant experience and skills.
    - **Why this company/role?** Demonstrate your research on the firm and explain how your skills align with their needs.
    - **Why consulting/finance?** Explain your motivation and fit for the industry and role.
    - **Leadership and Teamwork:** Describe a time you led or worked well in a team.
    - **Challenge or Failure:** Discuss a difficult situation or failure and what you learned.
    - **Strengths/Weaknesses:** Highlight one strength with an example, and a weakness with how you address it.
    ''')
    st.info('Bereite prägnante Beispiele vor und konzentriere dich auf deine Rolle und das Ergebnis bei jeder Geschichte.')

with behavioral_tab2:
    st.subheader('Answer Strategy (STAR Method)')
    st.markdown('''
    - **Situation:** Set the context and describe the challenge.
    - **Task:** Explain your responsibility or goal in that situation.
    - **Action:** Describe the specific steps you took.
    - **Result:** Share the outcomes (quantify if possible) and what you learned.
    - **Conciseness:** Aim for answers around 1-2 minutes to cover all STAR parts without rambling.
    ''')
    st.info('Structure your answers using STAR to ensure completeness and clarity. Stay positive and highlight your achievements.')

# Abschnitt: Vorbereitung Checkliste
st.header('Interview Preparation Checklist')
st.markdown('''
- **Practice Cases Regularly:** Work through sample case interviews to refine your problem-solving approach.
- **Master Core Frameworks:** Review key frameworks flexibly; don’t just memorize them.
- **Brush Up Quant Skills:** Practice mental math and basic finance concepts (e.g., NPV, basic accounting).
- **Research the Company:** Know the firm’s focus, recent deals, and prepare insightful questions.
- **Work on Soft Skills:** Practice speaking clearly, confident body language, and concise explanations.
- **Mock Interviews:** Conduct mock interviews with peers or mentors to get feedback.
- **Prepare Behavioral Stories:** Have several STAR-based stories ready and tailor them to different questions.
- **Market Sizing Practice:** Hone quick estimation skills by practicing population and percentage calculations.
- **Know Your Resume:** Be ready to discuss any detail on your resume confidently.
- **Stay Informed:** Keep up with business news and industry trends to show business awareness.
''')
st.info('Stay relaxed and confident: a good night’s sleep and a positive mindset are also key to performing well!')
