# app.py
import streamlit as st
import datetime # Για τον υπολογισμό της ηλικίας
from openai import OpenAI # Θα το χρησιμοποιήσουμε αργότερα

# --- Ρυθμίσεις Σελίδας ---
st.set_page_config(
    page_title="Chi Health AI - Η Ψηφιακή σου Υποστήριξη Υγείας",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Σταθερές Kira & Αποποίηση Ευθύνης ---
KIRA_OPENER_HISTORY = [] # Για την προσαρμογή των εναρκτήριων μηνυμάτων
KIRA_WELLBEING_COUNTER = 0 # Για τον έλεγχο ευεξίας κάθε 5ο μήνυμα

DISCLAIMER_TEXT = """
**⚠️ Σημαντική Αποποίηση Ευθύνης:**
Αυτή η εφαρμογή παρέχεται μόνο για ενημερωτικούς σκοπούς και δεν πρέπει να χρησιμοποιείται ως υποκατάστατο επαγγελματικής ιατρικής συμβουλής, διάγνωσης ή θεραπείας. Πάντα να συμβουλεύεστε έναν εξειδικευμένο επαγγελματία υγείας για οποιεσδήποτε ανησυχίες σχετικά με την υγεία σας. Σε περίπτωση έκτακτης ανάγκης, καλέστε άμεσα το 166.
"""

# --- Λειτουργία Kira (Opener & Scoping) ---
def kira_opener():
    global KIRA_WELLBEING_COUNTER
    KIRA_WELLBEING_COUNTER += 1
    
    current_hour = datetime.datetime.now().hour
    
    if 5 <= current_hour < 12:
        greeting = "Καλημέρα"
    elif 12 <= current_hour < 18:
        greeting = "Καλό απόγευμα"
    else:
        greeting = "Καλησπέρα"

    if KIRA_WELLBEING_COUNTER % 5 == 0:
        openers = [
            f"{greeting}, Chris! Πώς αισθάνεσαι σήμερα; Υπάρχουν νίκες ή ανησυχίες που θα ήθελες να μοιραστείς;",
            f"{greeting}, Chris! Είσαι καλά; Κάτι σε απασχολεί αυτή την εβδομάδα;",
            f"{greeting}, Chris! Πώς πάει η διάθεση; Χρειάζεσαι μια ανάσα;",
            f"{greeting}, Chris! Πώς σε βρίσκει η μέρα; Είμαι εδώ για να σε ακούσω.",
            f"{greeting}, Chris! Μια γρήγορη ερώτηση ευεξίας: όλα καλά; Πώς αισθάνεσαι;"
        ]
    else:
        openers = [
            f"{greeting} Chris! 👋 Τι είναι στην κορυφή της λίστας σου σήμερα;",
            f"{greeting} Chris! Θέλεις να αξιολογήσουμε κάτι σχετικά με την υγεία σου;",
            f"{greeting} Chris! Είσαι έτοιμος να δούμε τις μετρήσεις σου και να συζητήσουμε πιθανές ανησυχίες;",
            f"{greeting} Chris! Χρειάζεσαι μια γρήγορη αξιολόγηση υγείας ή βοήθεια με τις ερωτήσεις σου;",
            f"{greeting} Chris! Τι θα ήθελες να εστιάσουμε σήμερα; Είμαι εδώ για σένα.",
        ]
    
    return st.sidebar.info(openers[KIRA_WELLBEING_COUNTER % len(openers)])

# --- Main App ---
def main():
    st.image("https://askainurse.com/favicon-32x32.png", width=60) # Ενδεικτικό λογότυπο
    st.title("Chi Health AI 🌍: Ο Προσωπικός σου Σύμβουλος Υγείας")
    st.subheader("Με τη δύναμη της Kira – Για εσένα, τον Chris Iatropoulos.")

    # Kira's opener in the sidebar
    kira_opener()
    
    st.markdown("---")

    st.header("👤 Τα Στοιχεία σου")
    # Δεν έχουμε πραγματικό login ακόμα, οπότε εμφανίζουμε τα στοιχεία που έχουμε
    st.write(f"**Όνομα:** Chris Iatropoulos")
    st.write(f"**Ρόλος:** Self-Employed / Freelancer")
    st.write(f"**Χώρα:** Ελλάδα")
    st.write(f"**Ηλικία:** {datetime.datetime.now().year - 1975} ετών") # Υπολογισμός ηλικίας

    st.markdown("---")

    st.header("📊 Οι Μετρήσεις σου (Real Data)")
    st.write("Σε αυτή την ενότητα, θα εμφανίζονται οι ζωτικές μετρήσεις σου. Για την αρχική φάση, παρακαλώ εισάγετε τις τιμές χειροκίνητα. Στη συνέχεια, θα ενσωματώσουμε την τεχνολογία face scan για αυτόματη λήψη.")
    
    st.info("💡 **Σημείωση:** Όπου δεν μπορούμε να έχουμε πραγματικά δεδομένα από face scan, θα ζητάμε την εισαγωγή σου ή δεν θα εμφανίζεται η μέτρηση.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Βασικές Μετρήσεις")
        heart_rate = st.number_input("Καρδιακός Ρυθμός (bpm):", min_value=0, max_value=250, value=76, step=1)
        blood_pressure_sys = st.number_input("Συστολική Πίεση (mmHg):", min_value=0, max_value=300, value=128, step=1)
        blood_pressure_dia = st.number_input("Διαστολική Πίεση (mmHg):", min_value=0, max_value=200, value=82, step=1)
        breathing_rate = st.number_input("Αναπνευστικός Ρυθμός (/min):", min_value=0, max_value=50, value=15, step=1)
    with col2:
        st.subheader("Πρόσθετοι Δείκτες")
        stress_index = st.number_input("Δείκτης Άγχους (/100):", min_value=0, max_value=100, value=4, step=1)
        hrv = st.number_input("HRV (ms):", min_value=0, max_value=300, value=11, step=1)
        cardiac_workload = st.number_input("Καρδιακός Φόρτος:", min_value=0, max_value=300, value=162, step=1)
        bmi = st.number_input("BMI (kg/m²):", min_value=10.0, max_value=50.0, value=27.1, step=0.1)
        wellness_score = st.number_input("Wellness Score (/100):", min_value=0, max_value=100, value=41, step=1)
    
    st.markdown("---")

    st.header("🔍 Αξιολόγηση Ιατρικής Κατάστασης")
    st.write("Περιγράψτε την ιατρική κατάσταση που σας απασχολεί ή τα συμπτώματά σας. Όσο πιο αναλυτικός είστε, τόσο καλύτερη θα είναι η αρχική αξιολόγηση από την Kira.")
    
    medical_condition_input = st.text_area(
        "Τα συμπτώματά σας και το ιστορικό σας:",
        height=200,
        placeholder="Π.χ. 'Είχα αίμα κατά την κένωση, ένιωθα κάψιμο στον πρωκτό και έναν ελαφρύ πόνο κάτω από το στήθος...' "
    )

    if st.button("Λήψη Αξιολόγησης από Kira"):
        if medical_condition_input:
            with st.spinner("Η Kira αναλύει τα δεδομένα σας..."):
                # Εδώ θα γίνει η κλήση στον LLM
                # Για την αρχική βήτα, θα χρησιμοποιήσουμε ένα placeholder μέχρι να ενσωματώσουμε το API
                llm_response_placeholder = """
                ### 📝 Προσωρινή Αξιολόγηση από την Kira (Beta Preview)

                **Λόγω του ότι ακόμα δεν έχουμε συνδέσει το AI μοντέλο, αυτή είναι μια προσωρινή απάντηση.**

                Είδατε:
                - **Συμπτώματα:** {user_symptoms}
                - **Ζωτικές Μετρήσεις (εισαγόμενες):**
                    - Καρδιακός Ρυθμός: {hr} bpm
                    - Πίεση: {bp_sys}/{bp_dia} mmHg
                    - Αναπνευστικός Ρυθμός: {br} /min
                    - Δείκτης Άγχους: {si} /100
                    - HRV: {hrv} ms
                    - Καρδιακός Φόρτος: {cw}
                    - BMI: {bmi_val} kg/m²
                    - Wellness Score: {ws} /100

                Η Kira έχει επεξεργαστεί τα δεδομένα σας και είναι έτοιμη να παράγει μια λεπτομερή κλινική αναφορά, ακολουθώντας τα πρότυπα που συζητήσαμε (Πρωτογενής/Διαφορική Διάγνωση, Σχέδιο Θεραπείας, Σημάδια Προσοχής).

                **Μείνετε συντονισμένοι! Η πλήρης ενσωμάτωση του AI μοντέλου είναι το επόμενο βήμα!**
                """
                st.markdown(llm_response_placeholder.format(
                    user_symptoms=medical_condition_input,
                    hr=heart_rate, bp_sys=blood_pressure_sys, bp_dia=blood_pressure_dia,
                    br=breathing_rate, si=stress_index, hrv=hrv, cw=cardiac_workload,
                    bmi_val=bmi, ws=wellness_score
                ))
        else:
            st.warning("Παρακαλώ περιγράψτε τα συμπτώματά σας για να λάβετε αξιολόγηση.")
    
    st.markdown("---")
    st.markdown(DISCLAIMER_TEXT)

    # --- Ενότητα για API Key (Αργότερα) ---
    # st.sidebar.header("Ρυθμίσεις API (για developers)")
    # openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    # if openai_api_key:
    #     st.session_state["openai_api_key"] = openai_api_key
    #     st.sidebar.success("API Key αποθηκεύτηκε!")

# Run the app
if __name__ == "__main__":
    main()