import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Memoria: Animales Salvajes", layout="wide")

# Tu código HTML de Animales Salvajes
html_salvajes = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Memoria - Animales Salvajes</title>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        :root {
            --verde-selva: #2d6a4f;
            --verde-claro: #95d5b2;
            --naranja-tigre: #ff9f1c;
            --crema: #f8f9fa;
            --texto: #1b4332;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(rgba(45, 106, 79, 0.7), rgba(45, 106, 79, 0.7)), 
                        url('https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=1350&q=80');
            background-size: cover;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }

        header { text-align: center; margin-bottom: 20px; color: white; }
        h1 { font-size: 2.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }

        .game-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 12px;
            max-width: 850px;
            width: 100%;
            perspective: 1000px;
        }

        .card {
            aspect-ratio: 3/4;
            position: relative;
            cursor: pointer;
            transform-style: preserve-3d;
            transition: transform 0.6s;
        }

        .card.flipped { transform: rotateY(180deg); }

        .card-face {
            position: absolute;
            width: 100%; height: 100%;
            backface-visibility: hidden;
            border-radius: 12px;
            display: flex;
            justify-content: center;
            align-items: center;
            border: 3px solid white;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }

        .card-front {
            background: linear-gradient(45deg, #1b4332, #40916c);
            z-index: 2;
        }
        .card-front::after { content: '🌿🐆'; font-size: 1.5rem; }

        .card-back {
            background-color: var(--crema);
            transform: rotateY(180deg);
        }

        .card-image { font-size: 3.5rem; }
        .card-text { font-size: 1.2rem; font-weight: bold; color: var(--verde-selva); text-align: center; }

        #final-screen {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.9);
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 200;
            color: white;
            text-align: center;
        }

        .btn-restart {
            padding: 15px 30px;
            background: var(--naranja-tigre);
            color: white;
            border: none;
            border-radius: 30px;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <header>
        <h1>Animales Salvajes</h1>
        <p>PaoSpanishTeacher</p>
    </header>

    <main class="game-container" id="game-board"></main>

    <div id="final-screen">
        <span style="font-size: 4rem;">🏆</span>
        <h2>¡Felicidades!</h2>
        <p>Dominaste la selva y encontraste todos los animales.</p>
        <button class="btn-restart" onclick="location.reload()">Jugar otra vez</button>
    </div>

    <script>
        const ANIMALES = [
            { n: "León", i: "🦁" }, { n: "Tigre", i: "🐯" }, { n: "Elefante", i: "🐘" },
            { n: "Jirafa", i: "🦒" }, { n: "Mono", i: "🐒" }, { n: "Cebra", i: "🦓" },
            { n: "Oso", i: "🐻" }, { n: "Cocodrilo", i: "🐊" }, { n: "Rinoceronte", i: "🦏" },
            { n: "Hipopótamo", i: "🦛" }
        ];

        let flipped = [];
        let matched = 0;
        let locked = false;

        function createBoard() {
            const board = document.getElementById('game-board');
            let deck = [];
            ANIMALES.forEach(a => {
                deck.push({ t: 'text', v: a.n, id: a.n });
                deck.push({ t: 'img', v: a.i, id: a.n });
            });
            deck.sort(() => Math.random() - 0.5);
            deck.forEach(d => {
                const card = document.createElement('div');
                card.className = 'card';
                card.dataset.id = d.id;
                card.innerHTML = `
                    <div class="card-face card-front"></div>
                    <div class="card-face card-back">
                        ${d.t === 'text' ? `<span class="card-text">${d.v}</span>` : `<span class="card-image">${d.v}</span>`}
                    </div>`;
                card.onclick = () => flip(card);
                board.appendChild(card);
            });
        }

        function flip(card) {
            if (locked || card.classList.contains('flipped')) return;
            card.classList.add('flipped');
            flipped.push(card);
            if (flipped.length === 2) check();
        }

        function check() {
            locked = true;
            const [c1, c2] = flipped;
            if (c1.dataset.id === c2.dataset.id) {
                matched++;
                flipped = [];
                locked = false;
                if (matched === ANIMALES.length) {
                    confetti();
                    setTimeout(() => document.getElementById('final-screen').style.display = 'flex', 500);
                }
            } else {
                setTimeout(() => {
                    c1.classList.remove('flipped');
                    c2.classList.remove('flipped');
                    flipped = [];
                    locked = false;
                }, 1000);
            }
        }
        createBoard();
    </script>
</body>
</html>
"""

components.html(html_salvajes, height=900, scrolling=False)
