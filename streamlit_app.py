
import streamlit as st
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="FRONTIER AI SCAN", page_icon="🛂", layout="centered")

# --- 2. BASE DE DONNÉES DES PROFILS ---
# REMPLACE LES LIENS CI-DESSOUS PAR TES VRAIES PHOTOS (URLs)
PROFILS = {
    "Touriste": {
        "decision": "AUTORISÉ", "risk": "BAS", "color": "#42b72a",
        "image": "https://i.ibb.co/LzNf9fQ/tourist-avatar.jpg", # EXEMPLE
        "note": "Aucun antécédent. Sujet en règle."
    },
    "Hacker": {
        "decision": "REFUSÉ / DÉTENU", "risk": "CRITIQUE", "color": "#d93025",
        "image": "https://i.ibb.co/hK7XzPz/hacker-avatar.jpg", # EXEMPLE
        "note": "Matériel cyber-offensif détecté. Tentative d'intrusion."
    },
    "Trafiquant": {
        "decision": "REFUSÉ / INTERPELLÉ", "risk": "ÉLEVÉ", "color": "#d93025",
        "image": "https://i.ibb.co/6y4G1S0/smuggler-avatar.jpg",
        "note": "Contrebande détectée via scanner THz."
    },
    "Exilé": {
        "decision": "EN ATTENTE D'ASILE", "risk": "MODÉRÉ", "color": "#fabb3a",
        "image": "https://i.ibb.co/vYh3M5z/refugee-avatar.jpg",
        "note": "Vérification des documents de protection en cours."
    },
    "Ananas": {
        "decision": "SAISI / DÉTRUIT", "risk": "BIO-RISQUE", "color": "#d93025",
        "image": "https://i.ibb.co/6N7y9Wj/pineapple-avatar.jpg",
        "note": "Matériel biologique non identifié. Quarantaine."
    },
    "Agent": {
        "decision": "AUTORISÉ (Transit)", "risk": "AUCUN", "color": "#42b72a",
        "image": "https://i.ibb.co/zH8XyQz/agent-avatar.jpg",
        "note": "Agent en mission officielle. Code de transit validé."
    }
}

# --- 3. LES 10 QUESTIONS ---
QUESTIONS = [
    ("Motif de passage ?", [("Humanitaire", "Agent"), ("Vacances", "Touriste"), ("Crypto-Mining", "Hacker"), ("Asile", "Exilé")]),
    ("Contenu des bagages ?", [("Vêtements", "Touriste"), ("Serveurs", "Hacker"), ("Inconnu", "Ananas"), ("Rien", "Exilé")]),
    ("Ressources ?", [("Salaire", "Touriste"), ("Blockchain", "Hacker"), ("Aide d'État", "Agent"), ("Néant", "Ananas")]),
    ("Document ?", [("Passeport Bio", "Touriste"), ("Ordre de mission", "Agent"), ("Déchiré", "Exilé"), ("Faux", "Trafiquant")]),
    ("Réaction au Scan ?", [("Calme", "Agent"), ("Sueur", "Trafiquant"), ("Arrogance", "Hacker"), ("Confusion", "Ananas")]),
    ("Profession ?", [("Étudiant", "Touriste"), ("Ingénieur", "Hacker"), ("Diplomate", "Agent"), ("Sans emploi", "Exilé")]),
    ("Destination ?", [("Hôtel", "Touriste"), ("Datacenter", "Hacker"), ("Zone B", "Ananas"), ("Camp", "Exilé")]),
    ("Appareils ?", [("Smartphone", "Touriste"), ("Antenne Satellite", "Hacker"), ("Scellés", "Trafiquant"), ("Aucun", "Ananas")]),
    ("Durée ?", [("1 semaine", "Touriste"), ("Indéfini", "Exilé"), ("48h", "Agent"), ("24h", "Ananas")]),
    ("Dernier Pays ?", [("Europe", "Touriste"), ("Zone Noire", "Hacker"), ("Frontière Est", "Exilé"), ("Inconnu", "Ananas")])
]

# --- 4. LOGIQUE ---
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.scores = {k: 0 for k in PROFILS.keys()}
    st.session_state.id_val = f"ID-{random.randint(10000, 99999)}"

st.markdown(f"<h1 style='color: #1877f2; text-align: center;'>🛂 FRONTIER SCAN v1.0</h1>", unsafe_allow_html=True)

if st.session_state.step < len(QUESTIONS):
    st.progress(st.session_state.step / len(QUESTIONS))
    q_text, options = QUESTIONS[st.session_state.step]
    st.subheader(q_text)
    for text, cat in options:
        if st.button(text, key=text+str(st.session_state.step)):
            st.session_state.scores[cat] += 1
            st.session_state.step += 1
            st.rerun()
else:
    # RÉSULTAT
    gagnant = max(st.session_state.scores, key=st.session_state.scores.get)
    res = PROFILS[gagnant]
    
    st.markdown(f"""
        <div style="background: white; border-radius: 20px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); border-top: 10px solid {res['color']};">
            <div style="display: flex; justify-content: space-between; font-weight: bold;">
                <span style="color: {res['color']};">● {res['decision']}</span>
                <span style="color: gray;">{st.session_state.id_val}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 20px; margin-top: 20px;">
                <img src="{res['image']}" style="width: 120px; height: 120px; border-radius: 50%; border: 3px solid #1877f2; object-fit: cover;">
                <div>
                    <h2 style="margin:0;">SUJET ANALYSÉ</h2>
                    <p style="color: #1877f2; font-weight: bold; margin:0;">PROFIL : {gagnant.upper()}</p>
                    <p style="color: gray; font-size: 0.9rem;">RISQUE : {res['risk']}</p>
                </div>
            </div>
            <hr style="margin: 20px 0; opacity: 0.2;">
            <p style="font-size: 0.8rem; font-weight: bold; color: gray; text-transform: uppercase;">Note de l'IA de Sécurité</p>
            <p style="background: #f0f2f5; padding: 10px; border-radius: 10px; font-style: italic;">{res['note']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("RESCANNER"):
        st.session_state.step = 0
        st.session_state.scores = {k: 0 for k in PROFILS.keys()}
        st.rerun()
