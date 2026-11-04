
from flask import Flask, render_template_string, request, jsonify
import chess
import random

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ROYAL CHESS | Ultimate Chess Arena</title>

<script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script>

<style>
* { box-sizing:border-box; margin:0; padding:0; }

body {
    min-height:100vh;
    background:
      radial-gradient(circle at 50% 0%, #26344c, #0b101a 65%);
    color:#f5f5f5;
    font-family:Arial, sans-serif;
    padding:25px;
}

header {
    text-align:center;
    margin-bottom:25px;
}

header h1 {
    font-size:38px;
    letter-spacing:7px;
    color:#e6bd72;
}

header p {
    color:#aeb9c9;
    margin-top:9px;
    letter-spacing:2px;
    font-size:12px;
}

.container {
    max-width:1100px;
    margin:auto;
    display:grid;
    grid-template-columns:1fr 300px;
    gap:25px;
    align-items:start;
}

.panel {
    background:#151e2b;
    border:1px solid #344156;
    border-radius:15px;
    padding:20px;
    box-shadow:0 15px 40px #0006;
}

.settings {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:12px;
    margin-bottom:18px;
}

label {
    display:block;
    color:#c2ccdb;
    font-size:12px;
    margin-bottom:8px;
}

select, button {
    width:100%;
    padding:12px;
    border-radius:8px;
    border:1px solid #536176;
    background:#202d40;
    color:white;
    outline:none;
}

button {
    cursor:pointer;
    font-weight:bold;
    transition:.2s;
}

button:hover {
    background:#b98d4e;
    color:#111;
}

.start {
    background:#d2a65e;
    color:#10151d;
    border:0;
    font-size:15px;
}

.board-wrap {
    max-width:650px;
    margin:auto;
}

.player {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:12px 5px;
    color:#e8d2a7;
}

.player span {
    font-size:13px;
    color:#b6c1d0;
}

#board {
    display:grid;
    grid-template-columns:repeat(8,1fr);
    width:100%;
    aspect-ratio:1;
    border:7px solid #26364a;
    border-radius:5px;
    overflow:hidden;
}

.square {
    aspect-ratio:1;
    display:flex;
    align-items:center;
    justify-content:center;
    position:relative;
    cursor:pointer;
    user-select:none;
}

.light { background:#e6d4b7; }
.dark { background:#77916f; }

.square.selected {
    background:#d6bc45;
}

.square.target::after {
    content:"";
    width:25%;
    height:25%;
    border-radius:50%;
    background:#182c23a8;
    position:absolute;
}

.square.capture::after {
    content:"";
    position:absolute;
    inset:4px;
    border:5px solid #b93636a9;
    border-radius:50%;
}

.piece {
    font-size:clamp(25px,5vw,55px);
    line-height:1;
    z-index:2;
    cursor:pointer;
    font-family:"DejaVu Sans", "Segoe UI Symbol", serif;
}

.white-piece {
    color:#fffdf4;
    text-shadow:1px 2px 3px #252525, 0 0 2px #222;
}

.black-piece {
    color:#161b23;
    text-shadow:0 1px 2px #fff8;
}

.status {
    text-align:center;
    margin:15px 0;
    padding:13px;
    background:#202d40;
    color:#e9c783;
    border-radius:8px;
    font-weight:bold;
}

.controls {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:10px;
    margin-top:15px;
}

.side h3 {
    color:#e5bd79;
    margin-bottom:15px;
}

.info {
    background:#202d40;
    padding:15px;
    border-radius:9px;
    margin-bottom:15px;
}

.info p {
    color:#aeb9c9;
    font-size:13px;
    line-height:1.8;
}

#history {
    max-height:300px;
    overflow-y:auto;
    color:#d6dce5;
    font-size:13px;
    line-height:2;
}

.history-row {
    display:flex;
    justify-content:space-between;
    border-bottom:1px solid #344156;
    padding:4px;
}

.history-row span:first-child {
    color:#e6bd72;
}

footer {
    text-align:center;
    margin-top:25px;
    font-size:11px;
    color:#78879b;
}

@media(max-width:800px) {
    .container { grid-template-columns:1fr; }
    .side { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
    .side h3 { grid-column:1/-1; }
}

@media(max-width:480px) {
    body { padding:10px; }
    header h1 { font-size:25px; }
    .settings { grid-template-columns:1fr; }
    .side { display:block; }
}
</style>
</head>

<body>

<header>
    <h1>♛ ROYAL CHESS</h1>
    <p>STRATEGY • INTELLIGENCE • VICTORY</p>
</header>

<div class="container">

<div class="panel">

    <div class="settings">

        <div>
            <label>GAME MODE</label>
            <select id="mode">
                <option value="pvp">Player vs Player</option>
                <option value="pvc">Player vs Computer</option>
            </select>
        </div>

        <div>
            <label>YOUR COLOR</label>
            <select id="color">
                <option value="w">White</option>
                <option value="b">Black</option>
            </select>
        </div>

        <div>
            <label>AI DIFFICULTY</label>
            <select id="difficulty">
                <option value="1">Easy</option>
                <option value="2" selected>Medium</option>
                <option value="3">Hard</option>
            </select>
        </div>

    </div>

    <button class="start" onclick="newGame()">START NEW GAME</button>

    <div class="board-wrap">

        <div class="player">
            <strong id="topName">BLACK</strong>
            <span id="topInfo">Opponent</span>
        </div>

        <div id="board"></div>

        <div class="player">
            <strong id="bottomName">WHITE</strong>
            <span id="bottomInfo">Player</span>
        </div>

    </div>

    <div class="status" id="status">Choose your game mode and start!</div>

    <div class="controls">
        <button onclick="undoMove()">↶ Undo</button>
        <button onclick="newGame()">⟳ Restart</button>
        <button onclick="flipBoard()">⇅ Flip Board</button>
    </div>

</div>

<div class="panel side">

    <h3>♜ GAME INFORMATION</h3>

    <div class="info">
        <p>Game Mode: <strong id="modeInfo">Player vs Player</strong></p>
        <p>Selected Side: <strong id="sideInfo">White</strong></p>
        <p>Difficulty: <strong id="levelInfo">Medium</strong></p>
        <p>Moves Played: <strong id="moveCount">0</strong></p>
    </div>

    <div class="info">
        <h3>MOVE HISTORY</h3>
        <div id="history">No moves yet.</div>
    </div>

    <div class="info">
        <h3>HOW TO PLAY</h3>
        <p>
            1. Select your game mode.<br>
            2. Choose your color.<br>
            3. Click a chess piece.<br>
            4. Select a highlighted square.<br>
            5. Capture the opponent's king by checkmating it!
        </p>
    </div>

</div>

</div>

<footer>ROYAL CHESS ARENA | BUILT WITH PYTHON & FLASK</footer>

<script>
let game = new Chess();
let selected = null;
let possible = [];
let mode = "pvp";
let humanColor = "w";
let flipped = false;
let aiThinking = false;
let started = false;

const pieces = {
    wk:"♔", wq:"♕", wr:"♖", wb:"♗", wn:"♘", wp:"♙",
    bk:"♚", bq:"♛", br:"♜", bb:"♝", bn:"♞", bp:"♟"
};

function newGame() {
    game = new Chess();
    selected = null;
    possible = [];
    aiThinking = false;
    started = true;

    mode = document.getElementById("mode").value;
    humanColor = document.getElementById("color").value;
    flipped = mode === "pvc" && humanColor === "b";

    document.getElementById("modeInfo").innerText =
        mode === "pvp" ? "Player vs Player" : "Player vs Computer";

    document.getElementById("sideInfo").innerText =
        humanColor === "w" ? "White" : "Black";

    const level = document.getElementById("difficulty").value;
    document.getElementById("levelInfo").innerText =
        ["", "Easy", "Medium", "Hard"][level];

    document.getElementById("topName").innerText =
        mode === "pvc" ?
        (humanColor === "w" ? "BLACK · COMPUTER" : "WHITE · COMPUTER") :
        (flipped ? "WHITE" : "BLACK");

    document.getElementById("bottomName").innerText =
        mode === "pvc" ?
        (humanColor === "w" ? "WHITE · YOU" : "BLACK · YOU") :
        (flipped ? "BLACK" : "WHITE");

    render();
    updateStatus();

    if (mode === "pvc" && game.turn() !== humanColor) {
        computerMove();
    }
}

function render() {
    const board = document.getElementById("board");
    board.innerHTML = "";

    let positions = [];

    for(let r=0;r<8;r++) {
        for(let c=0;c<8;c++) {
            let row = flipped ? 7-r : r;
            let col = flipped ? 7-c : c;
            positions.push({
                square: String.fromCharCode(97+col)+(8-row),
                row: row,
                col: col
            });
        }
    }

    positions.forEach(pos => {
        const square = document.createElement("div");
        square.className =
            "square " + ((pos.row+pos.col)%2===0 ? "light":"dark");

        if(selected === pos.square) square.classList.add("selected");

        const move = possible.find(m => m.to === pos.square);

        if(move) {
            square.classList.add(
                game.get(pos.square) ? "capture" : "target"
            );
        }

        const piece = game.get(pos.square);

        if(piece) {
            const span = document.createElement("span");
            span.className = "piece " +
                (piece.color==="w" ? "white-piece":"black-piece");
            span.textContent = pieces[piece.color+piece.type];
            square.appendChild(span);
        }

        square.onclick = () => squareClick(pos.square);
        board.appendChild(square);
    });

    document.getElementById("moveCount").innerText =
        game.history().length;
    updateHistory();
}

function squareClick(sq) {
    if(!started || game.game_over() || aiThinking) return;

    if(mode === "pvc" && game.turn() !== humanColor) return;

    const piece = game.get(sq);

    if(selected) {
        let move = game.move({
            from:selected,
            to:sq,
            promotion:"q"
        });

        if(move) {
            selected = null;
            possible = [];
            render();
            updateStatus();

            if(mode === "pvc" && !game.game_over()) {
                computerMove();
            }
            return;
        }
    }

    if(piece && piece.color === game.turn()) {
        selected = sq;
        possible = game.moves({
            square:sq,
            verbose:true
        });
    } else {
        selected = null;
        possible = [];
    }

    render();
}

async function computerMove() {
    if(game.game_over() || aiThinking) return;

    aiThinking = true;
    selected = null;
    possible = [];

    document.getElementById("status").innerText =
        "🤖 Computer is thinking...";

    render();

    try {
        const response = await fetch("/ai_move", {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({
                fen:game.fen(),
                difficulty:document.getElementById("difficulty").value
            })
        });

        const data = await response.json();

        if(!response.ok) throw new Error(data.error || "AI error");

        if(data.move) {
            const move = game.move({
                from:data.move.substring(0,2),
                to:data.move.substring(2,4),
                promotion:data.move.length===5 ?
                    data.move.substring(4) : "q"
            });

            if(!move) throw new Error("Computer returned an invalid move.");
        }

    } catch(error) {
        document.getElementById("status").innerText =
            "Computer error: " + error.message;
    }

    aiThinking = false;
    render();
    updateStatus();
}

function updateStatus() {
    const status = document.getElementById("status");

    if(game.in_checkmate()) {
        status.innerText =
            "🏆 CHECKMATE! " +
            (game.turn()==="w" ? "BLACK" : "WHITE") + " WINS!";
    }
    else if(game.in_stalemate()) {
        status.innerText = "DRAW! STALEMATE.";
    }
    else if(game.in_draw()) {
        status.innerText = "GAME DRAWN!";
    }
    else if(game.in_check()) {
        status.innerText =
            (game.turn()==="w" ? "WHITE" : "BLACK") + " IS IN CHECK!";
    }
    else {
        status.innerText =
            (game.turn()==="w" ? "WHITE" : "BLACK") + " TO MOVE";
    }
}

function updateHistory() {
    const history = game.history();
    const box = document.getElementById("history");

    if(!history.length) {
        box.innerHTML = "No moves yet.";
        return;
    }

    box.innerHTML = "";

    for(let i=0;i<history.length;i+=2) {
        const row = document.createElement("div");
        row.className = "history-row";

        const number = document.createElement("span");
        number.textContent = (Math.floor(i/2)+1) + ".";

        const white = document.createElement("span");
        white.textContent = history[i];

        const black = document.createElement("span");
        black.textContent = history[i+1] || "";

        row.append(number,white,black);
        box.appendChild(row);
    }
}

function undoMove() {
    if(!started || aiThinking || game.history().length===0) return;

    game.undo();

    if(mode==="pvc" && game.turn() !== humanColor &&
       game.history().length>0) {
        game.undo();
    }

    selected = null;
    possible = [];
    render();
    updateStatus();
}

function flipBoard() {
    flipped = !flipped;
    render();
}

newGame();
</script>

</body>
</html>
"""


# ---------------- AI ENGINE ----------------

VALUES = {
    chess.PAWN:100,
    chess.KNIGHT:320,
    chess.BISHOP:330,
    chess.ROOK:500,
    chess.QUEEN:900,
    chess.KING:20000
}


def evaluate(board):
    if board.is_checkmate():
        return -100000 if board.turn else 100000

    if board.is_game_over():
        return 0

    score = 0

    for piece_type, value in VALUES.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value

    score += (len(list(board.legal_moves)) * 2) * (
        1 if board.turn == chess.WHITE else -1
    )

    return score


def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    moves = list(board.legal_moves)
    random.shuffle(moves)

    moves.sort(
        key=lambda m: board.is_capture(m),
        reverse=True
    )

    if maximizing:
        best = -float("inf")

        for move in moves:
            board.push(move)
            score = minimax(board, depth-1, alpha, beta, False)
            board.pop()

            best = max(best, score)
            alpha = max(alpha, best)

            if beta <= alpha:
                break

        return best

    else:
        best = float("inf")

        for move in moves:
            board.push(move)
            score = minimax(board, depth-1, alpha, beta, True)
            board.pop()

            best = min(best, score)
            beta = min(beta, best)

            if beta <= alpha:
                break

        return best


def get_best_move(board, depth):
    moves = list(board.legal_moves)

    if not moves:
        return None

    random.shuffle(moves)

    best_move = None

    if board.turn == chess.WHITE:
        best_score = -float("inf")

        for move in moves:
            board.push(move)
            score = minimax(
                board, depth-1,
                -float("inf"), float("inf"), False
            )
            board.pop()

            if score > best_score:
                best_score = score
                best_move = move

    else:
        best_score = float("inf")

        for move in moves:
            board.push(move)
            score = minimax(
                board, depth-1,
                -float("inf"), float("inf"), True
            )
            board.pop()

            if score < best_score:
                best_score = score
                best_move = move

    return best_move


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/ai_move", methods=["POST"])
def ai_move():
    try:
        data = request.get_json()
        board = chess.Board(data["fen"])

        if not board.is_valid():
            return jsonify({"error":"Invalid chess position"}), 400

        if board.is_game_over():
            return jsonify({"move":None})

        difficulty = int(data.get("difficulty", 2))
        depth = max(1, min(difficulty, 3))

        move = get_best_move(board, depth)

        if move is None:
            return jsonify({"move":None})

        return jsonify({"move":move.uci()})

    except Exception as error:
        return jsonify({"error":str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True)
