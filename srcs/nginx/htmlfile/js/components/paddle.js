class Paddle {
    constructor(x, y, width, height, dy, color) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.dy = dy;
        this.color = color;
        this.neon = 0;
    }

    update() {
        this.y += this.dy;
        if (this.y < 0) {
            this.y = 0;
        } else if (this.y + this.height > window.innerHeight) {
            this.y = window.innerHeight - this.height;
        }
    }

    setColor(color) {
        this.color = color;
    }

    updateState(data) {
        this.y = data['positionY'];
        this.dy = data['velocity'];
    }

    draw(context) {
        if (this.neon === 1) {
            // Set shadow properties for the neon effect
            context.shadowColor = this.color; // Use the paddle color as the glow color
            context.shadowBlur = 20; // Control the blur effect
            context.shadowOffsetX = 0; // No horizontal offset
            context.shadowOffsetY = 0; // No vertical offset
        } else {
            // Reset shadow properties if not neon
            context.shadowColor = 'transparent'; // No shadow color
            context.shadowBlur = 0; // No blur
        }

        // Draw the paddle
        context.fillStyle = this.color;
        context.fillRect(this.x, this.y, this.width, this.height);

        // Reset shadow properties to avoid affecting other drawings
        context.shadowColor = 'transparent';
        context.shadowBlur = 0;
    }
}
