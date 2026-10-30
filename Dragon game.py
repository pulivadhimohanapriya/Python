from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NIGHT RUNNER | Cinematic Game</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    min-height: 100vh;
    background: #05070e;
    color: #fff;
    font-family: Arial, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
    padding: 24px;
}

.page {
    width: 100%;
    max-width: 1100px;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    gap: 15px;
}

.brand {
    font-size: 13px;
    letter-spacing: 5px;
    color: #65e8ff;
    font-weight: bold;
}

.status {
    color: #9da9c0;
    font-size: 11px;
    letter-spacing: 2px;
}

.hero {
    margin-bottom: 20px;
}

.eyebrow {
    color: #ff9d64;
    font-size: 11px;
    letter-spacing: 4px;
    margin-bottom: 12px;
}

h1 {
    font-size: clamp(36px, 7vw, 76px);
    line-height: 0.95;
    letter-spacing: -3px;
    font-weight: 900;
}

h1 span {
    color: #66eaff;
    text-shadow: 0 0 30px #36caff55;
}

.subtitle {
    margin-top: 15px;
    color: #8e9bb5;
    font-size: 14px;
    line-height: 1.7;
}

.game-shell {
    border: 1px solid #25354d;
    background: #080d18;
    padding: 8px;
    border-radius: 14px;
    box-shadow: 0 0 60px #1aa9ff12,
                0 25px 90px #0009;
}

.hud {
    display: flex;
    justify-content: space-between;
    padding: 14px 16px;
    gap: 15px;
}

.hud-label {
    color: #71839e;
    font-size: 10px;
    letter-spacing: 2px;
}

.hud-value {
    margin-top: 6px;
    font-size: 22px;
    font-weight: bold;
    font-variant-numeric: tabular-nums;
}

#score {
    color: #6beaff;
}

#best {
    color: #ffb77c;
}

.game-area {
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    background: #080f22;
}

canvas {
    display: block;
    width: 100%;
    height: auto;
    touch-action: manipulation;
}

.overlay {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 20px;
    background: linear-gradient(90deg, #030714aa, #03071433, #030714aa);
}

.overlay.hidden {
    display: none;
}

.overlay-card {
    max-width: 420px;
}

.overlay h2 {
    font-size: clamp(27px, 5vw, 43px);
    letter-spacing: 3px;
    margin-bottom: 12px;
}

.overlay p {
    color: #a6b4ce;
    font-size: 13px;
    line-height: 1.8;
    margin-bottom: 24px;
}

button {
    background: #67eaff;
    color: #04101c;
    border: none;
    padding: 14px 28px;
    border-radius: 5px;
    font-weight: 900;
    letter-spacing: 2px;
    cursor: pointer;
    transition: 0.2s;
}

button:hover {
    background: #fff;
    box-shadow: 0 0 25px #67eaff66;
    transform: translateY(-2px);
}

.controls {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    padding: 16px 8px 8px;
    color: #8292ac;
    font-size: 11px;
    letter-spacing: 1px;
}

.key {
    color: #dceeff;
    border: 1px solid #34465e;
    border-radius: 4px;
    padding: 5px 8px;
    margin-right: 5px;
}

.footer {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    margin-top: 20px;
    color: #596981;
    font-size: 10px;
    letter-spacing: 2px;
}

@media (max-width: 600px) {
    body { padding: 12px; }
    .brand { letter-spacing: 2px; }
    .status { font-size: 9px; letter-spacing: 1px; }
    .hud-value { font-size: 18px; }
    .controls { line-height: 2.2; }
}
</style>
</head>

<body>
<div class="page">

    <div class="topbar">
        <div class="brand">✦ NIGHT RUNNER</div>
        <div class="status">SYSTEM ONLINE &nbsp; ●</div>
    </div>

    <div class="hero">
        <div class="eyebrow">THE NIGHT IS YOURS</div>
        <h1>RUN BEYOND<br><span>THE DARK.</span></h1>
        <p class="subtitle">
            One runner. Endless night. No second chances.<br>
            Jump into the unknown and beat your highest score.
        </p>
    </div>

    <div class="game-shell">
        <div class="hud">
            <div>
                <div class="hud-label">DISTANCE</div>
                <div class="hud-value" id="score">00000</div>
            </div>
            <div style="text-align:right">
                <div class="hud-label">PERSONAL BEST</div>
                <div class="hud-value" id="best">00000</div>
            </div>
        </div>

        <div class="game-area">
            <canvas id="game" width="1000" height="380"></canvas>

            <div class="overlay" id="overlay">
                <div class="overlay-card">
                    <div class="eyebrow">ENDLESS RUNNER EXPERIENCE</div>
                    <h2 id="overlayTitle">ENTER THE NIGHT</h2>
                    <p id="overlayText">
                        The world is silent. The road is endless.<br>
                        Are you ready to run?
                    </p>
                    <button id="startBtn">START RUNNING →</button>
                </div>
            </div>
        </div>

        <div class="controls">
            <div>
                <span class="key">SPACE</span>
                <span class="key">↑</span> JUMP
                &nbsp;&nbsp;
                <span class="key">↓</span> DUCK
            </div>
            <div><span class="key">R</span> RESTART</div>
        </div>
    </div>

    <div class="footer">
        <span>BUILT FOR THE FEARLESS</span>
        <span>INFINITE ROAD / 001</span>
    </div>

</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const overlay = document.getElementById("overlay");
const startBtn = document.getElementById("startBtn");
const overlayTitle = document.getElementById("overlayTitle");
const overlayText = document.getElementById("overlayText");
const scoreDisplay = document.getElementById("score");
const bestDisplay = document.getElementById("best");

const W = canvas.width;
const H = canvas.height;
const ground = 305;

let running = false;
let gameOver = false;
let score = 0;
let best = Number(localStorage.getItem("nightRunnerBest") || 0);
let speed = 7;
let spawnTimer = 0;
let lastTime = 0;
let elapsed = 0;
let obstacles = [];
let particles = [];
let clouds = [];
let stars = [];
let groundOffset = 0;
let animationFrame = 0;

const player = {
    x: 110,
    y: ground - 58,
    w: 42,
    h: 58,
    vy: 0,
    jumping: false,
    ducking: false
};

bestDisplay.textContent = String(best).padStart(5, "0");

for (let i = 0; i < 85; i++) {
    stars.push({
        x: Math.random() * W,
        y: Math.random() * 220,
        r: Math.random() * 1.6 + 0.3,
        a: Math.random() * 0.7 + 0.2
    });
}

for (let i = 0; i < 12; i++) {
    clouds.push({
        x: Math.random() * W,
        y: 45 + Math.random() * 150,
        w: 70 + Math.random() * 150,
        s: 0.15 + Math.random() * 0.35
    });
}

function roundedRect(x, y, w, h, r, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(x, y, w, h, r);
    ctx.fill();
}

function drawBackground(dt) {
    const sky = ctx.createLinearGradient(0, 0, 0, H);
    sky.addColorStop(0, "#050918");
    sky.addColorStop(0.58, "#111c3b");
    sky.addColorStop(1, "#342044");

    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, W, H);

    // Atmospheric moon
    const moonGlow = ctx.createRadialGradient(
        790, 95, 5, 790, 95, 90
    );
    moonGlow.addColorStop(0, "#c8f8ff35");
    moonGlow.addColorStop(1, "#c8f8ff00");
    ctx.fillStyle = moonGlow;
    ctx.fillRect(680, 0, 220, 200);

    ctx.fillStyle = "#d9f4ff";
    ctx.beginPath();
    ctx.arc(790, 95, 26, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#a5c9e5";
    ctx.beginPath();
    ctx.arc(800, 87, 24, 0, Math.PI * 2);
    ctx.fill();

    // Stars
    for (const s of stars) {
        ctx.globalAlpha = s.a * (0.8 + Math.sin(elapsed * 2 + s.x) * 0.2);
        ctx.fillStyle = "#d5efff";
        ctx.fillRect(s.x, s.y, s.r, s.r);
    }
    ctx.globalAlpha = 1;

    // Moving atmospheric clouds
    for (const c of clouds) {
        c.x -= c.s * dt * 0.06;
        if (c.x + c.w < 0) c.x = W + 30;

        ctx.fillStyle = "#7586b015";
        ctx.beginPath();
        ctx.ellipse(c.x, c.y, c.w / 2, 12, 0, 0, Math.PI * 2);
        ctx.fill();
    }

    // Distant mountains
    ctx.fillStyle = "#141a35";
    ctx.beginPath();
    ctx.moveTo(0, 270);
    for (let x = 0; x <= W; x += 55) {
        ctx.lineTo(x, 225 + Math.sin(x * 0.019) * 30);
    }
    ctx.lineTo(W, ground);
    ctx.lineTo(0, ground);
    ctx.closePath();
    ctx.fill();

    // Near mountains
    ctx.fillStyle = "#0c1227";
    ctx.beginPath();
    ctx.moveTo(0, 285);
    for (let x = 0; x <= W; x += 40) {
        ctx.lineTo(x, 250 + Math.sin(x * 0.025 + 1) * 22);
    }
    ctx.lineTo(W, ground);
    ctx.lineTo(0, ground);
    ctx.closePath();
    ctx.fill();

    // Ground
    ctx.fillStyle = "#080c18";
    ctx.fillRect(0, ground, W, H - ground);

    ctx.shadowBlur = 16;
    ctx.shadowColor = "#60eaff";
    ctx.strokeStyle = "#61dfff";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, ground);
    ctx.lineTo(W, ground);
    ctx.stroke();
    ctx.shadowBlur = 0;

    // Scrolling road marks
    groundOffset = (groundOffset + speed * dt * 0.06) % 70;

    ctx.fillStyle = "#273751";
    for (let x = -70; x < W + 70; x += 70) {
        ctx.fillRect(x - groundOffset, ground + 30, 34, 2);
    }

    // Perspective light pools
    const glow = ctx.createLinearGradient(0, ground, 0, H);
    glow.addColorStop(0, "#55dfff13");
    glow.addColorStop(1, "#55dfff00");
    ctx.fillStyle = glow;
    ctx.fillRect(0, ground, W, H - ground);
}

function drawPlayer() {
    const duck = player.ducking && !player.jumping;
    const h = duck ? 34 : player.h;
    const y = duck ? ground - h : player.y;
    const x = player.x;

    // Neon ground shadow
    ctx.fillStyle = "#63dfff30";
    ctx.beginPath();
    ctx.ellipse(x + 23, ground + 5, 31, 5, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.save();
    ctx.shadowColor = "#66eaff";
    ctx.shadowBlur = 15;
    ctx.fillStyle = "#67eaff";

    if (duck) {
        roundedRect(x + 3, y + 7, 36, 23, 7, "#67eaff");
        roundedRect(x + 23, y, 24, 20, 5, "#8cf2ff");
        ctx.fillStyle = "#07101c";
        ctx.fillRect(x + 39, y + 5, 4, 4);
    } else {
        // Body
        roundedRect(x + 7, y + 20, 29, 27, 6, "#67eaff");

        // Head
        roundedRect(x + 17, y + 1, 29, 25, 6, "#91f4ff");

        // Eye
        ctx.shadowBlur = 0;
        ctx.fillStyle = "#07101c";
        ctx.fillRect(x + 37, y + 8, 4, 4);

        // Running legs
        const step = running && !player.jumping
            ? Math.sin(elapsed * 20) * 9 : 0;

        ctx.strokeStyle = "#67eaff";
        ctx.lineWidth = 7;
        ctx.lineCap = "round";

        ctx.beginPath();
        ctx.moveTo(x + 15, y + 44);
        ctx.lineTo(x + 12 + step, y + 55);
        ctx.moveTo(x + 29, y + 44);
        ctx.lineTo(x + 30 - step, y + 55);
        ctx.stroke();

        // Arm
        ctx.strokeStyle = "#b0f7ff";
        ctx.lineWidth = 5;
        ctx.beginPath();
        ctx.moveTo(x + 14, y + 27);
        ctx.lineTo(x + 5, y + 36 + step * 0.3);
        ctx.stroke();
    }

    ctx.restore();
}

function spawnObstacle() {
    const isFlying = Math.random() < 0.22 && score > 100;

    if (isFlying) {
        obstacles.push({
            x: W + 20,
            y: ground - 75,
            w: 48,
            h: 24,
            type: "drone"
        });
    } else {
        const h = 35 + Math.random() * 28;
        obstacles.push({
            x: W + 20,
            y: ground - h,
            w: 24 + Math.random() * 15,
            h: h,
            type: "crystal"
        });
    }
}

function drawObstacle(o) {
    ctx.save();
    ctx.shadowBlur = 18;

    if (o.type === "drone") {
        ctx.shadowColor = "#ff8269";
        ctx.fillStyle = "#ff8269";
        roundedRect(o.x, o.y + 5, o.w, o.h - 10, 7, "#ff8269");

        ctx.fillStyle = "#fff1c5";
        ctx.fillRect(o.x + 8, o.y + 11, 5, 3);
        ctx.fillRect(o.x + 34, o.y + 11, 5, 3);

        ctx.strokeStyle = "#ff8269";
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(o.x - 6, o.y + 3);
        ctx.lineTo(o.x + o.w + 6, o.y + 3);
        ctx.stroke();
    } else {
        ctx.shadowColor = "#ff7d67";
        ctx.fillStyle = "#ff765f";

        ctx.beginPath();
        ctx.moveTo(o.x, ground);
        ctx.lineTo(o.x + o.w / 2, o.y);
        ctx.lineTo(o.x + o.w, ground);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = "#ffc0a4";
        ctx.beginPath();
        ctx.moveTo(o.x + o.w * 0.43, ground - 8);
        ctx.lineTo(o.x + o.w / 2, o.y + 8);
        ctx.lineTo(o.x + o.w * 0.58, ground - 8);
        ctx.closePath();
        ctx.fill();
    }

    ctx.restore();
}

function addParticles() {
    for (let i = 0; i < 16; i++) {
        particles.push({
            x: player.x + 10,
            y: ground - 5,
            vx: -Math.random() * 4,
            vy: -Math.random() * 4,
            life: 1,
            size: Math.random() * 3 + 1
        });
    }
}

function drawParticles(dt) {
    particles.forEach(p => {
        p.x += p.vx * dt * 0.06;
        p.y += p.vy * dt * 0.06;
        p.life -= dt * 0.0015;

        ctx.globalAlpha = Math.max(0, p.life);
        ctx.fillStyle = "#67eaff";
        ctx.fillRect(p.x, p.y, p.size, p.size);
    });

    ctx.globalAlpha = 1;
    particles = particles.filter(p => p.life > 0);
}

function jump() {
    if (!running || gameOver) return;

    if (!player.jumping) {
        player.vy = -15;
        player.jumping = true;
        player.ducking = false;
        addParticles();
    }
}

function isColliding(o) {
    const duck = player.ducking && !player.jumping;
    const h = duck ? 34 : player.h;
    const y = duck ? ground - h : player.y;

    const px = player.x + 5;
    const py = y + 5;
    const pw = player.w - 10;
    const ph = h - 8;

    const ox = o.x + 4;
    const oy = o.y + 3;
    const ow = o.w - 8;
    const oh = o.h - 5;

    return px < ox + ow &&
           px + pw > ox &&
           py < oy + oh &&
           py + ph > oy;
}

function endGame() {
    running = false;
    gameOver = true;

    addParticles();

    if (score > best) {
        best = score;
        localStorage.setItem("nightRunnerBest", best);
        bestDisplay.textContent = String(best).padStart(5, "0");
    }

    overlayTitle.textContent = "RUN TERMINATED";
    overlayText.innerHTML =
        "Distance achieved: <strong>" + score +
        "</strong><br>The night wins this round. Try again.";
    startBtn.textContent = "RETRY MISSION ↻";
    overlay.classList.remove("hidden");
}

function resetGame() {
    score = 0;
    speed = 7;
    spawnTimer = 0;
    elapsed = 0;
    obstacles = [];
    particles = [];

    player.y = ground - player.h;
    player.vy = 0;
    player.jumping = false;
    player.ducking = false;

    gameOver = false;
    running = true;
    lastTime = performance.now();

    overlay.classList.add("hidden");
    scoreDisplay.textContent = "00000";

    cancelAnimationFrame(animationFrame);
    animationFrame = requestAnimationFrame(loop);
}

function update(dt) {
    elapsed += dt / 1000;

    if (running) {
        score += dt * 0.012 * (speed / 7);
        speed = Math.min(14, 7 + score / 250);

        scoreDisplay.textContent =
            String(Math.floor(score)).padStart(5, "0");

        // Gravity
        player.y += player.vy * dt * 0.06;
        player.vy += 0.72 * dt * 0.06;

        if (player.y >= ground - player.h) {
            player.y = ground - player.h;
            player.vy = 0;
            player.jumping = false;
        }

        // Obstacles
        spawnTimer -= dt;

        if (spawnTimer <= 0) {
            spawnObstacle();
            spawnTimer = 800 + Math.random() * 850;
            spawnTimer *= 7 / speed;
        }

        obstacles.forEach(o => {
            o.x -= speed * dt * 0.06;
        });

        obstacles = obstacles.filter(o => o.x + o.w > -20);

        for (const o of obstacles) {
            if (isColliding(o)) {
                endGame();
                break;
            }
        }
    }

    drawBackground(dt);

    for (const o of obstacles) {
        drawObstacle(o);
    }

    drawParticles(dt);
    drawPlayer();
}

function loop(timestamp) {
    const dt = Math.min(timestamp - lastTime, 40);
    lastTime = timestamp;

    update(dt);

    if (running) {
        animationFrame = requestAnimationFrame(loop);
    }
}

// Keyboard controls
document.addEventListener("keydown", e => {
    if (["Space", "ArrowUp", "ArrowDown"].includes(e.code)) {
        e.preventDefault();
    }

    if (e.repeat) return;

    if (e.code === "Space" || e.code === "ArrowUp") {
        if (!running && !gameOver) resetGame();
        else jump();
    }

    if (e.code === "ArrowDown") {
        if (running && !player.jumping) player.ducking = true;
    }

    if (e.code === "KeyR") {
        resetGame();
    }
});

document.addEventListener("keyup", e => {
    if (e.code === "ArrowDown") {
        player.ducking = false;
    }
});

startBtn.addEventListener("click", resetGame);

canvas.addEventListener("pointerdown", () => {
    if (running) jump();
    else if (!gameOver) resetGame();
});

// Initial animated scene
function attractLoop(timestamp) {
    if (running) return;

    const dt = Math.min(timestamp - (lastTime || timestamp), 40);
    lastTime = timestamp;
    elapsed += dt / 1000;

    drawBackground(dt);

    for (const o of obstacles) drawObstacle(o);
    drawParticles(dt);
    drawPlayer();

    animationFrame = requestAnimationFrame(attractLoop);
}

lastTime = performance.now();
animationFrame = requestAnimationFrame(attractLoop);
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)
