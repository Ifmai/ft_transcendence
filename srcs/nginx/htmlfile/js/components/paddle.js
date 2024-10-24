class Paddle {
    constructor(x, y, width, height, dy) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.dy = dy;
    }

    update() {
        this.y += this.dy;
        if (this.y < 0) {
            this.y = 0;
        } else if (this.y + this.height > window.innerHeight) {
            this.y = window.innerHeight - this.height;
        }
    }

    updateState(data) {
        this.y = data['positionY'];
        this.dy = data['velocity'];
    }

    draw(context, color) {
		context.fillStyle = color;
		context.fillRect(this.x, this.y, this.width, this.height);
	}
}
