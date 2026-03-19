import streamlit as st
import streamlit.components.v1 as components

# Configuration de la page Streamlit
st.set_page_config(page_title="FRONTIER SCAN", layout="centered")

# On définit le code HTML/JS à l'intérieur d'une variable Python
frontier_html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #0e1621;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            padding: 20px;
        }
        #app-container {
            width: 100%;
            max-width: 450px;
            background: #1b2838;
            padding: 30px;
            border-radius: 25px;
            box-shadow: 0 15px 50px rgba(0,0,0,0.5);
            border: 1px solid #30475e;
            text-align: center;
        }
        h1 { color: #00d2ff; font-size: 1.6rem; text-transform: uppercase; letter-spacing: 2px; }
        .btn-option {
            width: 100%;
            padding: 15px;
            margin: 10px 0;
            background: transparent;
            color: #00d2ff;
            border: 2px solid #00d2ff;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }
        .btn-option:hover { background: #00d2ff; color: #0e1621; box-shadow: 0 0 20px rgba(0, 210, 255, 0.4); }
        .result-card { display: none; }
        .photo-frame {
            width: 160px;
            height: 160px;
            border-radius: 20px;
            border: 3px solid #00d2ff;
            margin: 20px auto;
            overflow: hidden;
            background: #0e1621;
        }
        .photo-frame img { width: 100%; height: 100%; object-fit: cover; }
        .status-badge { padding: 8px 20px; border-radius: 30px; font-weight: bold; display: inline-block; margin-bottom: 15px; }
        #alert-banner {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #d93025;
            color: white;
            text-align: center;
            padding: 15px;
            font-weight: bold;
            z-index: 1000;
            font-size: 1.2rem;
        }
    </style>
</head>
<body>

    <div id="alert-banner">🚨 ALERTE : INDIVIDU SUSPECT DÉTECTÉ 🚨</div>

    <div id="app-container">
        <div id="quiz-zone">
            <h1>🛂 FRONTIER SCAN</h1>
            <p id="question-text" style="color: #84a1c0; font-weight: bold; margin-bottom: 20px;"></p>
            <div id="options-zone"></div>
        </div>

        <div id="result-zone" class="result-card">
            <div id="status-display" class="status-badge">ANALYSE TERMINÉE</div>
            <div class="photo-frame">
                <img id="result-photo" src="" alt="Profil">
            </div>
            <h2 id="result-profile" style="color: #00d2ff; margin: 5px 0;">PROFIL</h2>
            <p id="result-note" style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px; font-style: italic; font-size: 0.9rem;"></p>
            <button class="btn-option" onclick="location.reload()">NOUVELLE ANALYSE</button>
        </div>
    </div>

    <script>
        // LIEN GITHUB POUR LES IMAGES
        const PATH = "https://raw.githubusercontent.com/noutatoum/gdp-dashboard/main/MonScanner/"; 

        const PROFILS = {
            "Touriste": { status: "AUTORISÉ", color: "#42b72a", img: "touriste.png", note: "Voyageur standard. Visa en règle. Séjour temporaire validé." },
            "Hacker": { status: "DÉTENU", color: "#d93025", img: "hacker.png", note: "Tentative d'intrusion réseau détectée sur le portail sécurisé." },
            "Trafiquant": { status: "INTERPELLÉ", color: "#d93025", img: "trafiquant.png", note: "Marchandises illicites détectées via scanner thermique." },
            "Exile": { status: "EN ATTENTE", color: "#fabb3a", img: "exile.png", note: "Dossier de protection internationale en cours de vérification." },
            "Ananas": { status: "DÉTRUIT", color: "#d93025", img: "ananas.png", note: "Bio-organisme non identifié. Risque de contamination." },
            "Agent": { status: "VALIDE", color: "#42b72a", img: "agent.png", note: "Mission officielle diplomatique. Priorité de transit accordée." },
            "Evasion": { status: "SIGNALÉ", color: "#fabb3a", img: "evasion.png", note: "Flux de capitaux suspects suspects." },
            "Artiste": { status: "AUTORISÉ", color: "#42b72a", img: "artiste.png", note: "Sujet créatif. Aucune menace identifiée." },
            "Chercheur": { status: "CONTRÔLÉ", color: "#1877f2", img: "chercheur.png", note: "Transport de matériel scientifique sous protocole strict." }
        };

        const QUESTIONS = [
            { q: "Motif de passage ?", options: [["Vacances", "Touriste"], ["Aide", "Agent"], ["Optimisation", "Evasion"], ["Asile", "Exile"]] },
            { q: "Contenu des bagages ?", options: [["Vêtements", "Touriste"], ["Serveurs", "Hacker"], ["Bio-Scan", "Ananas"], ["Rien", "Exile"]] },
            { q: "Ressources ?", options: [["Salaire", "Touriste"], ["Crypto", "Hacker"], ["Offshore", "Evasion"], ["Néant", "Exile"]] },
            { q: "Document ?", options: [["Passeport", "Touriste"], ["Diplomatique", "Agent"], ["Déchiré", "Exile"], ["Faux", "Trafiquant"]] },
            { q: "Appareils ?", options: [["Smartphone", "Touriste"], ["Laptop", "Hacker"], ["Brouilleur", "Trafiquant"], ["Éprouvettes", "Chercheur"]] },
            { q: "Réaction ?", options: [["Calme", "Agent"], ["Sueur", "Trafiquant"], ["Mépris", "Evasion"], ["Silence", "Ananas"]] },
            { q: "Profession ?", options: [["Étudiant", "Touriste"], ["Expert Cyber", "Hacker"], ["Peintre", "Artiste"], ["Biologiste", "Chercheur"]] },
            { q: "Destination ?", options: [["Hôtel", "Touriste"], ["Banque", "Evasion"], ["Laboratoire", "Chercheur"], ["Zone B", "Exile"]] },
            { q: "Durée ?", options: [["1 semaine", "Touriste"], ["Indéfini", "Exile"], ["48h", "Agent"], ["24h", "Ananas"]] },
            { q: "Dernier Pays ?", options: [["Schengen", "Touriste"], ["Paradis Fiscal", "Evasion"], ["Zone Conflit", "Exile"], ["Inconnu", "Ananas"]] }
        ];

        let step = 0;
        let scores = { "Touriste":0, "Hacker":0, "Trafiquant":0, "Exile":0, "Ananas":0, "Agent":0, "Evasion":0, "Artiste":0, "Chercheur":0 };

        function showQuestion() {
            if (step < QUESTIONS.length) {
                const current = QUESTIONS[step];
                document.getElementById("question-text").innerText = `SCAN ${step + 1}/10 : ${current.q}`;
                const zone = document.getElementById("options-zone");
                zone.innerHTML = "";
                current.options.forEach(opt => {
                    const btn = document.createElement("button");
                    btn.className = "btn-option";
                    btn.innerText = opt[0];
                    btn.onclick = () => { scores[opt[1]]++; step++; showQuestion(); };
                    zone.appendChild(btn);
                });
            } else { showResult(); }
        }

        function showResult() {
            document.getElementById("quiz-zone").style.display = "none";
            document.getElementById("result-zone").style.display = "block";
            const gagnant = Object.keys(scores).reduce((a, b) => scores[a] > scores[b] ? a : b);
            const res = PROFILS[gagnant];

            document.getElementById("status-display").innerText = res.status;
            document.getElementById("status-display").style.background = res.color;
            document.getElementById("result-photo").src = PATH + res.img;
            document.getElementById("result-profile").innerText = `PROFIL : ${gagnant.toUpperCase()}`;
            document.getElementById("result-note").innerText = res.note;

            if (["AUTORISÉ", "VALIDE"].includes(res.status)) {
                confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
            } else if (["DÉTENU", "INTERPELLÉ", "DÉTRUIT"].includes(res.status)) {
                document.getElementById("alert-banner").style.display = "block";
            }
        }
        showQuestion();
    </script>
</body>
</html>
"""

# Injection du code dans l'app Streamlit
components.html(frontier_html, height=800, scrolling=False)
