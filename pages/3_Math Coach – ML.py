import streamlit as st
import random
import time
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd

# Set page configuration and logo
st.set_page_config(
    page_title="Case Interview Preparation Guide",
    page_icon="📟",
    layout="wide"
)
st.logo("data/sabta_logo.png", size="large")

# Hauptüberschrift
st.title("📟 Case Interview Preparation Guide")
st.markdown("""
This app generates 30 random math problems (addition, subtraction, multiplication, division) across three difficulty levels (same as in Math Drills) and records your answer time and accuracy. Afterwards, a KNN classifier (scikit-learn) is trained to recommend the optimal next difficulty level. You will also receive personalized feedback on your calculation performance.
""")

st.divider()

# Initialisierung: Erzeugung der Fragenliste und Ergebnisse beim ersten Aufruf
if 'questions' not in st.session_state:
    st.session_state['questions'] = []   # Liste der Fragen (jeweils: a, op, b, Ergebnis, Schwierigkeitslevel)
    st.session_state['index'] = 0        # Index der aktuellen Frage
    st.session_state['times'] = []       # Antwortzeiten
    st.session_state['correct'] = []     # Korrektheitswerte (True/False)

    def generate_question(diff):
        # Operatorauswahl mit Gewichtung
        if diff == 1:
            op = random.choices(['+', '-', '*', '/'], weights=[3,3,2,2])[0]
        elif diff == 2:
            op = random.choices(['+', '-', '*', '/'], weights=[2,2,3,3])[0]
        else:
            op = random.choices(['+', '-', '*', '/'], weights=[1,1,4,4])[0]
        # Erzeugen von Operanden und Ergebnis
        if op == '+':
            if diff == 1:
                a = random.randint(0, 10); b = random.randint(0, 10)
            elif diff == 2:
                a = random.randint(0, 50); b = random.randint(0, 50)
            else:
                a = random.randint(0, 100); b = random.randint(0, 100)
            result = a + b
        elif op == '-':
            if diff == 1:
                a = random.randint(0, 10); b = random.randint(0, 10)
            elif diff == 2:
                a = random.randint(0, 50); b = random.randint(0, 50)
            else:
                a = random.randint(0, 100); b = random.randint(0, 100)
            result = a - b
        elif op == '*':
            if diff == 1:
                a = random.randint(0, 5); b = random.randint(0, 5)
            elif diff == 2:
                a = random.randint(0, 10); b = random.randint(0, 10)
            else:
                a = random.randint(0, 20); b = random.randint(0, 20)
            result = a * b
        else:  # Division: sicheres Teilen (ohne Rest)
            if diff == 1:
                b = random.randint(1, 5); c = random.randint(0, 5)
            elif diff == 2:
                b = random.randint(1, 10); c = random.randint(0, 10)
            else:
                b = random.randint(1, 15); c = random.randint(0, 15)
            a = b * c
            result = a // b
        return (a, op, b, result, diff)

    # Erzeuge 30 Zufallsfragen
    for _ in range(30):
        level = random.randint(1, 3)
        st.session_state['questions'].append(generate_question(level))
    # Setze Startzeit für die erste Frage
    st.session_state['start_time'] = time.time()

# Hauptablauf: Frage stellen oder Auswertung nach Abschluss
if st.session_state['index'] < 30:
    idx = st.session_state['index']
    a, op, b, result, diff = st.session_state['questions'][idx]
    st.write(f"**Question {idx+1} of 30 (Difficulty {diff})**")
    with st.container():
            st.markdown(
            f"""
            <div style="padding: 20px; border: 2px solid #800080; border-radius: 10px; background-color: #E6E6FA;">
                <h2 style="color: #4B0082; text-align: center;">{f"{a} {op} {b}"}</h2>
            </div>
            """,
            unsafe_allow_html=True
            )
    st.divider()
    with st.form(key=f"form_{idx}"):
        # Erlaube negative Antworten durch min_value-Parameter
        answer = st.number_input("Your answer:", value=0, step=1, min_value=-100000, max_value=100000, key=f"answer_{idx}")
        if st.form_submit_button("Submit answer"):
            # Zeitende der Antwort nehmen
            end_time = time.time()
            duration = end_time - st.session_state['start_time']
            # Korrektheitsprüfung
            is_correct = (answer == result)
            # Daten speichern
            st.session_state['times'].append(duration)
            st.session_state['correct'].append(is_correct)
            # Weiter zur nächsten Frage
            st.session_state['index'] += 1
            # Neue Startzeit für nächste Frage
            st.session_state['start_time'] = time.time()
            st.rerun()
    # Fortschrittsanzeige (Balken)
    progress = st.session_state['index'] / 30
    st.progress(progress)

else:
    # Auswertung nach Abschluss aller Fragen
    st.header("Results")
    total_correct = sum(st.session_state['correct'])
    avg_time = np.mean(st.session_state['times'])
    st.write(f"You answered **{total_correct} out of 30** questions correctly.")
    st.write(f"Average time per question: **{avg_time:.1f} seconds**.")

    # Statistiken pro Operator
    ops = ['+', '-', '*', '/']
    op_counts = {op: 0 for op in ops}
    op_correct = {op: 0 for op in ops}
    for i, (a, op, b, res, diff) in enumerate(st.session_state['questions']):
        op_counts[op] += 1
        if st.session_state['correct'][i]:
            op_correct[op] += 1

    # Balkendiagramm: korrekt vs. inkorrekt pro Operator
    chart_data = pd.DataFrame({
        "Correct": [op_correct[op] for op in ops],
        "Incorrect": [op_counts[op] - op_correct[op] for op in ops]
    }, index=ops)
    st.bar_chart(chart_data)

    # KNN-Klassifikator trainieren
    # Trainingsdaten (Beispielwerte für Leistung und Zeit)
    X_train = np.array([
        [5, 0.9], [7, 0.85], [9, 0.8],   # leicht, schnell & genau
        [12, 0.7], [15, 0.6],            # mittelmäßige Leistung
        [20, 0.5], [25, 0.3], [30, 0.2]  # langsamer & weniger genau
    ])
    y_train = np.array([1, 1, 1, 2, 2, 3, 3, 3])
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)
    # Merkmale aus deinen Ergebnissen
    accuracy = total_correct / 30
    user_features = np.array([[avg_time, accuracy]])
    predicted_level = knn.predict(user_features)[0]
    st.subheader(f"Recommended difficulty level: {predicted_level}")

    # Feedback-Generierung: alle zutreffenden Meldungen sammeln
    feedbacks = []

    # 1) Operator-spezifische Probleme
    for op in ops:
        count = op_counts.get(op, 0)
        correct_count = op_correct.get(op, 0)
        acc_op = (correct_count / count) if count > 0 else 1.0
        if acc_op < 0.5:
            if op == '/':
                feedbacks.append("You have difficulty with division. Practice dividing specifically.")
            elif op == '*':
                feedbacks.append("Multiplications are challenging for you. Review multiplication exercises.")
            elif op == '-':
                feedbacks.append("Subtractions are problematic. Try to calculate subtractions more calmly.")
            elif op == '+':
                feedbacks.append("You often make mistakes in additions. Focus on adding carefully.")

    # 2) Allgemeine Leistungsbewertung
    if accuracy >= 0.9 and avg_time < 7:
        feedbacks.append("Excellent and fast performance! Keep it up.")
    if accuracy >= 0.9:
        feedbacks.append("Very accurate calculations, but try to be a bit quicker.")
    if accuracy < 0.5:
        feedbacks.append("Performance could still improve. Practice basic arithmetic further.")
    if avg_time < 5 and accuracy < 0.7:
        feedbacks.append("You calculate very quickly but inaccurately. Work more calmly.")
    if avg_time > 20 and accuracy > 0.8:
        feedbacks.append("You are very accurate but quite slow. Try to work more swiftly.")

    # 3) Fallback, wenn noch kein Feedback gesammelt wurde
    if not feedbacks:
        feedbacks.append("Good work! Overall, you are at a solid level.")

    # Anzeige aller gesammelten Feedback-Nachrichten
    st.subheader("Your Feedback:")
    for msg in feedbacks:
        st.write(f"- {msg}")
