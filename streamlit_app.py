import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="FRONTIER SCAN v1.4", layout="centered")

frontier_html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #0b0e14; color: #e0e0e0; display: flex; justify-content: center; padding: 10px; margin: 0; }
        #app-container { width: 100%; max-width: 500px; text-align: center; }
        .header-title { color: #00d2ff; font-size: 1.8rem; font-weight: 800; margin: 20px 0; text-transform: uppercase; }
        
        #quiz-zone { background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .progress-container { width: 100%; background-color: #30363d; border-radius: 10px; margin-bottom: 20px; height: 6px; }
        .progress-bar { height: 100%; background: #00d2ff; width: 0%; transition: 0.4s; }
        
        .btn-option { width: 100%; padding: 12px; margin: 6px 0; background: #21262d; color: white; border: 1px solid #30363d; border-radius: 10px; font-size: 0.95rem; cursor: pointer; transition: 0.2s; text-align: left; padding-left: 20px; }
        .btn-option:hover { background: #30363d; border-color: #58a6ff; }

        .alert-banner { background: #f85149; color: white; padding: 10px; border-radius: 10px; margin-bottom: 15px; font-weight: bold; display: none; }
        #result-card { display: none; background: #0d1117; border-radius: 20px; padding: 20px; border: 2px solid #30363d; text-align: left; }
        
        .photo-area { display: flex; gap: 15px; align-items: center; margin-bottom: 20px; }
        .photo-frame { width: 120px; height: 120px; border-radius: 12px; border: 2px solid #58a6ff; overflow: hidden; background: #000; flex-shrink: 0; }
        .photo-frame img { width: 100%; height: 100%; object-fit: cover; }
        
        .stat-label { display: flex; justify-content: space-between; font-size: 0.75rem; margin-top: 8px; color: #8b949e; font-weight: bold; }
        .stat-bar-bg { background: #30363d; height: 6px; border-radius: 3px; margin: 4px 0; width: 100%; }
        .stat-bar-fill { height: 100%; border-radius: 3px; transition: 1.5s ease-out; width: 0%; }
        
        .restart-btn { width: 100%; padding: 15px; background: #238636; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; margin-top: 20px; }
    </style>
</head>
<body>
    <div id="app-container">
        <div class="header-title">Frontier Scanner v1.4</div>
        
        <div id="quiz-zone">
            <div class="progress-container"><div id="p-bar" class="progress-bar"></div></div>
            <h3 id="q-text" style="font-size:1.1rem; min-height: 50px;">Analyse...</h3>
            <div id="options-zone"></div>
        </div>

        <div id="result-zone" style="display:none;">
            <div id="alert-banner" class="alert-banner">⚠️ INCOHÉRENCE : FAUSSE IDENTITÉ</div>
            <div id="result-card">
                <div class="photo-area">
                    <div class="photo-frame"><img id="res-img" src=""></div>
                    <div>
                        <h2 id="res-status" style="margin:0; font-size:1.2rem;">TERMINÉ</h2>
                        <p id="res-type" style="font-size:1.4rem; font-weight:800; margin:2px 0; color:#58a6ff;"></p>
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
            "Touriste": { r: "BAS", c: "#238636" },
            "Hacker": { r: "CRITIQUE", c: "#f85149" },
            "Trafiquant": { r: "ÉLEVÉ", c: "#da3633" },
            "Exile": { r: "MODÉRÉ", c: "#d29922" },
            "Ananas": { r: "BIO-RISQUE", c: "#f0883e" },
            "Agent": { r: "SÉCURISÉ", c: "#58a6ff" },
            "Artiste": { r: "BAS", c: "#bc8cff" },
            "Chercheur": { r: "CONTRÔLÉ", c: "#1f6feb" },
            "Evasion": { r: "FINANCIER", c: "#8957e5" }
        };

        // 10 QUESTIONS PRÉCISES
        const QS = [
            { q: "1. Quel est l'objet principal de votre visite ?", opt: [["Tourisme / Vacances", "Touriste"], ["Recherche scientifique", "Chercheur"], ["Mission diplomatique", "Agent"], ["Demande d'asile", "Exile"]] },
            { q: "2. Que transportez-vous dans ce boîtier ?", opt: [["Un appareil photo", "Artiste"], ["Un ordinateur renforcé", "Hacker"], ["Des échantillons biologiques", "Ananas"], ["Rien de particulier", "Touriste"]] },
            { q: "3. Quel est votre niveau d'études ?", opt: [["Doctorat / PhD", "Chercheur"], ["Autodidacte", "Hacker"], ["École d'Art", "Artiste"], ["Standard", "Touriste"]] },
            { q: "4. Comment avez-vous financé ce voyage ?", opt: [["Économies personnelles", "Touriste"], ["Bourse d'État", "Agent"], ["Cryptomonnaies", "Hacker"], ["Fonds offshore", "Evasion"]] },
            { q: "5. Quelle est votre destination finale ?", opt: [["Un hôtel de luxe", "Touriste"], ["Une banque privée", "Evasion"], ["Une zone protégée", "Exile"], ["Un centre de données", "Hacker"]] },
            { q: "6. (TEST PSY) Face à l'autorité, vous êtes :", opt: [["Coopératif", "Touriste"], ["Indifférent", "Agent"], ["Nerveux", "Trafiquant"], ["Provocateur", "Hacker"]] },
            { q: "7. Que pensez-vous du système de sécurité ?", opt: [["Nécessaire", "Agent"], ["Trop faible", "Hacker"], ["Intrusif", "Artiste"], ["Je ne sais pas", "Touriste"]] },
            { q: "8. (PIÈGE) Confirmez votre métier :", opt: [["Chercheur (Incohérence possible)", "Chercheur"], ["Artiste (Incohérence possible)", "Artiste"], ["Agent d'État", "Agent"], ["Sans emploi", "Exile"]] },
            { q: "9. Pourquoi votre passeport a-t-1 des traces d'usure ?", opt: [["Beaucoup voyagé", "Touriste"], ["Zone de guerre", "Exile"], ["C'est un duplicata", "Trafiquant"], ["Aucune idée", "Evasion"]] },
            { q: "10. Dernière question : Avez-vous quelque chose à cacher ?", opt: [["Absolument rien", "Touriste"], ["Ma vie privée", "Artiste"], ["Mes codes sources", "Hacker"], ["Je refuse de répondre", "Trafiquant"]] }
        ];

        let step = 0;
        let sc = { "Touriste":0, "Hacker":0, "Trafiquant":0, "Exile":0, "Ananas":0, "Agent":0, "Artiste":0, "Chercheur":0, "Evasion":0 };
        let firstChoice = "";

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
                        if(step === 0) firstChoice = o[1];
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

            // IA SIMULÉE : On calcule le gagnant et on vérifie l'incohérence
            const win = Object.keys(sc).reduce((a, b) => sc[a] > sc[b] ? a : b);
            
            // LOGIQUE D'INCOHÉRENCE (Plus intelligente)
            // Si le métier final (win) est différent du motif initial (firstChoice) alors qu'ils devraient être liés
            let lie = false;
            if (sc[firstChoice] < 10 && (firstChoice === "Chercheur" || firstChoice === "Agent")) {
                lie = true;
            }
            if (sc["Trafiquant"] > 15) lie = true;

            const data = PROFILS[win];

            if (lie) {
                document.getElementById("alert-banner").style.display = "block";
                document.getElementById("res-status").innerText = "ACCÈS REFUSÉ";
                document.getElementById("res-status").style.color = "#f85149";
            } else {
                document.getElementById("res-status").innerText = "ACCÈS ACCORDÉ";
                document.getElementById("res-status").style.color = "#3fb950";
                confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
            }

            // Image
            const imgEl = document.getElementById("res-img");
            imgEl.src = PATH + win.toLowerCase() + ".png";
            imgEl.onerror = () => { imgEl.src = "https://via.placeholder.com/120?text=SCAN"; };

            document.getElementById("res-type").innerText = win.toUpperCase();
            document.getElementById("res-risk").innerText = "RISQUE DÉTECTÉ : " + data.r;

            // Affichage des traits de personnalité (Top 4)
            const stats = document.getElementById("stats-panel");
            const sorted = Object.entries(sc).sort((a,b) => b[1] - a[1]).slice(0,4);
            
            sorted.forEach(([name, value]) => {
                if(value > 0) {
                    const row = document.createElement("div");
                    const label = name === "Hacker" ? "Instinct Hacker" : name === "Artiste" ? "Esprit Créatif" : name;
                    row.innerHTML = `
                        <div class="stat-label"><span>${label}</span><span>${value}%</span></div>
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
