import streamlit as st
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="FRONTIER  SCAN", page_icon="🕵️‍♂️", layout="centered")

# --- 2. BASE DE DONNÉES DES 9 PROFILS ---
PROFILS = {
    "Touriste": {"decision": "AUTORISÉ", "risk": "BAS", "color": "#42b72a", "image": "touriste.jpg", "note": "Voyageur standard. Visa valide."},
    "Hacker": {"decision": "REFUSÉ / DÉTENU", "risk": "CRITIQUE", "color": "#d93025", "image": "hacker.jpg", "note": "Tentative d'intrusion réseau détectée."},
    "Trafiquant": {"decision": "REFUSÉ / INTERPELLÉ", "risk": "ÉLEVÉ", "color": "#d93025", "image": "trafiquant.jpg", "note": "Contrebande suspectée via scanner THz."},
    "Exilé": {"decision": "EN ATTENTE D'ASILE", "risk": "MODÉRÉ", "color": "#fabb3a", "image": "exile.jpg", "note": "Demande de protection internationale déposée."},
    "Ananas": {"decision": "SAISI / DÉTRUIT", "risk": "BIO-RISQUE", "color": "#d93025", "image": "ananas.jpg", "note": "Organisme non identifié. Risque de contamination."},
    "Agent": {"decision": "VALIDE (Diplomate)", "risk": "AUCUN", "color": "#42b72a", "image": "agent.jpg", "note": "Mission diplomatique officielle validée."},
    "Evasion": {"decision": "SIGNALÉ AU FISC", "risk": "FINANCIER", "color": "#fabb3a", "image": "evasion.jpg", "note": "Flux de capitaux suspects non déclarés."},
    "Artiste": {"decision": "AUTORISÉ", "risk": "BAS", "color": "#42b72a", "image": "artiste.jpg", "note": "Sujet créatif. Pas de menace détectée."},
    "Chercheur": {"decision": "AUTORISÉ (Contrôlé)", "risk": "MODÉRÉ", "color": "#1877f2", "image": "chercheur.jpg", "note": "Transport d'échantillons scientifiques autorisés."}
}

# --- 3. LES 10 QUESTIONS ---
QUESTIONS = [
    ("Motif principal ?", [("Vacances", "Touriste"), ("Diplomatie", "Agent"), ("Optimisation", "Evasion"), ("Asile", "Exilé")]),
    ("Contenu bagages ?", [("Vêtements", "Touriste"), ("Serveurs", "Hacker"), ("Bio-Scan", "Ananas"), ("Rien", "Exilé")]),
    ("Ressources ?", [("Salaire", "Touriste"), ("Blockchain", "Hacker"), ("Offshore", "Evasion"), ("Néant", "Exilé")]),
    ("Document ?", [("Passeport", "Touriste"), ("Mission", "Agent"), ("Déchiré", "Exilé"), ("Faux", "Trafiquant")]),
    ("Appareils ?", [("Smartphone", "Touriste"), ("Laptop", "Hacker"), ("Brouilleur", "Trafiquant"), ("Échantillons", "Chercheur")]),
    ("Réaction Scan ?", [("Calme", "Agent"), ("Sueur", "Trafiquant"), ("Mépris", "Evasion"), ("Silence", "Ananas")]),
    ("Profession ?", [("Étudiant", "Touriste"), ("Expert Cyber", "Hacker"), ("Peintre", "Artiste"), ("Biologiste", "Chercheur")]),
    ("Destination ?", [("Hôtel", "Touriste"), ("Banque", "Evasion"), ("Laboratoire", "Chercheur"), ("Camp", "Exilé")]),
    ("Durée séjour ?", [("1 semaine", "Touriste"), ("Indéfini", "Exilé"), ("48h", "Agent"), ("24h", "Ananas")]),
    ("Dernier Pays ?", [("Schengen", "Touriste"), ("Paradis Fiscal", "Evasion"), ("Zone Conflit", "Exilé"), ("Inconnu", "Ananas")])
]

# --- 4. INITIALISATION ---
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.scores = {k: 0 for k in PROFILS.keys()}
    st.session_state.id_val = f"ID-{random.randint(10000, 99999)}"

st.markdown("<h1 style='color: #00d2ff; text-align: center; text-transform: uppercase;'>⚡️ FRONTIER AI SCANNER ⚡️</h1>", unsafe_allow_html=True)

if st.session_state.step < len(QUESTIONS):
    # Barre de scan animée
    st.progress(st.session_state.step / len(QUESTIONS))
    q_text, options = QUESTIONS[st.session_state.step]
    st.subheader(f"PROTOCOLE {st.session_state.step + 1} : {q_text}")
    
    # Design des boutons
    for text, cat in options:
        if st.button(text, key=text+str(st.session_state.step), use_container_width=True):
            st.session_state.scores[cat] += 2
            st.session_state.step += 1
            st.rerun()
else:
    # --- RÉSULTAT FINAL ---
    gagnant = max(st.session_state.scores, key=st.session_state.scores.get)
    res = PROFILS[gagnant]
    
    # Effets de transition
    with st.spinner('CALCUL DES DONNÉES BIOMÉTRIQUES...'):
        time.sleep(1)

    # Effets de succès ou d'alerte
    if "AUTORISÉ" in res['decision'] or "VALIDE" in res['decision']:
        st.snow()
        st.success("🔓 ACCÈS ACCORDÉ")
    elif "REFUSÉ" in res['decision'] or "DÉTENU" in res['decision']:
        st.error(f"🚨 ALERTE : {res['decision']}")
    else:
        st.warning("⚠️ DOSSIER SOUS SURVEILLANCE")

    # Carte ID Graphique
    st.markdown(f"""
        <div style="background: #1b2838; border-radius: 20px; padding: 25px; border: 2px solid {res['color']}; color: white;">
            <div style="display: flex; justify-content: space-between; font-family: monospace;">
                <span style="color: {res['color']};">● STATUS: {res['decision']}</span>
                <span>{st.session_state.id_val}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 20px; margin-top: 20px;">
                <img src="{res['image']}" style="width: 140px; height: 140px; border-radius: 15px; border: 2px solid {res['color']}; object-fit: cover;">
                <div>
                    <h2 style="margin:0; color: #00d2ff;">SUJET IDENTIFIÉ</h2>
                    <p style="color: {res['color']}; font-weight: bold; margin:0; font-size: 1.2rem;">{gagnant.upper()}</p>
                    <p style="color: #84a1c0; font-size: 0.9rem; margin:0;">RISQUE : {res['risk']}</p>
                </div>
            </div>
            <hr style="border: 0.1px solid #30475e; margin: 20px 0;">
            <p style="font-size: 0.7rem; color: #84a1c0; text-transform: uppercase;">Analyse IA Terminal</p>
            <p style="background: #0e1621; padding: 15px; border-radius: 10px; font-family: monospace; color: #42b72a; border-left: 5px solid {res['color']};">
                > {res['note']}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("NOUVELLE ANALYSE", use_container_width=True):
        st.session_state.step = 0
        st.session_state.scores = {k: 0 for k in PROFILS.keys()}
        st.session_state.id_val = f"ID-{random.randint(10000, 99999)}"
        st.rerun()
