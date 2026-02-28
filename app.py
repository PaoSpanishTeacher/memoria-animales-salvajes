import streamlit as st
import streamlit.components.v1 as components

# 1. Configuración de pantalla ancha y título
st.set_page_config(page_title="Memoria: Animales Salvajes", layout="wide")

# Estilo para eliminar márgenes extra de Streamlit
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    iframe { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. El Código del Juego Optimizado
html_salvajes = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        :root {
            --verde-selva: #1b4332;
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
            overflow: hidden; /* Evita el doble scroll */
        }

        header { text-align: center; color: white; margin-bottom: 15px; }
        h1 { margin: 0; font-size: 2.2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
        .brand { font-style: italic; color: #95d5b2; font-size: 1rem; }

        .game-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            width: 95%;
            max-width: 800px;
            perspective: 1000px;
        }

        .card {
            aspect-ratio: 1 / 1; /* Fichas cuadradas para que quepan mejor */
            position: relative;
            cursor: pointer;
            transform-style: preserve-3d;
            transition: transform 0.5s;
        }

        .card.flipped { transform: rotateY(180deg); }

        .card-face {
            position: absolute;
            width: 100%; height: 100%;
            backface-visibility: hidden;
            border-radius: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            border: 3px solid white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }

        .card-front {
            background: linear-gradient(45deg, #2d6a4f, #40916c);
            z-index: 2;
        }
        .card-front::after { content: '🌿'; font-size: 2rem; }

        .card-back {
            background-color: var(--crema);
            transform: rotateY(180deg);
            padding: 5px;
        }

        .card-image { font-size: 4rem; } /* ANIMALES MÁS GRANDES */
        .card-text { font-size: 1.1rem; font-weight: bold; color: var(--verde-selva); text-align: center; word-break: break-word; }

        #final-screen {
            position: fixed; inset: 0;
            background: rgba(0, 0, 0, 0.9);
            display: none; flex-direction: column;
            justify-content: center; align-items: center;
            z-index: 200; color: white; text-align: center;
        }

        .btn-restart {
            padding: 12px 25px; background: var(--naranja);
            color: white; border: none; border-radius: 25px;
            font-size: 1.2rem; font-weight: bold; cursor: pointer; margin-top: 15px;
        }
    </style>
</head>
<body>
    <header>
        <h1>Animales Salvajes</h1>
        <div class="brand">PaoSpanishTeacher</div>
    </header>

    <main class="game-container" id="game-board"></main>

    <div id="final-screen">
        <span style="font-size: 4rem;">🦁🏆</span>
        <h2>¡Felicidades!</h2>
        <p>Has encontrado todos los animales salvajes.</p>
        <button class="btn-restart" onclick="location.reload()">Jugar otra vez</button>
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

# 3. Renderizado final con altura ajustada (850 píxeles suele ser perfecto)
components.html(html_salvajes, height=850, scrolling=False)
