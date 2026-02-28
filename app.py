import streamlit as st
import streamlit.components.v1 as components

# 1. Configuración de pantalla
st.set_page_config(page_title="Memoria - Viajes", layout="wide")

# Estilo para limpiar márgenes de Streamlit
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    iframe { border-radius: 20px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. El Código del Juego (Imagen + Palabra Juntas)
html_viajes_duo = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&family=Quicksand:wght@500;700&family=Dancing+Script:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #00b4d8;
            --secondary: #ff9e00;
            --accent: #e63946;
            --text-dark: #023e8a;
            --card-back: #48cae4;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }

        body {
            font-family: 'Quicksand', sans-serif;
            min-height: 100vh;
            background: linear-gradient(rgba(202, 240, 248, 0.4), rgba(202, 240, 248, 0.4)), 
                        url('https://img.freepik.com/vector-gratis/fondo-dibujos-animados-aeropuerto-terminal-salon-salidas-interior-puerta-embarque_107791-4562.jpg');
            background-size: cover;
            background-attachment: fixed;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 10px;
        }

        header { text-align: center; margin: 15px 0; z-index: 10; }
        h1 { font-family: 'Fredoka', sans-serif; font-size: 2.8rem; color: var(--text-dark); text-shadow: 3px 3px 0px white; }
        .brand-name { font-family: 'Dancing Script', cursive; font-size: 1.6rem; color: var(--accent); margin-top: -5px; }

        .game-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 12px;
            width: 100%;
            max-width: 850px;
            perspective: 1000px;
        }

        .card {
            aspect-ratio: 1/1.1;
            cursor: pointer;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .card:hover:not(.flipped) { transform: translateY(-5px) scale(1.03); }
        .card.flipped { transform: rotateY(180deg); }

        .card-face {
            position: absolute;
            width: 100%; height: 100%;
            backface-visibility: hidden;
            border-radius: 15px;
            border: 5px solid white;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .card-back {
            background: var(--card-back);
            background-image: radial-gradient(circle, rgba(255,255,255,0.3) 20%, transparent 20%);
            background-size: 15px 15px;
        }

        .card-back::after { content: "🧳"; font-size: 3rem; filter: drop-shadow(2px 2px 0px rgba(0,0,0,0.1)); }

        .card-front { background: white; transform: rotateY(180deg); padding: 8px; }

        .card-image { font-size: 3.5rem; margin-bottom: 5px; }
        .card-word { 
            font-family: 'Fredoka', sans-serif; 
            font-size: 1.1rem; 
            color: var(--text-dark); 
            font-weight: 600; 
            text-transform: uppercase;
            text-align: center;
        }

        #feedback-msg {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0);
            font-family: 'Fredoka', sans-serif; font-size: 4rem; color: white;
            text-shadow: 0 0 15px rgba(0,0,0,0.2), 4px 4px 0 var(--secondary); 
            z-index: 100; pointer-events: none;
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        #feedback-msg.show { transform: translate(-50%, -50%) scale(1); animation: popOut 1s forwards 0.5s; }
        @keyframes popOut { to { opacity: 0; transform: translate(-50%, -60%) scale(0.8); } }

        .watermark {
            position: fixed; bottom: 10px; right: 20px;
            font-size: 1rem; color: rgba(2, 62, 138, 0.2);
            font-family: 'Dancing Script', cursive; font-weight: bold;
        }

        #victory-screen {
            position: fixed; inset: 0; background: rgba(0, 180, 216, 0.96);
            display: none; flex-direction: column; justify-content: center;
            align-items: center; z-index: 2000; text-align: center; color: white; padding: 20px;
        }

        .profesor { font-size: 8rem; animation: teacherFloat 3s infinite ease-in-out; }
        @keyframes teacherFloat { 0%, 100% { transform: translateY(0) rotate(0); } 50% { transform: translateY(-20px) rotate(5deg); } }

        .btn-restart {
            background: var(--secondary); color: white; border: none;
            padding: 18px 45px; font-size: 2rem; font-family: 'Fredoka', sans-serif;
            border-radius: 50px; cursor: pointer; box-shadow: 0 8px 0 #cc7e00; margin-top: 25px;
        }

        .btn-restart:active { transform: translateY(4px); box-shadow: 0 4px 0 #cc7e00; }

        .balloon { position: absolute; bottom: -100px; animation: floatUp 5s linear forwards; z-index: 2001; font-size: 3rem; }
        @keyframes floatUp { to { transform: translateY(-120vh) translateX(40px); } }
    </style>
</head>
<body>

    <header>
        <h1>Memoria - Viajes</h1>
        <div class="brand-name">PaoSpanishTeacher</div>
    </header>

    <div class="game-container" id="board"></div>
    <div id="feedback-msg">¡Excelente!</div>
    <div class="watermark">PaoSpanishTeacher</div>

    <div id="victory-screen">
        <div class="profesor">👨‍🏫</div>
        <h2 style="font-size: 2.5rem; margin-bottom: 10px;">¡Felicidades!</h2>
        <p style="font-size: 1.5rem;">Has completado la memoria de viajes.</p>
        <p style="margin-top: 20px; font-weight: bold; color: #ff9e00;">Juego creado por PaoSpanishTeacher</p>
        <button class="btn-restart" onclick="location.reload()">Jugar otra vez</button>
    </div>

    <audio id="sfx-hit" src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3"></audio>
    <audio id="sfx-error" src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3"></audio>
    <audio id="sfx-win" src="https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3" loop></audio>

    <script>
        const GAME_DATA = [
            { w: "Aeropuerto", i: "🏢" }, { w: "Avión", i: "✈️" },
            { w: "Maleta", i: "🧳" }, { w: "Pasaporte", i: "🛂" },
            { w: "Hotel", i: "🏨" }, { w: "Mapa", i: "🗺️" },
            { w: "Playa", i: "🏖️" }, { w: "Tren", i: "🚆" },
            { w: "Autobús", i: "🚌" }, { w: "Turista", i: "📸" }
        ];

        let flipped = [];
        let matched = 0;
        let lock = false;

        function init() {
            const board = document.getElementById('board');
            let deck = [];
            // Creamos 2 fichas idénticas por cada elemento (ambas con palabra e imagen)
            GAME_DATA.forEach(item => {
                deck.push({ ...item });
                deck.push({ ...item });
            });
            deck.sort(() => Math.random() - 0.5);

            deck.forEach(data => {
                const card = document.createElement('div');
                card.className = 'card';
                card.dataset.id = data.w;
                card.innerHTML = `
                    <div class="card-face card-back"></div>
                    <div class="card-face card-front">
                        <div class="card-image">${data.i}</div>
                        <div class="card-word">${data.w}</div>
                    </div>`;
                card.onclick = () => flip(card);
                board.appendChild(card);
            });
        }

        function flip(card) {
            if (lock || card.classList.contains('flipped')) return;
            
            card.classList.add('flipped');
            flipped.push(card);
            
            if (flipped.length === 2) check();
        }

        function check() {
            lock = true;
            const [c1, c2] = flipped;
            if (c1.dataset.id === c2.dataset.id) {
                matched++;
                document.getElementById('sfx-hit').play().catch(()=>{});
                document.getElementById('feedback-msg').classList.add('show');
                setTimeout(() => document.getElementById('feedback-msg').classList.remove('show'), 1000);
                flipped = [];
                lock = false;
                if (matched === GAME_DATA.length) win();
            } else {
                document.getElementById('sfx-error').play().catch(()=>{});
                setTimeout(() => {
                    c1.classList.remove('flipped');
                    c2.classList.remove('flipped');
                    flipped = [];
                    lock = false;
                }, 1200);
            }
        }

        function win() {
            document.getElementById('sfx-win').play().catch(()=>{});
            document.getElementById('victory-screen').style.display = 'flex';
            confetti({ particleCount: 200, spread: 80, origin: { y: 0.6 } });
            
            for(let i=0; i<15; i++) {
                setTimeout(() => {
                    const b = document.createElement('div');
                    b.className = 'balloon';
                    b.innerHTML = ['🎈','🌈','✈️','🌍'][Math.floor(Math.random()*4)];
                    b.style.left = Math.random() * 90 + 'vw';
                    document.body.appendChild(b);
                    setTimeout(() => b.remove(), 5000);
                }, i * 350);
            }
            
            if ('speechSynthesis' in window) {
                const msg = new SpeechSynthesisUtterance("Te felicito, sigue avanzando en tu español.");
                msg.lang = 'es-ES';
                window.speechSynthesis.speak(msg);
            }
        }

        init();
    </script>
</body>
</html>
"""

# 3. Renderizado final
components.html(html_viajes_duo, height=920, scrolling=False)
