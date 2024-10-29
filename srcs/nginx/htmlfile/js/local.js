function local_pong(mode) {
    const canvas = document.getElementById('local_pong');
    const context = canvas.getContext('2d');
    const playerScoreElement = document.getElementById('PlayerScore');
    const aiScoreElement = document.getElementById('AIScore');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const keysPressed = {};
    let isPaused = false;

    const W = 87;
    const S = 83;
    const UP_ARROW = 38;
    const DOWN_ARROW = 40;
    const SPACE = 32;

    class Local_Ball {
        constructor(pos, velocity, radius) {
            this.pos = pos;
            this.velocity = velocity;
            this.radius = radius;
        }
    
        update() {
            this.pos.x += this.velocity.x;
            this.pos.y += this.velocity.y;
        }
    
        draw(context) {
            context.fillStyle = "#33ff00";
            context.strokeStyle = "#33ff00";
            context.beginPath();
            context.arc(this.pos.x, this.pos.y, this.radius, 0, Math.PI * 2);
            context.fill();
            context.stroke();
        }
    }
    
    class Local_Paddle {
        constructor(pos, velocity, width, height) {
            this.pos = pos;
            this.velocity = velocity;
            this.width = width;
            this.height = height;
            this.score = 0;
        }
        update(keysPressed, player) {
            if (keysPressed[UP_ARROW] && player == 2) {
                this.pos.y -= this.velocity.y;
            }
            if (keysPressed[DOWN_ARROW] && player == 2) {
                this.pos.y += this.velocity.y;
            }
            if (keysPressed[W] && player == 1) {
                this.pos.y -= this.velocity.y;
            }
            if (keysPressed[S] && player == 1) {
                this.pos.y += this.velocity.y;
            }
        }
    
        draw(context, color) {
            context.fillStyle = color;
            context.fillRect(this.pos.x, this.pos.y, this.width, this.height);
        }
    
        getHalfWidth() {
            return (this.width / 2);
        }
    
        getHalfHeight() {
            return (this.height / 2);
        }
    
        getCenter() {
            return vec2(
                this.pos.x + this.getHalfWidth(),
                this.pos.y + this.getHalfHeight()
            );
        }
    }
    
    function vec2(x, y) {
        return { x, y };
    }
    
    class Local_Game {
        constructor(context, width, height, mode) {
            this.context = context;
            this.width = width;
            this.height = height;
            this.mode = mode;
            this.ball = new Local_Ball(vec2(200, 200), vec2(8, 8), 20);
            this.paddle1 = new Local_Paddle(vec2(0, 50), vec2(10, 10), 20, 160);
            this.paddle2 = new Local_Paddle(vec2(width-20, 200), vec2(10, 10), 20, 160);
            this.game_finish =  false;
        }
    
        update(keysPressed) {
            this.ball.update();
            this.paddle1.update(keysPressed, 1);
            if (this.mode === "ai") {
                this.AIPlayer();
            } else if (this.mode === "multiplayer_local") {
                this.paddle2.update(keysPressed, 2);
            }
            this.ballCollisionWithTheEdges();
            this.paddleCollisionWithTheEdges();
            this.ballCollisionWithThePaddle();
            this.gameScore();
        }
    
        render(isPaused) {
            this.context.fillStyle = "rgba(0, 0, 0, 0.4)";
            this.context.fillRect(0, 0, this.width, this.height);
            this.ball.draw(this.context);
            this.paddle1.draw(this.context, "#33ff00");
            if (this.mode == 'ai')
                this.paddle2.draw(this.context, "#A6A6A6");
            else
                this.paddle2.draw(this.context, "#FF5F1F");
            this.drawGameFrame();
    
            if (isPaused)
                this.pauseTable();
        }
    
        loop(keysPressed, isPaused) {
            if (!isPaused) {
                if (this.game_finish){
                    return ;
                }
                this.update(keysPressed);
            }
            this.render(isPaused);
        }
    
        ballCollisionWithTheEdges() {
            if (this.ball.pos.y + this.ball.radius > this.height || this.ball.pos.y - this.ball.radius <= 0) {
                this.ball.velocity.y *= -1;
            }
        }
    
        paddleCollisionWithTheEdges() {
            if (this.paddle1.pos.y <= 0)
                this.paddle1.pos.y = 0;
    
            if (this.paddle1.pos.y + this.paddle1.height >= this.height)
                this.paddle1.pos.y = this.height - this.paddle1.height;
    
            if (this.paddle2.pos.y <= 0)
                this.paddle2.pos.y = 0;
    
            if (this.paddle2.pos.y + this.paddle2.height >= this.height)
                this.paddle2.pos.y = this.height - this.paddle2.height;
        }
    
        ballCollisionWithThePaddle() {
            let dx1 = Math.abs(this.ball.pos.x - this.paddle1.getCenter().x);
            let dy1 = Math.abs(this.ball.pos.y - this.paddle1.getCenter().y);
            let dx2 = Math.abs(this.ball.pos.x - this.paddle2.getCenter().x);
            let dy2 = Math.abs(this.ball.pos.y - this.paddle2.getCenter().y);
    
            if (dx1 <= (this.ball.radius + this.paddle1.getHalfWidth()) && dy1 <= (this.ball.radius + this.paddle1.getHalfHeight())) {
                this.ball.velocity.x *= -1;
                this.ball.velocity.x += 3;
                this.ball.velocity.y += 3;
            }
            if (dx2 <= (this.ball.radius + this.paddle2.getHalfWidth()) && dy2 <= (this.ball.radius + this.paddle2.getHalfHeight())) {
                this.ball.velocity.x += 3;
                this.ball.velocity.y += 3;
                this.ball.velocity.x *= -1;
            }
        }
    
        respawnBall() {
            this.ball.pos.x = this.width / 2;
            this.ball.pos.y = this.height / 2;
    
            this.ball.velocity.x = 0;
            this.ball.velocity.y = 0;
    
            setTimeout(() => {
                let angle;
                let speed = 12;
    
                do {
                    angle = Math.random() * 2 * Math.PI;
                } while (Math.abs(Math.sin(angle)) < 0.3 || Math.abs(Math.cos(angle)) < 0.3);
    
                this.ball.velocity.x = Math.cos(angle) * speed;
                this.ball.velocity.y = Math.sin(angle) * speed;
            }, 500);
        }
    
        gameScore() {
            if (this.paddle1.score != 5 && this.paddle2.score != 5) {
                if (this.ball.pos.x <= -this.ball.radius) {
                    this.paddle2.score += 1;
                    aiScoreElement.innerHTML = this.paddle2.score;
                    this.respawnBall();
                }
    
                if (this.ball.pos.x >= this.ball.radius + this.width) {
                    this.paddle1.score += 1;
                    playerScoreElement.innerHTML = this.paddle1.score;
                    this.respawnBall();
                }
            }
            else
            {
               window.history.pushState({}, "", '/play');
               loadPage(selectPage('/play'));
               this.game_finish = true;
               return ;
            }
        }
    
        drawGameFrame() {
            this.context.strokeStyle = '#ffff00';
    
            this.context.beginPath();
            this.context.lineWidth = 15;
            this.context.moveTo(0, 0)
            this.context.lineTo(this.width, 0);
            this.context.stroke();
    
            this.context.beginPath();
            this.context.lineWidth = 15;
            this.context.moveTo(0, this.height)
            this.context.lineTo(this.width, this.height);
            this.context.stroke();
    
            this.context.beginPath();
            this.context.lineWidth = 15;
            this.context.moveTo(0, 0)
            this.context.lineTo(0, this.height);
            this.context.stroke();
    
            this.context.beginPath();
            this.context.lineWidth = 15;
            this.context.moveTo(this.width, 0)
            this.context.lineTo(this.width, this.height);
            this.context.stroke();
    
            this.context.beginPath();
            this.context.lineWidth = 12;
            this.context.moveTo(this.width / 2, 0)
            this.context.lineTo(this.width / 2, this.height);
            this.context.stroke();
    
            this.context.beginPath();
            this.context.arc(this.width / 2, this.height / 2, 40, 0, Math.PI * 2);
            this.context.stroke();
        }
    
        pauseTable() {
            this.context.fillStyle = "rgba(0, 0, 0, 0.5)";
            this.context.fillRect(0, 0, this.width, this.height);
    
            this.context.fillStyle = "#FFFFFF";
            this.context.font = "48px Arial";
            this.context.textAlign = "center";
            this.context.fillText("Game Paused", this.width / 2, this.height / 2);
        }
    
        AIPlayer() {
            if (this.ball.velocity.x > 0) {
                if (this.ball.pos.y > this.paddle2.pos.y) {
                    this.paddle2.pos.y += this.paddle2.velocity.y;
    
                    if (this.paddle2.pos.y + this.paddle2.height >= this.height)
                        this.paddle2.pos.y = this.height - this.paddle2.height;
                }
    
                if (this.ball.pos.y < this.paddle2.pos.y) {
                    this.paddle2.pos.y -= this.paddle2.velocity.y;
    
                    if (this.paddle2.pos.y + this.paddle2.height <= 0)
                        this.paddle2.pos.y = 0;
                }
            }
        }
    }
    // Utility function for creating 2D vectors

    const game = new Local_Game(context, canvas.width, canvas.height, mode);

    document.addEventListener('keydown', (e) => {
        keysPressed[e.keyCode] = true;
        if (e.keyCode === SPACE) {
            isPaused = !isPaused;
        }
    });

    document.addEventListener('keyup', (e) => {
        keysPressed[e.keyCode] = false;
    });

    function gameLoop() {
        if (!game.game_finish) {
            game.loop(keysPressed, isPaused);
            requestAnimationFrame(gameLoop);
        }
    }

    canvas.style.display = 'block';
    gameLoop();
}

// Router'daki '/local' yolu için bu fonksiyonu çağırın
// routers['/local'] = '../pages/local.html';
// scripts['/local'] = () => local_pong("multiplayer_local");
