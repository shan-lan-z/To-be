// 游戏常量
const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 600;
const TANK_SIZE = 30;
const BULLET_SIZE = 4;
const TANK_SPEED = 3;
const BULLET_SPEED = 5;
const ENEMY_SPAWN_INTERVAL = 3000;
const MAX_ENEMIES = 5;

// 游戏状态
let gameState = {
    score: 0,
    lives: 3,
    enemiesRemaining: 5,
    gameOver: false,
    gameWon: false
};

// 获取Canvas和Context
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 玩家坦克
let playerTank = {
    x: CANVAS_WIDTH / 2,
    y: CANVAS_HEIGHT - 50,
    direction: 0, // 0: 上, 1: 右, 2: 下, 3: 左
    color: '#00ff00',
    lastShot: 0,
    shotCooldown: 300
};

// 游戏对象数组
let bullets = [];
let enemies = [];
let explosions = [];

// 按键状态
let keys = {};

// 移动端控制状态
let mobileControls = {
    up: false,
    down: false,
    left: false,
    right: false,
    shoot: false
};

// 检测是否为移动设备
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

// 初始化移动端控制
function initMobileControls() {
    if (!isMobile) return;
    
    // 移动控制按钮
    document.getElementById('btnUp').addEventListener('touchstart', (e) => {
        e.preventDefault();
        mobileControls.up = true;
    });
    document.getElementById('btnUp').addEventListener('touchend', (e) => {
        e.preventDefault();
        mobileControls.up = false;
    });
    
    document.getElementById('btnDown').addEventListener('touchstart', (e) => {
        e.preventDefault();
        mobileControls.down = true;
    });
    document.getElementById('btnDown').addEventListener('touchend', (e) => {
        e.preventDefault();
        mobileControls.down = false;
    });
    
    document.getElementById('btnLeft').addEventListener('touchstart', (e) => {
        e.preventDefault();
        mobileControls.left = true;
    });
    document.getElementById('btnLeft').addEventListener('touchend', (e) => {
        e.preventDefault();
        mobileControls.left = false;
    });
    
    document.getElementById('btnRight').addEventListener('touchstart', (e) => {
        e.preventDefault();
        mobileControls.right = true;
    });
    document.getElementById('btnRight').addEventListener('touchend', (e) => {
        e.preventDefault();
        mobileControls.right = false;
    });
    
    document.getElementById('btnShoot').addEventListener('touchstart', (e) => {
        e.preventDefault();
        mobileControls.shoot = true;
    });
    document.getElementById('btnShoot').addEventListener('touchend', (e) => {
        e.preventDefault();
        mobileControls.shoot = false;
    });
    
    // 防止页面滚动
    document.addEventListener('touchmove', (e) => {
        e.preventDefault();
    }, { passive: false });
}

// 初始化游戏
function initGame() {
    gameState = {
        score: 0,
        lives: 3,
        enemiesRemaining: 5,
        gameOver: false,
        gameWon: false
    };
    
    playerTank = {
        x: CANVAS_WIDTH / 2,
        y: CANVAS_HEIGHT - 50,
        direction: 0,
        color: '#00ff00',
        lastShot: 0,
        shotCooldown: 300
    };
    
    bullets = [];
    enemies = [];
    explosions = [];
    
    updateUI();
    spawnEnemy();
}

// 生成敌方坦克
function spawnEnemy() {
    if (enemies.length < MAX_ENEMIES && gameState.enemiesRemaining > 0) {
        const side = Math.floor(Math.random() * 4); // 0: 上, 1: 右, 2: 下, 3: 左
        let x, y, direction;
        
        switch(side) {
            case 0: // 上
                x = Math.random() * (CANVAS_WIDTH - TANK_SIZE);
                y = -TANK_SIZE;
                direction = 2;
                break;
            case 1: // 右
                x = CANVAS_WIDTH;
                y = Math.random() * (CANVAS_HEIGHT - TANK_SIZE);
                direction = 3;
                break;
            case 2: // 下
                x = Math.random() * (CANVAS_WIDTH - TANK_SIZE);
                y = CANVAS_HEIGHT;
                direction = 0;
                break;
            case 3: // 左
                x = -TANK_SIZE;
                y = Math.random() * (CANVAS_HEIGHT - TANK_SIZE);
                direction = 1;
                break;
        }
        
        enemies.push({
            x: x,
            y: y,
            direction: direction,
            color: '#ff0000',
            lastShot: 0,
            shotCooldown: 1000 + Math.random() * 1000,
            moveTimer: 0,
            moveInterval: 1000 + Math.random() * 2000
        });
    }
}

// 绘制坦克
function drawTank(tank) {
    ctx.save();
    ctx.translate(tank.x + TANK_SIZE / 2, tank.y + TANK_SIZE / 2);
    ctx.rotate(tank.direction * Math.PI / 2);
    
    // 坦克主体
    ctx.fillStyle = tank.color;
    ctx.fillRect(-TANK_SIZE / 2, -TANK_SIZE / 2, TANK_SIZE, TANK_SIZE);
    
    // 坦克炮管
    ctx.fillStyle = '#333';
    ctx.fillRect(-2, -TANK_SIZE / 2 - 8, 4, 8);
    
    // 坦克履带
    ctx.fillStyle = '#666';
    ctx.fillRect(-TANK_SIZE / 2 - 2, -TANK_SIZE / 2, 2, TANK_SIZE);
    ctx.fillRect(TANK_SIZE / 2, -TANK_SIZE / 2, 2, TANK_SIZE);
    
    ctx.restore();
}

// 绘制子弹
function drawBullet(bullet) {
    ctx.fillStyle = bullet.color;
    ctx.beginPath();
    ctx.arc(bullet.x, bullet.y, BULLET_SIZE, 0, Math.PI * 2);
    ctx.fill();
}

// 绘制爆炸效果
function drawExplosion(explosion) {
    const alpha = 1 - (explosion.timer / explosion.duration);
    ctx.save();
    ctx.globalAlpha = alpha;
    
    // 爆炸粒子
    for (let i = 0; i < 8; i++) {
        const angle = (i / 8) * Math.PI * 2;
        const x = explosion.x + Math.cos(angle) * explosion.radius;
        const y = explosion.y + Math.sin(angle) * explosion.radius;
        
        ctx.fillStyle = `hsl(${30 + explosion.timer * 2}, 100%, 50%)`;
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fill();
    }
    
    ctx.restore();
}

// 发射子弹
function shootBullet(tank, isPlayer = false) {
    const now = Date.now();
    if (now - tank.lastShot < tank.shotCooldown) return;
    
    let bulletX = tank.x + TANK_SIZE / 2;
    let bulletY = tank.y + TANK_SIZE / 2;
    let bulletVX = 0;
    let bulletVY = 0;
    
    switch(tank.direction) {
        case 0: bulletVY = -BULLET_SPEED; break; // 上
        case 1: bulletVX = BULLET_SPEED; break;  // 右
        case 2: bulletVY = BULLET_SPEED; break;  // 下
        case 3: bulletVX = -BULLET_SPEED; break; // 左
    }
    
    bullets.push({
        x: bulletX,
        y: bulletY,
        vx: bulletVX,
        vy: bulletVY,
        color: isPlayer ? '#ffff00' : '#ff6666',
        isPlayer: isPlayer
    });
    
    tank.lastShot = now;
}

// 检测碰撞
function checkCollision(rect1, rect2) {
    return rect1.x < rect2.x + rect2.width &&
           rect1.x + rect1.width > rect2.x &&
           rect1.y < rect2.y + rect2.height &&
           rect1.y + rect1.height > rect2.y;
}

// 创建爆炸效果
function createExplosion(x, y) {
    explosions.push({
        x: x,
        y: y,
        radius: 20,
        timer: 0,
        duration: 30
    });
}

// 更新游戏状态
function updateGame() {
    if (gameState.gameOver || gameState.gameWon) return;
    
    const now = Date.now();
    
    // 玩家坦克移动（键盘控制）
    if (keys['w'] || keys['W']) {
        playerTank.direction = 0;
        if (playerTank.y > 0) playerTank.y -= TANK_SPEED;
    }
    if (keys['s'] || keys['S']) {
        playerTank.direction = 2;
        if (playerTank.y < CANVAS_HEIGHT - TANK_SIZE) playerTank.y += TANK_SPEED;
    }
    if (keys['a'] || keys['A']) {
        playerTank.direction = 3;
        if (playerTank.x > 0) playerTank.x -= TANK_SPEED;
    }
    if (keys['d'] || keys['D']) {
        playerTank.direction = 1;
        if (playerTank.x < CANVAS_WIDTH - TANK_SIZE) playerTank.x += TANK_SPEED;
    }
    
    // 移动端控制
    if (mobileControls.up) {
        playerTank.direction = 0;
        if (playerTank.y > 0) playerTank.y -= TANK_SPEED;
    }
    if (mobileControls.down) {
        playerTank.direction = 2;
        if (playerTank.y < CANVAS_HEIGHT - TANK_SIZE) playerTank.y += TANK_SPEED;
    }
    if (mobileControls.left) {
        playerTank.direction = 3;
        if (playerTank.x > 0) playerTank.x -= TANK_SPEED;
    }
    if (mobileControls.right) {
        playerTank.direction = 1;
        if (playerTank.x < CANVAS_WIDTH - TANK_SIZE) playerTank.x += TANK_SPEED;
    }
    
    // 玩家射击（键盘和移动端）
    if (keys[' '] || mobileControls.shoot) {
        shootBullet(playerTank, true);
    }
    
    // 更新子弹
    bullets = bullets.filter(bullet => {
        bullet.x += bullet.vx;
        bullet.y += bullet.vy;
        
        // 移除超出边界的子弹
        if (bullet.x < 0 || bullet.x > CANVAS_WIDTH || 
            bullet.y < 0 || bullet.y > CANVAS_HEIGHT) {
            return false;
        }
        
        return true;
    });
    
    // 更新敌方坦克
    enemies.forEach(enemy => {
        enemy.moveTimer += 16; // 假设60FPS
        
        // 随机移动
        if (enemy.moveTimer > enemy.moveInterval) {
            enemy.direction = Math.floor(Math.random() * 4);
            enemy.moveTimer = 0;
            enemy.moveInterval = 1000 + Math.random() * 2000;
        }
        
        // 移动坦克
        switch(enemy.direction) {
            case 0: if (enemy.y > 0) enemy.y -= TANK_SPEED * 0.5; break;
            case 1: if (enemy.x < CANVAS_WIDTH - TANK_SIZE) enemy.x += TANK_SPEED * 0.5; break;
            case 2: if (enemy.y < CANVAS_HEIGHT - TANK_SIZE) enemy.y += TANK_SPEED * 0.5; break;
            case 3: if (enemy.x > 0) enemy.x -= TANK_SPEED * 0.5; break;
        }
        
        // 敌方射击
        if (Math.random() < 0.01) { // 1% 概率射击
            shootBullet(enemy, false);
        }
    });
    
    // 碰撞检测
    bullets.forEach((bullet, bulletIndex) => {
        const bulletRect = {
            x: bullet.x - BULLET_SIZE,
            y: bullet.y - BULLET_SIZE,
            width: BULLET_SIZE * 2,
            height: BULLET_SIZE * 2
        };
        
        // 子弹击中敌方坦克
        if (bullet.isPlayer) {
            enemies.forEach((enemy, enemyIndex) => {
                const enemyRect = {
                    x: enemy.x,
                    y: enemy.y,
                    width: TANK_SIZE,
                    height: TANK_SIZE
                };
                
                if (checkCollision(bulletRect, enemyRect)) {
                    createExplosion(enemy.x + TANK_SIZE / 2, enemy.y + TANK_SIZE / 2);
                    enemies.splice(enemyIndex, 1);
                    bullets.splice(bulletIndex, 1);
                    gameState.score += 100;
                    gameState.enemiesRemaining--;
                    updateUI();
                }
            });
        } else {
            // 子弹击中玩家坦克
            const playerRect = {
                x: playerTank.x,
                y: playerTank.y,
                width: TANK_SIZE,
                height: TANK_SIZE
            };
            
            if (checkCollision(bulletRect, playerRect)) {
                createExplosion(playerTank.x + TANK_SIZE / 2, playerTank.y + TANK_SIZE / 2);
                bullets.splice(bulletIndex, 1);
                gameState.lives--;
                updateUI();
                
                if (gameState.lives <= 0) {
                    gameState.gameOver = true;
                    document.getElementById('gameStatus').textContent = '游戏结束！按R重新开始';
                } else {
                    // 重置玩家位置
                    playerTank.x = CANVAS_WIDTH / 2;
                    playerTank.y = CANVAS_HEIGHT - 50;
                }
            }
        }
    });
    
    // 更新爆炸效果
    explosions = explosions.filter(explosion => {
        explosion.timer++;
        return explosion.timer < explosion.duration;
    });
    
    // 检查游戏胜利
    if (gameState.enemiesRemaining <= 0 && enemies.length === 0) {
        gameState.gameWon = true;
        document.getElementById('gameStatus').textContent = '恭喜获胜！按R重新开始';
    }
    
    // 生成新敌人
    if (Math.random() < 0.005 && gameState.enemiesRemaining > 0) {
        spawnEnemy();
    }
}

// 绘制游戏
function drawGame() {
    // 清空画布
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    
    // 绘制网格背景
    ctx.strokeStyle = '#222';
    ctx.lineWidth = 1;
    for (let x = 0; x < CANVAS_WIDTH; x += 40) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, CANVAS_HEIGHT);
        ctx.stroke();
    }
    for (let y = 0; y < CANVAS_HEIGHT; y += 40) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(CANVAS_WIDTH, y);
        ctx.stroke();
    }
    
    // 绘制玩家坦克
    drawTank(playerTank);
    
    // 绘制敌方坦克
    enemies.forEach(enemy => drawTank(enemy));
    
    // 绘制子弹
    bullets.forEach(bullet => drawBullet(bullet));
    
    // 绘制爆炸效果
    explosions.forEach(explosion => drawExplosion(explosion));
    
    // 游戏结束或胜利时的覆盖层
    if (gameState.gameOver || gameState.gameWon) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
        
        ctx.fillStyle = gameState.gameWon ? '#00ff00' : '#ff0000';
        ctx.font = '48px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(
            gameState.gameWon ? '胜利！' : '游戏结束',
            CANVAS_WIDTH / 2,
            CANVAS_HEIGHT / 2
        );
        
        ctx.fillStyle = '#fff';
        ctx.font = '24px Arial';
        ctx.fillText(
            '按R重新开始',
            CANVAS_WIDTH / 2,
            CANVAS_HEIGHT / 2 + 50
        );
    }
}

// 更新UI
function updateUI() {
    document.getElementById('score').textContent = gameState.score;
    document.getElementById('lives').textContent = gameState.lives;
    document.getElementById('enemies').textContent = gameState.enemiesRemaining;
}

// 游戏主循环
function gameLoop() {
    updateGame();
    drawGame();
    requestAnimationFrame(gameLoop);
}

// 键盘事件监听
document.addEventListener('keydown', (e) => {
    keys[e.key] = true;
    
    // 重新开始游戏
    if (e.key === 'r' || e.key === 'R') {
        if (gameState.gameOver || gameState.gameWon) {
            initGame();
        }
    }
});

document.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

// 防止空格键滚动页面
document.addEventListener('keydown', (e) => {
    if (e.key === ' ') {
        e.preventDefault();
    }
});

// 开始游戏
initGame();
initMobileControls();
gameLoop();