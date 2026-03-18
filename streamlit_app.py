import streamlit as st

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="SCAN FRONTIÈRE v1.0", page_icon="🛂", layout="centered")

# --- 2. DESIGN GRAPHIQUE AVANCÉ (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; }
    h1 { color: #1877f2; text-align: center; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; }
    
    /* Style des boutons de réponse */
    div.stButton > button {
        background-color: white; color: #1877f2; border: 2px solid #1877f2;
        border-radius: 15px; height: 3.5rem; font-weight: bold; font-size: 1.1rem;
        transition: 0.3s; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 10px;
    }
    div.stButton > button:hover { background-color: #1877f2; color: white; transform: translateY(-3px); box-shadow: 0 8px 15px rgba(24,119,242,0.2); }

    /* La Carte de Résultat Finale */
    .id-card {
        background: white; border-radius: 25px; padding: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1); border-top: 12px solid #1877f2;
        margin-top: 20px; font-family: 'Helvetica Neue', sans-serif;
    }
    .status-online { color: #42b72a; font-weight: bold; font-size: 0.9rem; text-transform: uppercase; }
    .label { color: #606770; font-size: 0.8rem; font-weight: bold; text-transform: uppercase; margin-bottom: 2px; }
    .value { color: #1c1e21; font-size: 1.1rem; font-weight: bold; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIQUE & QUESTIONS ---
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.scores = {"Hacker": 0, "Touriste": 0, "Exilé": 0, "Ananas": 0, "Agent": 0}

QUESTIONS = [
    ("Motif principal de votre passage ?", [("Aide Humanitaire", "Agent"), ("Vacances", "Touriste"), ("Affaires confidentielles", "Hacker"), ("Asile", "Exilé")]),
    ("Objectif après la frontière ?", [("Installation", "Exilé"), ("Transit rapide", "Agent"), ("Recherche / Exploration", "Hacker"), ("Inconnu", "Ananas")]),
    ("Ressources financières ?", [("Standard / Cash", "Touriste"), ("Cryptomonnaies", "Hacker"), ("Faibles", "Exilé"), ("Inexistantes", "Ananas")]),
    ("Document présenté ?", [("Passeport Bio", "Touriste"), ("Diplomatique", "Agent"), ("Abîmé", "Exilé"), ("Aucun", "Ananas")]),
    ("Objets suspects ?", [("Laptop chiffré", "Hacker"), ("Aucun", "Agent"), ("Arme de défense", "Ananas"), ("Souvenirs", "Touriste")]),
    ("Type de bagage ?", [("Sac à dos", "Touriste"), ("Mallette technique", "Hacker"), ("Valise luxe", "Agent"), ("Rien", "Ananas")]),
    ("Réaction au scanner ?", [("Calme", "Agent"), ("Nervosité", "Exilé"), ("Arrogance", "Hacker"), ("Absence d'émotion", "Ananas")]),
    ("Profession déclarée ?", [("Étudiant", "Touriste"), ("Agent d'État", "Agent"), ("Freelance Tech", "Hacker"), ("Sans emploi", "Exilé")]),
    ("Durée du séjour ?", [("Quelques jours", "Touriste"), ("Permanent", "Exilé"), ("Quelques heures", "Agent"), ("Indéfinie", "Ananas")]),
    ("Dernière zone visitée ?", [("Capitale", "Touriste"), ("Zone de conflit", "Exilé"), ("Paradis fiscal", "Hacker"), ("Jungle", "Ananas")])
]

st.markdown("<h1>🛂 SCAN FRONTIÈRE v1.0</h1>", unsafe_allow_html=True)

if st.session_state.step < len(QUESTIONS):
    # Barre de progression
    st.progress(st.session_state.step / len(QUESTIONS))
    
    q_text, options = QUESTIONS[st.session_state.step]
    st.markdown(f"### PROTOCOLE {st.session_state.step + 1}/10")
    st.subheader(q_text)
    
    # Affichage des boutons
    for text, category in options:
        if st.button(text):
            st.session_state.scores[category] += 1
            st.session_state.step += 1
            st.rerun()

else:
    # CALCUL DU GAGNANT
    gagnant = max(st.session_state.scores, key=st.session_state.scores.get)
    
    # FICHE FINALE
    st.balloons()
    st.markdown(f"""
        <div class="id-card">
            <div style="display: flex; justify-content: space-between;">
                <span class="status-online">● ANALYSE BIOMÉTRIQUE VALIDÉE</span>
                <span style="color:#606770;">ID #SCAN-{random.randint(1000,9999)}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 30px; margin-top: 30px;">
                <div style="font-size: 80px; background: #f0f2f5; border-radius: 50%; width: 120px; height: 120px; display: flex; align-items: center; justify-content: center; border: 4px solid #1877f2;">
                    👤
                </div>
                <div>
                    <h2 style="margin:0; color:#1c1e21;">NOUR AL-FAYED</h2>
                    <p style="color:#1877f2; font-weight: bold; font-size: 1.2rem; margin:0;">PROFIL : {gagnant.upper()}</p>
                </div>
            </div>
            <hr style="border: 0.5px solid #eee; margin: 30px 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <p class="label">Autorisation</p>
                    <p class="value">ACCORDÉE</p>
                </div>
                <div>
                    <p class="label">Niveau de Risque</p>
                    <p class="value">{"BAS" if gagnant == "Touriste" else "MODÉRÉ"}</p>
                </div>
            </div>
            <p class="label">Note de l'IA</p>
            <p class="value" style="font-style: italic;">Sujet identifié avec une précision de 94.2%. Aucun antécédent majeur.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("RESCANNER UN PASSAGER"):
        st.session_state.step = 0
        st.session_state.scores = {k: 0 for k in st.session_state.scores}
        st.rerun()
