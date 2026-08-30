<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Game Doi Khang Pixel</title>
    <style>
        * { box-sizing: border-box; touch-action: manipulation; user-select: none; }
        body { margin: 0; background: #111; color: #fff; font-family: sans-serif; text-align: center; }
        .game-container { position: relative; width: 100%; max-width: 600px; margin: 0 auto; }
        
        /* Thanh Máu */
        .ui-bar { display: flex; justify-content: space-between; padding: 10px; background: #222; }
        .health-box { width: 45%; background: #444; height: 20px; border: 2px solid #fff; border-radius: 5px; overflow: hidden; }
        .health-fill { height: 100%; width: 100%; background: #2ecc71; transition: width 0.1s; }
        #p2Health { background: #e74c3c; float: right; }

        canvas { background: #1a1a2e; border-bottom: 4px solid #4e4e50; display: block; width: 100%; height: auto; }

        /* Phím điều khiển cảm ứng cho điện thoại */
        .controls { display: flex; justify-content: space-between; padding: 15px 10px; max-width: 600px; margin: 0 auto; }
        .btn-group { display: grid; grid-template-columns: repeat(3, 50px); grid-gap: 8px; }
        .btn { background: #333; color: #fff; border: 2px solid #555; border-radius: 10px; font-weight: bold; font-size: 16px; height: 50px; width: 50px; display: flex; align-items: center; justify-content: center; }
        .btn:active { background: #666; }
        .btn-punch { background: #e67e22; }
        .btn-kick { background: #e74c3c; }
        #restartBtn { display: none; margin: 10px auto; padding: 10px 20px; background: #27ae60; color: white; border: none; font-size: 16px; font-weight: bold; border-radius: 5px; }
    </style>
</head>
<body>

    <div class="game-container">
        <div class="ui-bar">
            <div>Player 1<div class="health-box"><div id="p1Health" class="health-fill"></div></div></div>
            <div>AI / Player 2<div class="health-box"><div id="p2Health" class="health-fill"></div></div></div>
        </div>
        <canvas id="gameCanvas" width="600" height="300"></canvas>
        <button id="restartBtn" onclick="initGame()">🎮 Chơi Lại</button>
    </div>

    <!-- Phím Bấm Điện Thoại -->
    <div class="controls">
        <div class="btn-group">
            <button class="btn" onclick="moveP1(-1)">◄</button>
            <button class="btn" onclick="jumpP1()">▲</button>
            <button class="btn" onclick="moveP1(1)">►</button>
        </div>
        <div class="btn-group" style="grid-template-columns: repeat(2, 55px);">
            <button class="btn btn-punch" onclick="attackP1('punch')">Đấm</button>
            <button class="btn btn-kick" onclick="attackP1('kick')">Đá</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let p1, p2, gameInterval;

        function initGame() {
            document.getElementById("restartBtn").style.display = "none";
            p1 = { x: 80, y: 200, w: 30, h: 60, vx: 0, vy: 0, hp: 100, color: '#3498db', attacking: false };
            p2 = { x: 480, y: 200, w: 30, h: 60, vx: 0, vy: 0, hp: 100, color: '#e74c3c', attacking: false };
            updateUI();
            if (gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(update, 1000 / 60);
        }

        function moveP1(dir) { p1.vx = dir * 4; setTimeout(() => p1.vx = 0, 150); }
        function jumpP1() { if (p1.y >= 200) p1.vy = -12; }

        function attackP1(type) {
            if (p1.attacking) return;
            p1.attacking = true;
            
            // Tầm đánh
            let range = type === 'punch' ? 40 : 55;
            let damage = type === 'punch' ? 8 : 12;

            if (Math.abs((p1.x + p1.w/2) - (p2.x + p2.w/2)) < range && Math.abs(p1.y - p2.y) < 40) {
                p2.hp = Math.max(0, p2.hp - damage);
                p2.x += 15; // Đẩy lùi đối thủ khi trúng đòn
                updateUI();
            }

            setTimeout(() => { p1.attacking = false; }, 200);
        }

        // AI Máy đơn giản tự di chuyển và tấn công
        function updateAI() {
            if (p2.hp <= 0 || p1.hp <= 0) return;
            if (p2.x > p1.x + 40) p2.x -= 1.5;
            else if (p2.x < p1.x - 40) p2.x += 1.5;

            // Tự đánh khi lại gần
            if (Math.abs(p2.x - p1.x) < 45 && Math.random() < 0.03) {
                p1.hp = Math.max(0, p1.hp - 6);
                p1.x -= 10;
                updateUI();
            }
        }

        function updateUI() {
            document.getElementById("p1Health").style.width = p1.hp + "%";
            document.getElementById("p2Health").style.width = p2.hp + "%";
        }

        function update() {
            // Trọng lực & Di chuyển
            p1.x += p1.vx; p1.y += p1.vy;
            if (p1.y < 200) p1.vy += 0.8; else { p1.y = 200; p1.vy = 0; }
            
            // Giới hạn màn hình
            p1.x = Math.max(0, Math.min(canvas.width - p1.w, p1.x));
            p2.x = Math.max(0, Math.min(canvas.width - p2.w, p2.x));

            updateAI();

            // Vẽ màn hình
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Vẽ Sàn nhà
            ctx.fillStyle = '#333';
            ctx.fillRect(0, 260, canvas.width, 40);

            // Vẽ P1
            ctx.fillStyle = p1.color;
            ctx.fillRect(p1.x, p1.y, p1.w, p1.h);
            if (p1.attacking) {
                ctx.fillStyle = '#f1c40f';
                ctx.fillRect(p1.x + p1.w, p1.y + 15, 20, 10); // Hiệu ứng tay đấm
            }

            // Vẽ P2
            ctx.fillStyle = p2.color;
            ctx.fillRect(p2.x, p2.y, p2.w, p2.h);

            // Kiểm tra Thua / Thắng
            if (p1.hp <= 0 || p2.hp <= 0) {
                clearInterval(gameInterval);
                ctx.fillStyle = "#fff";
                ctx.font = "bold 30px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText(p1.hp > 0 ? "PLAYER 1 THẮNG!" : "AI THẮNG!", canvas.width / 2, 140);
                document.getElementById("restartBtn").style.display = "block";
            }
        }

        initGame();
    </script>
</body>
</html>
