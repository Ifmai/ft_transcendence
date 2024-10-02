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

	draw(context){
		context.fillStyle = "#33ff00";
		context.strokeStyle = "#33ff00";
		context.beginPath();
		context.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
		context.fill();
		context.stroke();
	}
}
