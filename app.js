// Chess Opening Explorer - Main Application

// Initialize chess game
const game = new Chess();
let board = null;
let stockfish = null;
let currentAnalysis = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeBoard();
    initializeStockfish();
    setupEventListeners();
    updateDisplay();
    queryLichessAPI();
});

// Initialize the chess board
function initializeBoard() {
    const config = {
        draggable: true,
        position: 'start',
        onDragStart: onDragStart,
        onDrop: onDrop,
        onSnapEnd: onSnapEnd
    };
    
    board = Chessboard('chessboard', config);
    
    // Adjust board size
    $(window).resize(board.resize);
}

// Board drag handlers
function onDragStart(source, piece, position, orientation) {
    // Don't allow moves if game is over
    if (game.game_over()) return false;
    
    // Only allow moves for the side to move
    if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
        (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
        return false;
    }
}

function onDrop(source, target) {
    // Try to make the move
    const move = game.move({
        from: source,
        to: target,
        promotion: 'q' // Always promote to queen for simplicity
    });
    
    // Illegal move
    if (move === null) return 'snapback';
    
    // Update display and fetch new data
    updateDisplay();
    queryLichessAPI();
}

function onSnapEnd() {
    board.position(game.fen());
}

// Initialize Stockfish engine
function initializeStockfish() {
    try {
        if (typeof STOCKFISH === 'function') {
            stockfish = STOCKFISH();
            
            stockfish.onmessage = function(event) {
                handleStockfishMessage(event.data);
            };
            
            // Initialize the engine
            stockfish.postMessage('uci');
            stockfish.postMessage('isready');
            
            document.getElementById('stockfish-loading').style.display = 'none';
            document.getElementById('stockfish-content').style.display = 'block';
        } else {
            throw new Error('Stockfish not loaded');
        }
    } catch (error) {
        console.error('Error initializing Stockfish:', error);
        document.getElementById('stockfish-loading').style.display = 'none';
        document.getElementById('stockfish-error').textContent = 
            'Failed to initialize Stockfish engine. Using CDN version may have issues.';
        document.getElementById('stockfish-error').style.display = 'block';
    }
}

// Handle Stockfish messages
let bestMoves = [];
let currentEval = null;

function handleStockfishMessage(message) {
    console.log('Stockfish:', message);
    
    if (message.includes('info depth')) {
        // Parse analysis info
        const depthMatch = message.match(/depth (\d+)/);
        const scoreMatch = message.match(/score cp (-?\d+)/);
        const mateMatch = message.match(/score mate (-?\d+)/);
        const pvMatch = message.match(/pv (.+)$/);
        
        if (depthMatch && (scoreMatch || mateMatch) && pvMatch) {
            const depth = parseInt(depthMatch[1]);
            const pv = pvMatch[1].split(' ');
            
            let evaluation;
            if (mateMatch) {
                const mateIn = parseInt(mateMatch[1]);
                evaluation = `M${mateIn}`;
            } else {
                const centipawns = parseInt(scoreMatch[1]);
                evaluation = (centipawns / 100).toFixed(2);
            }
            
            currentEval = evaluation;
            
            // Update best moves list
            const moveSequence = convertUCIMovesToSAN(pv.slice(0, 5));
            
            if (depth >= 10) {
                const existingIndex = bestMoves.findIndex(m => m.move === moveSequence);
                if (existingIndex >= 0) {
                    bestMoves[existingIndex] = { move: moveSequence, eval: evaluation, depth: depth };
                } else if (bestMoves.length < 5) {
                    bestMoves.push({ move: moveSequence, eval: evaluation, depth: depth });
                }
                
                displayBestMoves();
                displayEvaluation();
            }
        }
    }
}

// Convert UCI moves to SAN notation
function convertUCIMovesToSAN(uciMoves) {
    const tempGame = new Chess(game.fen());
    const sanMoves = [];
    
    for (const uciMove of uciMoves) {
        if (!uciMove || uciMove.length < 4) break;
        
        const from = uciMove.substring(0, 2);
        const to = uciMove.substring(2, 4);
        const promotion = uciMove.length > 4 ? uciMove[4] : undefined;
        
        const move = tempGame.move({
            from: from,
            to: to,
            promotion: promotion
        });
        
        if (move) {
            sanMoves.push(move.san);
        } else {
            break;
        }
    }
    
    return sanMoves.join(' ');
}

// Analyze current position with Stockfish
function analyzePosition() {
    if (!stockfish) {
        alert('Stockfish engine not available');
        return;
    }
    
    const depth = parseInt(document.getElementById('depth-input').value) || 15;
    
    // Reset analysis
    bestMoves = [];
    currentEval = null;
    document.getElementById('best-moves-list').innerHTML = 
        '<div class="loading">Analyzing...</div>';
    
    // Send position to Stockfish
    stockfish.postMessage('stop');
    stockfish.postMessage('ucinewgame');
    stockfish.postMessage('position fen ' + game.fen());
    stockfish.postMessage('go depth ' + depth);
}

// Display best moves
function displayBestMoves() {
    const container = document.getElementById('best-moves-list');
    
    if (bestMoves.length === 0) {
        container.innerHTML = '<div class="loading">No analysis yet. Click "Analyze Position".</div>';
        return;
    }
    
    let html = '';
    bestMoves.forEach((item, index) => {
        const evalClass = getEvalClass(item.eval);
        html += `
            <div class="best-move-item">
                <div class="best-move-header">
                    <span class="move-sequence">${index + 1}. ${item.move}</span>
                    <span class="move-eval ${evalClass}">${item.eval}</span>
                </div>
                <div class="move-depth">Depth: ${item.depth}</div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Display evaluation bar
function displayEvaluation() {
    const container = document.getElementById('evaluation-display');
    
    if (!currentEval) {
        container.innerHTML = '<div class="loading">No evaluation available</div>';
        return;
    }
    
    let evalText = currentEval;
    let evalPercent = 50;
    
    if (typeof currentEval === 'string' && currentEval.startsWith('M')) {
        // Mate score
        const mateIn = parseInt(currentEval.substring(1));
        evalPercent = mateIn > 0 ? 100 : 0;
        evalText = currentEval;
    } else {
        // Centipawn score
        const evalNum = parseFloat(currentEval);
        evalPercent = 50 + (evalNum * 5);
        evalPercent = Math.max(0, Math.min(100, evalPercent));
    }
    
    container.innerHTML = `
        <div class="eval-text">${evalText}</div>
        <div class="eval-bar-container">
            <div class="eval-bar-white" style="width: ${evalPercent}%"></div>
        </div>
        <div style="margin-top: 10px; color: #666;">
            White advantage: ${evalPercent.toFixed(0)}%
        </div>
    `;
}

// Get evaluation class for styling
function getEvalClass(evaluation) {
    if (typeof evaluation === 'string' && evaluation.startsWith('M')) {
        const mateIn = parseInt(evaluation.substring(1));
        return mateIn > 0 ? 'eval-positive' : 'eval-negative';
    }
    
    const evalNum = parseFloat(evaluation);
    if (evalNum > 1) return 'eval-positive';
    if (evalNum < -1) return 'eval-negative';
    return 'eval-neutral';
}

// Query Lichess Opening Explorer API
async function queryLichessAPI() {
    const fen = game.fen();
    
    // Show loading state
    document.getElementById('lichess-loading').style.display = 'block';
    document.getElementById('lichess-content').style.display = 'none';
    document.getElementById('lichess-error').style.display = 'none';
    
    try {
        // Use the moves sequence instead of FEN for better results
        const moves = game.history({ verbose: true })
            .map(m => m.from + m.to + (m.promotion || ''))
            .join(',');
        
        const url = moves 
            ? `https://explorer.lichess.ovh/lichess?play=${moves}&moves=12`
            : 'https://explorer.lichess.ovh/lichess?moves=12';
        
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`API returned ${response.status}`);
        }
        
        const data = await response.json();
        displayLichessData(data);
        
    } catch (error) {
        console.error('Error querying Lichess API:', error);
        document.getElementById('lichess-loading').style.display = 'none';
        document.getElementById('lichess-error').textContent = 
            'Failed to fetch data from Lichess API: ' + error.message;
        document.getElementById('lichess-error').style.display = 'block';
    }
}

// Display Lichess data
function displayLichessData(data) {
    document.getElementById('lichess-loading').style.display = 'none';
    document.getElementById('lichess-content').style.display = 'block';
    
    // Display position statistics
    const totalGames = data.white + data.draws + data.black;
    const whitePercent = totalGames > 0 ? ((data.white / totalGames) * 100).toFixed(1) : 0;
    const drawPercent = totalGames > 0 ? ((data.draws / totalGames) * 100).toFixed(1) : 0;
    const blackPercent = totalGames > 0 ? ((data.black / totalGames) * 100).toFixed(1) : 0;
    
    document.getElementById('position-stats').innerHTML = `
        <div class="stat-item">
            <div class="stat-label">White Wins</div>
            <div class="stat-value">${data.white.toLocaleString()}</div>
            <div class="stat-percentage">${whitePercent}%</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Draws</div>
            <div class="stat-value">${data.draws.toLocaleString()}</div>
            <div class="stat-percentage">${drawPercent}%</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Black Wins</div>
            <div class="stat-value">${data.black.toLocaleString()}</div>
            <div class="stat-percentage">${blackPercent}%</div>
        </div>
    `;
    
    // Display popular moves
    if (data.moves && data.moves.length > 0) {
        let movesHTML = '';
        
        data.moves.forEach(move => {
            const moveTotal = move.white + move.draws + move.black;
            const whiteP = ((move.white / moveTotal) * 100).toFixed(0);
            const drawP = ((move.draws / moveTotal) * 100).toFixed(0);
            const blackP = ((move.black / moveTotal) * 100).toFixed(0);
            
            movesHTML += `
                <div class="move-item" onclick="makeMove('${move.san}')">
                    <div>
                        <div class="move-notation">${move.san}</div>
                        <div class="move-bar">
                            <div class="move-bar-fill">
                                <div class="bar-white" style="width: ${whiteP}%"></div>
                                <div class="bar-draw" style="width: ${drawP}%"></div>
                                <div class="bar-black" style="width: ${blackP}%"></div>
                            </div>
                        </div>
                    </div>
                    <div class="move-stats">
                        <div class="move-stat">
                            <span class="move-stat-value">${moveTotal.toLocaleString()}</span>
                            <span class="move-stat-label">games</span>
                        </div>
                        <div class="move-stat">
                            <span class="move-stat-value">${whiteP}%</span>
                            <span class="move-stat-label">white</span>
                        </div>
                        <div class="move-stat">
                            <span class="move-stat-value">${drawP}%</span>
                            <span class="move-stat-label">draws</span>
                        </div>
                        <div class="move-stat">
                            <span class="move-stat-value">${blackP}%</span>
                            <span class="move-stat-label">black</span>
                        </div>
                    </div>
                </div>
            `;
        });
        
        document.getElementById('popular-moves-list').innerHTML = movesHTML;
    } else {
        document.getElementById('popular-moves-list').innerHTML = 
            '<div class="loading">No popular moves available for this position.</div>';
    }
    
    // Display opening name
    if (data.opening) {
        document.getElementById('opening-name').textContent = 
            `${data.opening.eco || ''} ${data.opening.name || 'Unknown Opening'}`.trim();
    } else {
        document.getElementById('opening-name').textContent = 'Position not in opening database';
    }
}

// Make a move on the board
function makeMove(san) {
    try {
        const move = game.move(san);
        if (move) {
            board.position(game.fen());
            updateDisplay();
            queryLichessAPI();
        }
    } catch (error) {
        console.error('Invalid move:', error);
    }
}

// Update display (PGN and FEN)
function updateDisplay() {
    const pgn = game.pgn({ max_width: 5, newline_char: ' ' });
    document.getElementById('pgn-display').textContent = pgn || 'No moves yet';
    document.getElementById('fen-display').textContent = game.fen();
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('resetBtn').addEventListener('click', function() {
        game.reset();
        board.position('start');
        updateDisplay();
        queryLichessAPI();
        bestMoves = [];
        currentEval = null;
        document.getElementById('best-moves-list').innerHTML = 
            '<div class="loading">No analysis yet. Click "Analyze Position".</div>';
        document.getElementById('evaluation-display').innerHTML = 
            '<div class="loading">No evaluation available</div>';
    });
    
    document.getElementById('flipBtn').addEventListener('click', function() {
        board.flip();
    });
    
    document.getElementById('undoBtn').addEventListener('click', function() {
        game.undo();
        board.position(game.fen());
        updateDisplay();
        queryLichessAPI();
    });
    
    document.getElementById('analyzeBtn').addEventListener('click', analyzePosition);
}
