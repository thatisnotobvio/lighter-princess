const canvas = document.getElementById("heart");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const particles = [];
const heartColor = "#FF4D8D";

function heartFunction(t) {
  const x = 16 * Math.pow(Math.sin(t), 3);
  const y =
    -(13 * Math.cos(t) -
      5 * Math.cos(2 * t) -
      2 * Math.cos(3 * t) -
      Math.cos(4 * t));

  return {
    x: x * 20,
    y: y * 20,
  };
}

class Particle {
  constructor() {
    const t = Math.random() * Math.PI * 2;
    const pos = heartFunction(t);

    this.x = canvas.width / 2 + pos.x;
    this.y = canvas.height / 2 + pos.y;

    this.baseX = this.x;
    this.baseY = this.y;

    this.size = Math.random() * 2 + 1;
    this.offset = Math.random() * 20;
  }

  update(time) {
    const beat = Math.sin(time * 0.005) * 8;

    const dx = this.baseX - canvas.width / 2;
    const dy = this.baseY - canvas.height / 2;

    const dist = Math.sqrt(dx * dx + dy * dy);

    this.x =
      this.baseX + (dx / dist) * beat + (Math.random() - 0.5) * 2;

    this.y =
      this.baseY + (dy / dist) * beat + (Math.random() - 0.5) * 2;
  }

  draw() {
    ctx.fillStyle = heartColor;
    ctx.fillRect(this.x, this.y, this.size, this.size);
  }
}

for (let i = 0; i < 4000; i++) {
  particles.push(new Particle());
}

function animate(time) {
  ctx.fillStyle = "rgba(5, 7, 15, 0.2)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  particles.forEach((particle) => {
    particle.update(time);
    particle.draw();
  });

  requestAnimationFrame(animate);
}

animate();
