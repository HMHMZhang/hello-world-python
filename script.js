// script.js - 游戏逻辑将在这里实现

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const GAME_WIDTH = canvas.width;
const GAME_HEIGHT = canvas.height;

console.log('Canvas initialized:', GAME_WIDTH, GAME_HEIGHT);

// GameObject 基类
class GameObject {
    constructor(x, y, width, height, color = 'gray') {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.color = color;
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }
}

// 碰撞检测函数
function isColliding(obj1, obj2) {
    return obj1.x < obj2.x + obj2.width &&
           obj1.x + obj1.width > obj2.x &&
           obj1.y < obj2.y + obj2.height &&
           obj1.y + obj1.height > obj2.y;
}

// Obstacle 类
class Obstacle extends GameObject {
    constructor(x, y, width, height, color, destructible = false) {
        super(x, y, width, height, color);
        this.destructible = destructible;
        this.active = true; // 障碍物是否存活
    }
}

// Bullet 类
class Bullet extends GameObject {
    constructor(x, y, width, height, color, speed, direction, owner) {
        super(x, y, width, height, color);
        this.speed = speed;
        this.direction = direction;
        this.active = true; // 子弹是否存活
        this.owner = owner; // 'player' or 'enemy'
    }

    update() {
        switch (this.direction) {
            case 0: // Up
                this.y -= this.speed;
                break;
            case 1: // Right
                this.x += this.speed;
                break;
            case 2: // Down
                this.y += this.speed;
                break;
            case 3: // Left
                this.x -= this.speed;
                break;
        }

        // 检查是否出界
        if (this.x < 0 || this.x > GAME_WIDTH || this.y < 0 || this.y > GAME_HEIGHT) {
            this.active = false;
        }
    }
}

// Tank 类
class Tank extends GameObject {
    constructor(x, y, width, height, color, speed, direction, isPlayer = false) {
        super(x, y, width, height, color);
        this.speed = speed;
        this.direction = direction; // 0: up, 1: right, 2: down, 3: left
        this.health = 1;
        this.isPlayer = isPlayer;
        this.lastShotTime = 0;
        this.shotInterval = 1000; // 敌方坦克射击间隔
        this.moveTimer = 0;
        this.moveInterval = 2000; // 敌方坦克移动方向改变间隔
    }

    draw() {
        super.draw();
        // 绘制炮管
        ctx.fillStyle = 'dark' + this.color;
        switch (this.direction) {
            case 0: // Up
                ctx.fillRect(this.x + this.width / 2 - 2, this.y - 5, 4, 10);
                break;
            case 1: // Right
                ctx.fillRect(this.x + this.width - 5, this.y + this.height / 2 - 2, 10, 4);
                break;
            case 2: // Down
                ctx.fillRect(this.x + this.width / 2 - 2, this.y + this.height - 5, 4, 10);
                break;
            case 3: // Left
                ctx.fillRect(this.x - 5, this.y + this.height / 2 - 2, 10, 4);
                break;
        }
    }

    update(deltaTime) {
        if (this.isPlayer) return; // 玩家坦克不使用此AI更新

        this.moveTimer += deltaTime;
        if (this.moveTimer >= this.moveInterval) {
            this.direction = Math.floor(Math.random() * 4); // 随机改变方向
            this.moveTimer = 0;
            this.moveInterval = Math.random() * 2000 + 1000; // 随机设置下次改变方向的时间
        }

        // 尝试移动
        let nextX = this.x;
        let nextY = this.y;
        switch (this.direction) {
            case 0: // Up
                nextY -= this.speed;
                break;
            case 1: // Right
                nextX += this.speed;
                break;
            case 2: // Down
                nextY += this.speed;
                break;
            case 3: // Left
                nextX -= this.speed;
                break;
        }

        // 检查边界碰撞
        if (nextX < 0) nextX = 0;
        if (nextX + this.width > GAME_WIDTH) nextX = GAME_WIDTH - this.width;
        if (nextY < 0) nextY = 0;
        if (nextY + this.height > GAME_HEIGHT) nextY = GAME_HEIGHT - this.height;

        // 检查与不可破坏障碍物的碰撞
        let collidedWithObstacle = false;
        const tempTank = { x: nextX, y: nextY, width: this.width, height: this.height };
        for (let i = 0; i < obstacles.length; i++) {
            const obstacle = obstacles[i];
            if (obstacle.active && !obstacle.destructible && isColliding(tempTank, obstacle)) {
                collidedWithObstacle = true;
                // 如果即将撞到障碍物，尝试改变方向
                this.direction = Math.floor(Math.random() * 4); 
                this.moveTimer = 0; // 立即重置计时器以重新评估移动
                break;
            }
        }

        if (!collidedWithObstacle) {
            this.x = nextX;
            this.y = nextY;
        }

        // 尝试射击
        if (Date.now() - this.lastShotTime > this.shotInterval) {
            this.shoot();
            this.lastShotTime = Date.now();
            this.shotInterval = Math.random() * 1500 + 500; // 随机设置下次射击间隔
        }
    }

    shoot() {
        let bulletX, bulletY;
        const bulletSize = 5;
        const bulletSpeed = 5;

        switch (this.direction) {
            case 0: // Up
                bulletX = this.x + this.width / 2 - bulletSize / 2;
                bulletY = this.y - bulletSize;
                break;
            case 1: // Right
                bulletX = this.x + this.width;
                bulletY = this.y + this.height / 2 - bulletSize / 2;
                break;
            case 2: // Down
                bulletX = this.x + this.width / 2 - bulletSize / 2;
                bulletY = this.y + this.height;
                break;
            case 3: // Left
                bulletX = this.x - bulletSize;
                bulletY = this.y + this.height / 2 - bulletSize / 2;
                break;
        }
        bullets.push(new Bullet(bulletX, bulletY, bulletSize, bulletSize, 'yellow', bulletSpeed, this.direction, this.isPlayer ? 'player' : 'enemy'));
    }

    }
}

    }
}

// 玩家坦克
const playerTank = new Tank(GAME_WIDTH / 2 - 20, GAME_HEIGHT - 50, 40, 40, 'green', 2, 0, true);

// 敌方坦克
const enemyTanks = [];

// UI 元素
const startScreen = document.getElementById('start-screen');
const startButton = document.getElementById('start-button');
const endScreen = document.getElementById('end-screen');
const endMessage = document.getElementById('end-message');
const finalScoreDisplay = document.getElementById('final-score');
const restartButton = document.getElementById('restart-button');
const scoreDisplay = document.getElementById('score');
const livesDisplay = document.getElementById('lives');
const gameCanvas = document.getElementById('gameCanvas');
const gameInfo = document.getElementById('game-info');

let score = 0;
let playerLives = 3;
let gameState = 'start'; // 'start', 'playing', 'gameOver', 'victory'

// 存储按下的键
const keys = {};

// 存储所有子弹
const bullets = [];

// 初始化游戏 (在startGame中调用)
function initializeGame() {
    score = 0;
    playerLives = 3;
    playerTank.x = GAME_WIDTH / 2 - 20;
    playerTank.y = GAME_HEIGHT - 50;
    playerTank.direction = 0;
    playerTank.health = 1; // 重置玩家坦克生命值

    enemyTanks.length = 0; // 清空敌方坦克
    enemyTanks.push(new Tank(100, 100, 40, 40, 'blue', 1, 2, false));
    enemyTanks.push(new Tank(GAME_WIDTH - 140, 100, 40, 40, 'blue', 1, 2, false));

    bullets.length = 0; // 清空子弹

    // 重新生成障碍物 (如果障碍物是可破坏的, 每次游戏开始需要重新生成)
    obstacles.length = 0;
    for (let row = 0; row < gameMap.length; row++) {
        for (let col = 0; col < gameMap[row].length; col++) {
            const tile = gameMap[row][col];
            if (tile === 1) { // 砖墙
                obstacles.push(new Obstacle(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE, 'brown', true));
            } else if (tile === 2) { // 钢墙
                obstacles.push(new Obstacle(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE, 'silver', false));
            }
        }
    }
}

function updateUI() {
    scoreDisplay.textContent = score;
    livesDisplay.textContent = playerLives;
}

function startGame() {
    gameState = 'playing';
    startScreen.style.display = 'none';
    endScreen.style.display = 'none';
    gameCanvas.style.display = 'block';
    gameInfo.style.display = 'flex'; // 显示游戏信息
    initializeGame();
    updateUI();
    requestAnimationFrame(gameLoop);
}

function endGame(message) {
    gameState = 'gameOver';
    endMessage.textContent = message;
    finalScoreDisplay.textContent = score;
    startScreen.style.display = 'none';
    endScreen.style.display = 'flex'; // 使用 flexbox 布局来居中内容
    gameCanvas.style.display = 'none';
    gameInfo.style.display = 'none';
}

function checkGameEndConditions() {
    if (playerLives <= 0) {
        endGame('游戏失败!');
        return true;
    }
    if (enemyTanks.length === 0) {
        endGame('游戏胜利!');
        return true;
    }
    return false;
}

startButton.addEventListener('click', startGame);
restartButton.addEventListener('click', startGame);

// 初始显示开始屏幕
startScreen.style.display = 'flex';
gameCanvas.style.display = 'none';
gameInfo.style.display = 'none';

window.addEventListener('keydown', (e) => {
    keys[e.code] = true;
    if (e.code === 'Space' && gameState === 'playing') {
        // 发射子弹
        let bulletX, bulletY;
        const bulletSize = 5;
        const bulletSpeed = 5;

        switch (playerTank.direction) {
            case 0: // Up
                bulletX = playerTank.x + playerTank.width / 2 - bulletSize / 2;
                bulletY = playerTank.y - bulletSize;
                break;
            case 1: // Right
                bulletX = playerTank.x + playerTank.width;
                bulletY = playerTank.y + playerTank.height / 2 - bulletSize / 2;
                break;
            case 2: // Down
                bulletX = playerTank.x + playerTank.width / 2 - bulletSize / 2;
                bulletY = playerTank.y + playerTank.height;
                break;
            case 3: // Left
                bulletX = playerTank.x - bulletSize;
                bulletY = playerTank.y + playerTank.height / 2 - bulletSize / 2;
                break;
        }
        bullets.push(new Bullet(bulletX, bulletY, bulletSize, bulletSize, 'red', bulletSpeed, playerTank.direction, 'player'));
    }
});

window.addEventListener('keyup', (e) => {
    keys[e.code] = false;
});

// 游戏地图 (0: 空, 1: 砖墙-可破坏, 2: 钢墙-不可破坏)
const gameMap = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 2],
    [2, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 2],
    [2, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 2],
    [2, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 2],
    [2, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
];

const obstacles = [];
const TILE_SIZE = GAME_WIDTH / gameMap[0].length;

// 游戏主循环
function gameLoop(currentTime) {
    if (gameState !== 'playing') {
        requestAnimationFrame(gameLoop);
        return;
    }

    if (!lastTime) lastTime = currentTime;
    const deltaTime = currentTime - lastTime;
    lastTime = currentTime;

    // 清除画布
    ctx.clearRect(0, 0, GAME_WIDTH, GAME_HEIGHT);

    // 更新游戏状态
    // 玩家坦克移动
    let nextX = playerTank.x;
    let nextY = playerTank.y;

    if (keys['ArrowUp'] || keys['KeyW']) {
        playerTank.direction = 0;
        nextY -= playerTank.speed;
    }
    if (keys['ArrowRight'] || keys['KeyD']) {
        playerTank.direction = 1;
        nextX += playerTank.speed;
    }
    if (keys['ArrowDown'] || keys['KeyS']) {
        playerTank.direction = 2;
        nextY += playerTank.speed;
    }
    if (keys['ArrowLeft'] || keys['KeyA']) {
        playerTank.direction = 3;
        nextX -= playerTank.speed;
    }

    // 检查玩家坦克与边界的碰撞
    if (nextX < 0) nextX = 0;
    if (nextX + playerTank.width > GAME_WIDTH) nextX = GAME_WIDTH - playerTank.width;
    if (nextY < 0) nextY = 0;
    if (nextY + playerTank.height > GAME_HEIGHT) nextY = GAME_HEIGHT - playerTank.height;

    // 检查玩家坦克与障碍物的碰撞
    let collidedWithObstacle = false;
    const tempPlayerTank = { x: nextX, y: nextY, width: playerTank.width, height: playerTank.height };

    for (let i = 0; i < obstacles.length; i++) {
        const obstacle = obstacles[i];
        if (obstacle.active && !obstacle.destructible && isColliding(tempPlayerTank, obstacle)) {
            collidedWithObstacle = true;
            break;
        }
    }

    if (!collidedWithObstacle) {
        playerTank.x = nextX;
        playerTank.y = nextY;
    }

    // 更新敌方坦克AI
    enemyTanks.forEach(enemyTank => enemyTank.update(deltaTime));

    // 子弹与敌方坦克碰撞检测
    for (let i = bullets.length - 1; i >= 0; i--) {
        const bullet = bullets[i];
        if (bullet.owner === 'player') { // 只有玩家子弹才能击中敌方坦克
            for (let j = enemyTanks.length - 1; j >= 0; j--) {
                const enemyTank = enemyTanks[j];
                if (isColliding(bullet, enemyTank)) {
                    bullet.active = false; // 子弹销毁
                    enemyTank.health--; // 敌方坦克生命值减少
                    if (enemyTank.health <= 0) {
                        enemyTanks.splice(j, 1); // 敌方坦克销毁
                        score += 100; // 增加分数
                        updateUI();
                    }
                    break; // 一个子弹只能击中一个目标
                }
            }
        }
    }

    // 敌方子弹与玩家坦克碰撞检测
    for (let i = bullets.length - 1; i >= 0; i--) {
        const bullet = bullets[i];
        if (bullet.owner === 'enemy' && isColliding(bullet, playerTank)) {
            bullet.active = false; // 子弹销毁
            playerTank.health--; // 玩家坦克生命值减少
            if (playerTank.health <= 0) {
                playerLives--;
                updateUI();
                if (playerLives > 0) {
                    // 玩家坦克重置位置
                    playerTank.x = GAME_WIDTH / 2 - 20;
                    playerTank.y = GAME_HEIGHT - 50;
                    playerTank.direction = 0;
                    playerTank.health = 1; // 重置生命值
                } else {
                    endGame('游戏失败!');
                }
            }
            break;
        }
    }

    // 子弹与障碍物碰撞检测
    for (let i = bullets.length - 1; i >= 0; i--) {
        const bullet = bullets[i];
        for (let j = obstacles.length - 1; j >= 0; j--) {
            const obstacle = obstacles[j];
            if (obstacle.active && isColliding(bullet, obstacle)) {
                bullet.active = false; // 子弹销毁
                if (obstacle.destructible) {
                    obstacles.splice(j, 1); // 障碍物销毁
                }
                break; // 一个子弹只能击中一个障碍物
            }
        }
    }

    // 更新子弹位置
    for (let i = 0; i < bullets.length; i++) {
        bullets[i].update();
    }

    // 移除不活跃的子弹
    for (let i = bullets.length - 1; i >= 0; i--) {
        if (!bullets[i].active) {
            bullets.splice(i, 1);
        }
    }

    // 检查游戏结束条件
    if (checkGameEndConditions()) {
        return;
    }

    // 绘制游戏元素
    obstacles.forEach(obstacle => obstacle.draw());
    playerTank.draw();
    enemyTanks.forEach(enemyTank => enemyTank.draw()); // 绘制敌方坦克
    bullets.forEach(bullet => bullet.draw());

    requestAnimationFrame(gameLoop);
}

// 初始显示开始屏幕
startScreen.style.display = 'flex';
gameCanvas.style.display = 'none';
gameInfo.style.display = 'none';

requestAnimationFrame(gameLoop);