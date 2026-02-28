import streamlit as st
import streamlit.components.v1 as components

# 1. Configuración de pantalla ancha
st.set_page_config(page_title="Memoria: Animales Salvajes", layout="wide")

# Estilo para eliminar márgenes extra de Streamlit y que se vea profesional
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    iframe { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. El Código del Juego con el diseño "Selva" recuperado
html_salvajes = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        :root {
            --verde-selva: #1b4332;
            --verde-medio: #2d6a4f;
            --naranja: #ff9f1c;
            --crema: #f8f9fa;
        }

        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(rgba(27, 67, 50, 0.8), rgba(27, 67, 50, 0.8)), 
                        url('https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=1350&q=80');
            background-size: cover;
            margin: 0;
            padding: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }

        header { text-align: center; color: white; margin-bottom: 10px; }
        h1 { margin: 0; font-size: 2.2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); font-weight: 800; }
        .brand { font-style: italic; color: #95d5b2; font-size: 1rem; }

        .game-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 12px;
            width: 95%;
            max-width: 850px;
            perspective: 1000px;
        }

        .card {
            aspect-ratio: 1 / 1;
            position: relative;
            cursor: pointer;
            transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
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
            border: 4px solid white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }

        /* CARA FRONTAL (La que se ve al inicio - DISEÑO RECUPERADO) */
        .card-front {
            background: linear-gradient(45deg, #1b4332, #40916c);
            background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40"><path d="M0 40 L40 0 M10 40 L40 10 M20 40 L40 20 M30 40 L40 30 M0 30 L30 0 M0 20 L20 0 M0 10 L10 0" stroke="rgba(255,255,255,0.1)" stroke-width="2" fill="none"/></svg>');
            z-index: 2;
        }

        /* Texto/Figuritas en la cara frontal */
        .card-front::after {
            content: '🌿🐆🐒🌿';
            font-size: 1.2rem;
            text-align: center;
            color: rgba(255,255,255,0.8);
            letter-spacing: 2px;
        }

        /* CARA TRASERA (Al voltear) */
        .card-back {
            background-color: var(--crema);
            transform: rotateY(180deg);
            padding: 5px;
        }

        .card.matched .card-back {
            background-color: #d8f3dc;
            border-color: #b7e4c7;
        }

        .card-image { font-size: 4.5rem; } /* FIGURAS GIGANTES */
        .card-text { font-size: 1.2rem; font-weight: 900; color: var(--verde-selva); text-align: center; text-transform: uppercase; }

        #final-screen {
            position: fixed; inset: 0;
            background: rgba(0, 0, 0, 0.9);
            display: none; flex-direction: column;
            justify-content: center; align-items: center;
            z-index: 200; color: white; text-align: center;
        }

        .btn-restart {
            padding: 15px 35px; background: var(--naranja);
            color: white; border: none; border-radius: 30px;
            font-size: 1.4rem; font-weight: bold; cursor: pointer; margin-top: 20px;
            box-shadow: 0 5px 15px rgba(255, 159, 28, 0.4);
        }
    </style>
</head>
<body>
    <header>
        <h1>Memoria: Animales Salvajes</h1>
        <div class="brand">PaoSpanishTeacher</div>
    </header>

    <main class="game-container" id="game-board"></main>

    <div id="final-screen">
        <span style="font-size: 5rem;">🦁🐘🦒</span>
        <h2>¡INCREÍBLE!</h2>
        <p style="font-size: 1.5rem;">Lograste encontrar todos los animales de la selva.</p>
        <button class="btn-restart" onclick="location.reload()">JUGAR OTRA VEZ</button>
    </div>

    <script>
        const ANIMALES = [
            { n: "León", i: "🦁" }, { n: "Tigre", i: "🐯" }, { n: "Elefante", i: "🐘" },
            { n: "Jirafa", i: "🦒" }, { n: "Mono", i: "🐒" }, { n: "Cebra", i: "🦓" },
            { n: "Oso", i: "🐻" }, { n: "Cocodrilo", i: "🐊" }, { n: "Rino", i: "🦏" },
            { n: "Hippo", i: "🦛" }
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
                        ${d.t === 'img' ? `<span class="card-image">${d.v}</span>` : `<span class="card-text">${d.v}</span>`}
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
                c1.classList.add('matched');
                c2.classList.add('matched');
                flipped = [];
                locked = false;
                if (matched === ANIMALES.length) {
                    confetti({ particleCount: 200, spread: 70, origin: { y: 0.6 } });
                    setTimeout(() => document.getElementById('final-screen').style.display = 'flex', 600);
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

# 3. Altura de visualización
components.html(html_salvajes, height=900, scrolling=False)
