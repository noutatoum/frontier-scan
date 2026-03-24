import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="FRONTIER SCAN v1.5", layout="centered")

frontier_html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #0b0e14; color: #e0e0e0; display: flex; justify-content: center; padding: 10px; margin: 0; }
        #app-container { width: 100%; max-width: 500px; text-align: center; }
        .header-title { color: #00d2ff; font-size: 1.8rem; font-weight: 800; margin: 20px 0; text-transform: uppercase; letter-spacing: 1px; }
        
        #quiz-zone { background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .progress-container { width: 100%; background-color: #30363d; border-radius: 10px; margin-bottom: 20px; height: 6px; }
        .progress-bar { height: 100%; background: linear-gradient(90deg, #00d2ff, #3a7bd5); width: 0%; transition: 0.4s; }
        
        .btn-option { width: 100%; padding: 12px; margin: 6px 0; background: #21262d; color: white; border: 1px solid #30363d; border-radius: 10px; font-size: 0.95rem; cursor: pointer; transition: 0.2s; text-align: left; padding-left: 20px; }
        .btn-option:hover { background: #30363d; border-color: #58a6ff; transform: scale(1.01); }

        #result-zone { display: none; }
        .alert-banner { background: #f85149; color: white; padding: 10px; border-radius: 10px; margin-bottom: 15px; font-weight: bold; animation: blink 1s infinite; display: none; text-transform: uppercase; font-size: 0.9rem; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.6; } 100% { opacity: 1; } }
        
        #result-card { background: #0d1117; border-radius: 20px; padding: 20px; border: 2px solid #30363d; text-align: left; }
        .photo-area { display: flex; gap: 15px; align-items: center; margin-bottom: 20px; }
        .photo-frame { width: 120px; height: 120px; border-radius: 12px; border: 2px solid #58a6ff; overflow: hidden; background: #000; flex-shrink: 0; }
        .photo-frame img { width: 100%; height: 100%; object-fit: cover; }
        
        .stat-label { display: flex; justify-content: space-between; font-size: 0.75rem; margin-top: 8px; color: #8b949e; font-weight: bold; text-transform: uppercase; }
        .stat-bar-bg { background: #30363d; height: 6px; border-radius: 3px; margin: 4px 0; width: 100%; overflow: hidden; }
        .stat-bar-fill { height: 100%; border-radius: 3px; transition: 1.5s cubic-bezier(0.1, 0, 0, 1); width: 0%; }
        
        .restart-btn { width: 100%; padding: 15px; background: #238636; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; margin-top: 20px; }
    </style>
</head>
<body>
    <div id="app-container">
        <div class="header-title">Frontier Scanner v1.5</div>
        
        <div id="quiz-zone">
            <div class="progress-container"><div id="p-bar" class="progress-bar"></div></div>
            <h3 id="q-text" style="font-size:1.1rem; min-height: 50px;">Analyse en cours...</h3>
            <div id="options-zone"></div>
        </div>

        <div id="result-zone">
            <div id="alert-banner" class="alert-banner">🚨 INCOHÉRENCE : FAUSSE IDENTITÉ DÉTECTÉE</div>
            <div id="result-card">
                <div class="photo-area">
                    <div class="photo-frame"><img id="res-img" src=""></div>
                    <div>
                        <h2 id="res-status" style="margin:0; font-size:1.2rem;">ANALYSE TERMINÉE</h2>
                        <p id="res-type" style="font-size:1.4rem; font-weight:800; margin:5px 0; color:#58a6ff;"></p>
                        <p id="res-risk" style="margin:0; font-size:0.8rem; font-family:monospace; color:#8b949e;"></p>
                    </div>
                </div>
                <div id="stats-panel"></div>
                <button class="restart-btn" onclick="location.reload()">NOUVELLE ANALYSE</button>
            </div>
        </div>
    </div>

    <script>
        const PATH = "https://raw.githubusercontent.com/noutatoum/gdp-dashboard/main/MonScanner/";
        
        const PROFILS = {
            "Touriste": { label: "Esprit Voyageur", r: "BAS", c: "#238636" },
            "Hacker": { label: "Instinct Hacker", r: "CRITIQUE", c: "#f85149" },
            "Trafiquant": { label: "Profil Suspect", r: "ÉLEVÉ", c: "#da3633" },
            "Exile": { label: "Profil Humanitaire", r: "MODÉRÉ", c: "#d29922" },
            "Ananas": { label: "Risque Bio", r: "BIO-DANGER", c: "#f0883e" },
            "Agent": { label: "Discipline d'État", r: "SÉCURISÉ", c: "#58a6ff" },
            "Artiste": { label: "Âme Créative", r: "BAS", c: "#bc8cff" },
            "Chercheur": { label: "Esprit Scientifique", r: "CONTRÔLÉ", c: "#1f6feb" },
            "Evasion": { label: "Tempérament Fiscal", r: "FINANCIER", c: "#8957e5" }
        };

        const QS = [
            { q: "1. Motif déclaré du séjour ?", opt: [["Vacances", "Touriste"], ["Recherche", "Chercheur"], ["Mission diplomatique", "Agent"], ["Asile", "Exile"]] },
            { q: "2. Contenu principal des bagages ?", opt: [["Vêtements", "Touriste"], ["Matériel informatique", "Hacker"], ["Outils de dessin", "Artiste"], ["Produits non identifiés", "Ananas"]] },
            { q: "3. Quel est votre domaine d'expertise ?", opt: [["Art et Design", "Artiste"], ["Cybersécurité", "Hacker"], ["Sciences", "Chercheur"], ["Commerce international", "Evasion"]] },
            { q: "4. Provenance de vos fonds ?", opt: [["Salaire", "Touriste"], ["Fonds d'État", "Agent"], ["Crypto-actifs", "Hacker"], ["Sociétés écrans", "Evasion"]] },
            { q: "5. Votre réaction face au scan corporel ?", opt: [["Coopératif", "Agent"], ["Amusé", "Artiste"], ["Nerveux", "Trafiquant"], ["Indifférent", "Touriste"]] },
            { q: "6. Destination finale de votre voyage ?", opt: [["Hôtel de ville", "Touriste"], ["Laboratoire B-12", "Chercheur"], ["Banque privée", "Evasion"], ["Inconnue", "Trafiquant"]] },
            { q: "7. Que pensez-vous des lois frontalières ?", opt: [["Nécessaires", "Agent"], ["Obsolètes", "Hacker"], ["Poétiques", "Artiste"], ["Contraignantes", "Evasion"]] },
            { q: "8. (PIÈGE) Quel est votre dernier diplôme ?", opt: [["Doctorat (Incohérent ?)", "Chercheur"], ["Autodidacte", "Hacker"], ["École d'Art", "Artiste"], ["Aucun", "Trafiquant"]] },
            { q: "9. État de vos documents officiels ?", opt: [["Neufs", "Agent"], ["Usés (voyages)", "Touriste"], ["Récemment modifiés", "Trafiquant"], ["Électroniques", "Hacker"]] },
            { q: "10. Quelque chose à déclarer ?", opt: [["Rien du tout", "Touriste"], ["Mes idées seulement", "Artiste"], ["Données cryptées", "Hacker"], ["Je refuse", "Trafiquant"]] }
        ];

        let step = 0;
        let sc = { "Touriste":0, "Hacker":0, "Trafiquant":0, "Exile":0, "Ananas":0, "Agent":0, "Artiste":0, "Chercheur":0, "Evasion":0 };
        let initialJob = "";

        function loadQ() {
            if (step < QS.length) {
                const curr = QS[step];
                document.getElementById("p-bar").style.width = ((step / QS.length) * 100) + "%";
                document.getElementById("q-text").innerText = curr.q;
                const zone = document.getElementById("options-zone");
                zone.innerHTML = "";
                curr.opt.forEach(o => {
                    const b = document.createElement("button");
                    b.className = "btn-option"; b.innerText = o[0];
                    b.onclick = () => { 
                        if(step === 0) initialJob = o[1];
                        sc[o[1]] += 10; 
                        step++; 
                        loadQ(); 
                    };
                    zone.appendChild(b);
                });
            } else { finish(); }
        }

        function finish() {
            document.getElementById("quiz-zone").style.display = "none";
            document.getElementById("result-zone").style.display = "block";

            // Calcul du gagnant
            const win = Object.keys(sc).reduce((a, b) => sc[a] > sc[b] ? a : b);
            
            // Correction de la logique de mensonge : 
            // On déclenche l'alerte seulement si le score de Trafiquant est élevé (>20) 
            // OU si le métier final est totalement différent du motif de départ (ex: départ Chercheur, fin Hacker)
            let isLying = (sc["Trafiquant"] >= 20);
            if(initialJob === "Chercheur" && sc["Chercheur"] < 10) isLying = true;

            const data = PROFILS[win];

            if (isLying) {
                document.getElementById("alert-banner").style.display = "block";
                document.getElementById("res-status").innerText = "ACCÈS REFUSÉ";
                document.getElementById("res-status").style.color = "#f85149";
            } else if (data.r === "BAS" || data.r === "SÉCURISÉ") {
                document.getElementById("res-status").innerText = "ACCÈS ACCORDÉ";
                document.getElementById("res-status").style.color = "#3fb950";
                confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
            }

            // Image
            const imgEl = document.getElementById("res-img");
            const fileName = win === "Evasion" ? "evasion.png" : win.toLowerCase() + ".png";
            imgEl.src = PATH + fileName;
            imgEl.onerror = () => { imgEl.src = "https://via.placeholder.com/120?text=SCAN"; };

            document.getElementById("res-type").innerText = data.label;
            document.getElementById("res-risk").innerText = "NIVEAU DE RISQUE : " + data.r;

            // Affichage des statistiques Top 4
            const stats = document.getElementById("stats-panel");
            const sorted = Object.entries(sc).sort((a,b) => b[1] - a[1]).slice(0,4);
            
            sorted.forEach(([name, value]) => {
                if(value > 0) {
                    const row = document.createElement("div");
                    row.innerHTML = `
                        <div class="stat-label"><span>${PROFILS[name].label}</span><span>${value}%</span></div>
                        <div class="stat-bar-bg"><div class="stat-bar-fill" style="width:${value}%; background:${PROFILS[name].c}"></div></div>
                    `;
                    stats.appendChild(row);
                }
            });
        }
        loadQ();
    </script>
</body>
</html>
"""

components.html(frontier_html, height=850)
