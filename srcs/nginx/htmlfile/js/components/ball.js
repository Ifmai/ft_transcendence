class Ball {
	constructor(x, y, radius, dx, dy) {
		this.x = x;
		this.y = y;
		this.radius = radius;
		this.dx = dx;
		this.dy = dy;
	}

	update(){
		this.x += this.dx;
		this.y += this.dy;
	}

	updateState(data){
		this.x = data['positionX'];
		this.y = data['positionY'];
		this.dx = data['velocityX'];
		this.dy = data['velocityY'];
	}

	draw(context, color){
		context.fillStyle = color;
		context.strokeStyle = color;
		context.beginPath();
		context.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
		context.fill();
		context.stroke();
	}
}
