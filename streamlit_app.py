import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="FRONTIER SCAN v1.1", layout="centered")

frontier_html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f8f9fa; display: flex; justify-content: center; padding: 20px; margin: 0; }
        #app-container { width: 100%; max-width: 600px; text-align: center; }
        .header-title { color: #00d2ff; font-size: 2.5rem; font-weight: 800; margin-bottom: 20px; }
        .progress-container { width: 100%; background-color: #ddd; border-radius: 10px; margin-bottom: 25px; height: 12px; overflow: hidden; border: 1px solid #ccc; }
        .progress-bar { height: 100%; background-color: #00d2ff; width: 0%; transition: 0.4s ease-out; }
        .btn-option { width: 100%; padding: 16px; margin: 10px 0; background: white; color: #1c1e21; border: 1px solid #ddd; border-radius: 12px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .btn-option:hover { background: #f0f2f5; border-color: #00d2ff; transform: translateY(-2px); }
        #access-bar { display: none; width: 100%; padding: 15px; border-radius: 12px; margin-bottom: 15px; font-weight: bold; text-align: left; font-size: 1.1rem; border-left: 5px solid; }
        #result-card { display: none; background: #1b2838; border-radius: 20px; padding: 30px; border-bottom: 6px solid #42b72a; text-align: left; position: relative; animation: slideUp 0.6s cubic-bezier(0.23, 1, 0.32, 1); }
        .id-number { position: absolute; top: 20px; right: 25px; color: white; opacity: 0.6; font-family: monospace; font-size: 1.1rem; }
        .photo-frame { width: 190px; height: 190px; border-radius: 18px; border: 3px solid #42b72a; overflow: hidden; background: #0e1621; flex-shrink: 0; display: flex; align-items: center; justify-content: center; }
        .photo-frame img { width: 100%; height: 100%; object-fit: cover; object-position: center top; }
        .terminal-box { background: #0e1621; padding: 18px; border-radius: 12px; border-left: 4px solid #42b72a; color: #42b72a; font-family: 'Courier New', monospace; font-size: 1.05rem; }
        #restart-btn { display: none; width: 100%; padding: 15px; margin-top: 25px; background: #00d2ff; color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 1.1rem; cursor: pointer; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div id="app-container">
        <div class="header-title">⚡ FRONTIER SCAN ⚡</div>
        <div id="quiz-zone">
            <div class="progress-container"><div id="p-bar" class="progress-bar"></div></div>
            <h3 id="q-text" style="color: #1c1e21;">Analyse...</h3>
            <div id="options-zone"></div>
        </div>
        <div id="result-zone">
            <div id="access-bar"></div>
            <div id="result-card">
                <span class="id-number" id="res-id"></span>
                <div style="display:flex; gap:25px; align-items:center; margin-bottom:30px;">
                    <div class="photo-frame"><img id="res-img" src=""></div>
                    <div class="info-text">
                        <h2>SUJET IDENTIFIÉ</h2>
                        <p class="profile-type" id="res-type"></p>
                        <p id="res-risk" style="color:#84a1c0; font-size:0.95rem; font-weight:bold;"></p>
                    </div>
                </div>
                <div class="terminal-box">> <span id="res-note"></span></div>
            </div>
            <button id="restart-btn" onclick="location.reload()">RESCANNER</button>
        </div>
    </div>

    <script>
        const PATH = "https://raw.githubusercontent.com/noutatoum/gdp-dashboard/main/MonScanner/";

        const PROFILS = {
            "Touriste": { s: "AUTORISÉ", c: "#42b72a", img: "touriste.png", f: "touriste.png", n: "Voyageur standard. Visa en règle.", r: "BAS", msg: "🔓 ACCÈS ACCORDÉ", bc: "#e8f5e9" },
            "Hacker": { s: "DÉTENU", c: "#d93025", img: "hacker.png", f: "hacker.png", n: "Matériel d'intrusion détecté.", r: "CRITIQUE", msg: "🚨 ALERTE SÉCURITÉ", bc: "#ffebee" },
            "Trafiquant": { s: "INTERPELLÉ", c: "#d93025", img: "trafiquant.png", f: "trafiquant.png", n: "Contrebande suspectée.", r: "ÉLEVÉ", msg: "🚨 INTERCEPTION", bc: "#ffebee" },
            "Exile": { s: "EN ATTENTE", c: "#fabb3a", img: "exile.png", f: "exile.png", n: "Dossier humanitaire en cours.", r: "MODÉRÉ", msg: "⚠️ EXAMEN REQUIS", bc: "#fff3e0" },
            "Ananas": { s: "SAISI", c: "#d93025", img: "ananas.png", f: "ananas.png", n: "Risque biologique détecté.", r: "BIO-RISQUE", msg: "🚫 BIO-DANGER", bc: "#ffebee" },
            "Agent": { s: "VALIDE", c: "#42b72a", img: "agent.png", f: "agent.png", n: "Mission d'État confirmée.", r: "AUCUN", msg: "🔓 PRIORITÉ DIPLOMATIQUE", bc: "#e8f5e9" },
            "Artiste": { s: "AUTORISÉ", c: "#42b72a", img: "artiste.png", f: "artiste.png", n: "Sujet créatif. Pas de menace.", r: "BAS", msg: "🔓 ACCÈS ACCORDÉ", bc: "#e8f5e9" },
            "Chercheur": { s: "CONTRÔLÉ", c: "#1877f2", img: "chercheur.png", f: "chercheur.png", n: "Matériel scientifique certifié.", r: "MODÉRÉ", msg: "🔍 CONTRÔLE SCIENTIFIQUE", bc: "#e3f2fd" },
            "Evasion": { s: "SIGNALÉ", c: "#fabb3a", img: "evasion.png", f: "evasion.png", n: "Capitaux suspects. Signalement fiscal.", r: "FINANCIER", msg: "⚠️ SIGNALEMENT FISCAL", bc: "#fff3e0" }
        };

        const QS = [
            { q: "Motif du passage ?", opt: [["Vacances", "Touriste"], ["Mission État", "Agent"], ["Optimisation fiscale", "Evasion"], ["Asile politique", "Exile"]] },
            { q: "Contenu bagages ?", opt: [["Vêtements", "Touriste"], ["Serveurs chiffrés", "Hacker"], ["Spécimen végétal", "Ananas"], ["Toiles et pinceaux", "Artiste"]] },
            { q: "Profession ?", opt: [["Salarié", "Touriste"], ["Trader / Banquier", "Evasion"], ["Sculpteur", "Artiste"], ["Chercheur", "Chercheur"]] },
            { q: "Comportement ?", opt: [["Impassible", "Agent"], ["Sueur / Nervosité", "Trafiquant"], ["Dédain", "Evasion"], ["Confusion", "Ananas"]] },
            { q: "Document ?", opt: [["Passeport Bio", "Touriste"], ["Ordre de mission", "Agent"], ["Sans papiers", "Exile"], ["Faux visa", "Trafiquant"]] },
            { q: "Électronique ?", opt: [["Smartphone", "Touriste"], ["Microscope", "Chercheur"], ["Brouilleur signal", "Trafiquant"], ["Antenne piratage", "Hacker"]] },
            { q: "Finances ?", opt: [["Salaire fixe", "Touriste"], ["Monero (Anonyme)", "Hacker"], ["Fonds offshore", "Evasion"], ["Néant", "Exile"]] },
            { q: "Destination ?", opt: [["Hôtel", "Touriste"], ["Banque privée", "Evasion"], ["Laboratoire", "Chercheur"], ["Zone B-12", "Exile"]] },
            { q: "Durée du séjour ?", opt: [["15 jours", "Touriste"], ["Permanent", "Exile"], ["48h (Transit)", "Agent"], ["Escale technique", "Ananas"]] },
            { q: "Provenance ?", opt: [["Espace Schengen", "Touriste"], ["Zone de conflit", "Exile"], ["Paradis fiscal", "Evasion"], ["Inconnu", "Ananas"]] }
        ];

        let step = 0;
        let sc = { "Touriste":0, "Hacker":0, "Trafiquant":0, "Exile":0, "Ananas":0, "Agent":0, "Artiste":0, "Chercheur":0, "Evasion":0 };

        function loadQ() {
            if (step < QS.length) {
                const curr = QS[step];
                document.getElementById("p-bar").style.width = ((step / QS.length) * 100) + "%";
                document.getElementById("q-text").innerText = `ÉTAPE ${step + 1} / 10 : ${curr.q}`;
                const zone = document.getElementById("options-zone");
                zone.innerHTML = "";
                curr.opt.forEach(o => {
                    const b = document.createElement("button");
                    b.className = "btn-option"; b.innerText = o[0];
                    b.onclick = () => { sc[o[1]] += 10; step++; loadQ(); };
                    zone.appendChild(b);
                });
            } else { finish(); }
        }

        function finish() {
            document.getElementById("quiz-zone").style.display = "none";
            document.getElementById("result-card").style.display = "block";
            document.getElementById("restart-btn").style.display = "block";

            // On ajoute un petit aléatoire aux scores pour départager les égalités à 0
            const win = Object.keys(sc).reduce((a, b) => (sc[a] + Math.random()) > (sc[b] + Math.random()) ? a : b);
            const r = PROFILS[win];

            const bar = document.getElementById("access-bar");
            bar.style.display = "block"; bar.style.background = r.bc; bar.style.color = r.c; bar.style.borderColor = r.c; bar.innerText = r.msg;

            const img = document.getElementById("res-img");
            img.onerror = function() { this.src = PATH + r.f; }; 
            img.src = PATH + r.img;

            document.getElementById("res-type").innerText = win.toUpperCase();
            document.getElementById("res-type").style.color = r.c;
            document.getElementById("res-risk").innerText = `RISQUE : ${r.r}`;
            document.getElementById("res-note").innerText = r.n;
            document.getElementById("res-id").innerText = "ID-" + Math.floor(10000 + Math.random() * 90000);
            document.getElementById("result-card").style.borderColor = r.c;

            if (r.s === "AUTORISÉ" || r.s === "VALIDE") {
                confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
            }
        }
        loadQ();
    </script>
</body>
</html>
"""

components.html(frontier_html, height=920, scrolling=False)
