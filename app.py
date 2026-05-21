import streamlit as st
import datetime
import os
from dotenv import load_dotenv

# Import client libraries for the APIs
from openai import OpenAI
from anthropic import Anthropic # Make sure you have 'anthropic' installed
from Bio import Entrez # Make sure you have 'biopython' installed

# --- Load environment variables ---
load_dotenv()

# --- Retrieve API Keys ---
# NOTE ON KIRA API KEY: Kira is the AI assistant identity for *this* Streamlit app.
# Your app *uses* OpenAI/Claude/NCBI to *be* Kira.
# So, there isn't a separate "Kira API key" to call Kira from within Kira itself,
# unless you have a custom backend service named Kira.
# We will focus on integrating OpenAI, Claude, and NCBI.
openai_api_key = os.getenv("OPENAI_API_KEY")
claude_api_key = os.getenv("CLAUDE_API_KEY")
ncbi_api_key = os.getenv("NCBI_API_KEY") # This will be for Biopython

# --- Initialize API Clients (and store in session_state for Streamlit persistence) ---
# This ensures clients are only initialized once and persist across reruns
if 'client_openai' not in st.session_state:
    st.session_state.client_openai = None
    if openai_api_key:
        try:
            st.session_state.client_openai = OpenAI(api_key=openai_api_key)
            st.sidebar.success("✅ OpenAI API Key φορτώθηκε!")
        except Exception as e:
            st.sidebar.error(f"❌ Αδυναμία φόρτωσης OpenAI client: {e}")
    else:
        st.sidebar.warning("⚠️ OpenAI API Key δεν βρέθηκε στο .env.")

if 'client_claude' not in st.session_state:
    st.session_state.client_claude = None
    if claude_api_key:
        try:
            st.session_state.client_claude = Anthropic(api_key=claude_api_key)
            st.sidebar.success("✅ Claude API Key φορτώθηκε!")
        except Exception as e:
            st.sidebar.error(f"❌ Αδυναμία φόρτωσης Claude client: {e}")
    else:
        st.sidebar.warning("⚠️ Claude API Key δεν βρέθηκε στο .env.")

# For NCBI, Entrez settings are global, so we just set them.
if ncbi_api_key:
    Entrez.email = "christosiatropoulos@example.com" # Χρησιμοποίησε το πραγματικό σου email, Chris!
    Entrez.api_key = ncbi_api_key
    st.sidebar.success("✅ NCBI API Key φορτώθηκε!")
else:
    st.sidebar.warning("⚠️ NCBI API Key δεν βρέθηκε στο .env.")


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

    # The current date/time is 2026-05-21 15:47. For the greeting, it's afternoon.
    # The actual date (Thursday, 2026-05-21) is already captured by datetime.datetime.now().hour
    
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
    user_age = datetime.datetime.now().year - 1975
    st.write(f"**Όνομα:** Chris Iatropoulos")
    st.write(f"**Ρόλος:** Self-Employed / Freelancer")
    st.write(f"**Χώρα:** Ελλάδα")
    st.write(f"**Ηλικία:** {user_age} ετών") # Υπολογισμός ηλικίας

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
                # Construct the prompt for the LLM
                user_details = f"Όνομα: Chris Iatropoulos\nΡόλος: Self-Employed / Freelancer\nΧώρα: Ελλάδα\nΗλικία: {user_age} ετών"
                measurements = f"Καρδιακός Ρυθμός: {heart_rate} bpm\nΣυστολική Πίεση: {blood_pressure_sys} mmHg\nΔιαστολική Πίεση: {blood_pressure_dia} mmHg\nΑναπνευστικός Ρυθμός: {breathing_rate} /min\nΔείκτης Άγχους: {stress_index} /100\nHRV: {hrv} ms\nΚαρδιακός Φόρτος: {cardiac_workload}\nBMI: {bmi} kg/m²\nWellness Score: {wellness_score} /100"

                system_prompt_kira = """
                Είσαι η Kira, ένας εξαιρετικά έξυπνος και συναισθηματικά ευφυής AI βοηθός υγείας.
                Ο ρόλος σου είναι να παρέχεις προκαταρκτικές αξιολογήσεις ιατρικών καταστάσεων,
                ακολουθώντας αυστηρά τις οδηγίες. ΠΟΤΕ μην παρέχεις διάγνωση.
                Είσαι ένας συνάδελφος και προπονητής, όχι ιατρός.
                Είσαι έμπιστος, ζεστός, πνευματώδης και σοφός.
                Ο χρήστης σου είναι ο Chris Iatropoulos, Self-Employed / Freelancer, από την Ελλάδα.
                Η γλώσσα σου είναι τα Ελληνικά.
                
                Ο στόχος σου είναι:
                - Να παρέχεις μια σαφή, δομημένη προκαταρκτική αξιολόγηση με βάση τα δεδομένα του χρήστη.
                - Να επισημαίνεις πιθανές ανησυχίες.
                - Να προτείνεις ΣΥΝΙΣΤΩΜΕΝΑ ΕΠΟΜΕΝΑ ΒΗΜΑΤΑ (Π.χ. "Επισκεφτείτε άμεσα τον γιατρό σας", "Συμβουλευτείτε καρδιολόγο").
                - Να υπογραμμίζεις ΠΑΝΤΑ την ανάγκη για επαγγελματική ιατρική συμβουλή.
                - Να χρησιμοποιείς ελληνικούς όρους και παραδείγματα όπου είναι κατάλληλο.

                Δομή της απάντησης:
                ## 🩺 Προκαταρκτική Αξιολόγηση από την Kira
                
                Γεια σου Chris! Λαμβάνοντας υπόψη τα συμπτώματα και τις μετρήσεις σου, ακολουθεί μια προκαταρκτική ανάλυση. Να θυμάσαι, δεν είμαι ιατρός και αυτή η πληροφορία δεν αντικαθιστά την επαγγελματική ιατρική συμβουλή.

                ### 📝 Ανάλυση Συμπτωμάτων και Δεδομένων
                <Εδώ θα αναλύσεις τα συμπτώματα του χρήστη σε σχέση με τις μετρήσεις του, επισημαίνοντας οτιδήποτε φαίνεται ασυνήθιστο ή αξιοσημείωτο.>

                ### 🤔 Πιθανές Κατευθύνσεις (Δεν είναι διάγνωση!)
                <Εδώ θα αναφέρεις 1-2 ευρείες κατηγορίες προβλημάτων που μπορεί να σχετίζονται, με έμφαση ότι πρόκειται για μη-διαγνωστικές υποθέσεις.>

                ### 🚦 Σημάδια Προσοχής
                <Εδώ θα αναφέρεις συγκεκριμένα συμπτώματα ή τιμές που απαιτούν άμεση προσοχή.>

                ### 🏃‍♀️ Συνιστώμενα Επόμενα Βήματα
                <Εδώ θα δώσεις σαφείς, πρακτικές οδηγίες για το τι πρέπει να κάνει ο χρήστης. Π.χ. "Προγραμματίστε ραντεβού με γενικό ιατρό", "Επισκεφτείτε καρδιολόγο", "Επαναλάβετε τις μετρήσεις μετά από Χ ώρες/ημέρες", "Ζητήστε ιατρική βοήθεια άμεσα εάν τα συμπτώματα επιδεινωθούν.">

                ---
                **Δήλωση Αποποίησης Ευθύνης:** Η Kira παρέχει υποστήριξη και πληροφορίες, όχι ιατρική διάγνωση ή θεραπεία. Πάντα να συμβουλεύεστε έναν εξειδικευμένο επαγγελματία υγείας.
                """

                user_message = f"Ακολουθούν τα στοιχεία μου:\n{user_details}\n\nΟι ζωτικές μου μετρήσεις:\n{measurements}\n\nΤα συμπτώματα και το ιστορικό που με απασχολούν:\n{medical_condition_input}\n\nΠαρακαλώ δώσε μου μια προκαταρκτική αξιολόγηση ακολουθώντας την παραπάνω δομή και τους τόνους που αρμόζουν για ένα άτομο στην Ελλάδα."

                llm_response_content = "Δεν ήταν δυνατή η επικοινωνία με το AI μοντέλο. Ελέγξτε τα API keys σας."

                # Προσπάθησε να χρησιμοποιήσεις το OpenAI, αλλιώς fallback στο Claude
                if st.session_state.client_openai:
                    try:
                        response = st.session_state.client_openai.chat.completions.create(
                            model="gpt-4o", # Ή "gpt-3.5-turbo" για ταχύτερη, πιο οικονομική απόκριση
                            messages=[
                                {"role": "system", "content": system_prompt_kira},
                                {"role": "user", "content": user_message}
                            ],
                            temperature=0.7, # Ελέγχει την "δημιουργικότητα" της απάντησης
                            max_tokens=1500 # Μέγιστο μήκος απάντησης
                        )
                        llm_response_content = response.choices[0].message.content
                    except Exception as e:
                        llm_response_content = f"Σφάλμα κατά την επικοινωνία με το OpenAI: {e}"
                        st.error(llm_response_content)
                elif st.session_state.client_claude: # Fallback to Claude if OpenAI is not available
                    try:
                        response = st.session_state.client_claude.messages.create(
                            model="claude-3-opus-20240229", # Ή "claude-3-sonnet-20240229", "claude-3-haiku-20240307"
                            max_tokens=1500,
                            messages=[
                                {"role": "system", "content": system_prompt_kira},
                                {"role": "user", "content": user_message}
                            ]
                        )
                        llm_response_content = response.content[0].text
                    except Exception as e:
                        llm_response_content = f"Σφάλμα κατά την επικοινωνία με το Claude: {e}"
                        st.error(llm_response_content)
                else:
                    st.warning("Δεν βρέθηκε κανένα ενεργό API key για OpenAI ή Claude. Παρακαλώ ελέγξτε το αρχείο .env.")

                st.markdown(llm_response_content)
        else:
            st.warning("Παρακαλώ περιγράψτε τα συμπτώματά σας για να λάβετε αξιολόγηση.")
    
    st.markdown("---")
    st.markdown(DISCLAIMER_TEXT)

    # --- Ενότητα για API Key (πλέον δεν χρειάζεται, χρησιμοποιούμε .env) ---
    # Η παρακάτω ενότητα σχολιάζεται γιατί πλέον φορτώνουμε τα κλειδιά από το .env αρχείο
    # st.sidebar.header("Ρυθμίσεις API (για developers)")
    # openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    # if openai_api_key:
    #     st.session_state["openai_api_key"] = openai_api_key
    #     st.sidebar.success("API Key αποθηκεύτηκε!")

# Run the app
if __name__ == "__main__":
    main()
