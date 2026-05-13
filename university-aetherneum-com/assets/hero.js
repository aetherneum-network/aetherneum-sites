/* Hero animation — falling code rain + faint hooded silhouette echo
   Quieter than the root site (lower opacity) so it doesn't compete with content. */
(function () {
  const canvas = document.getElementById('hero-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W = 0, H = 0;
  const DPR = Math.min(window.devicePixelRatio || 1, 2);
  let cols = [];
  const FONT_SIZE = 13;
  const CHARS = '0123456789ABCDEF·∴⋄◇◆▪▫░▒▓ÆÆØΩæþƎ⌬⎔⏣';

  function resize() {
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = W * DPR;
    canvas.height = H * DPR;
    canvas.style.width = W + 'px';
    canvas.style.height = H + 'px';
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    ctx.font = FONT_SIZE + 'px JetBrains Mono, monospace';
    const colCount = Math.floor(W / FONT_SIZE);
    cols = new Array(colCount).fill(0).map(() => ({
      y: Math.random() * H,
      speed: 0.35 + Math.random() * 1.0,
      brightness: 0.12 + Math.random() * 0.4,
      lastChar: CHARS[Math.floor(Math.random() * CHARS.length)],
      changeRate: 0.05 + Math.random() * 0.08,
    }));
  }

  function draw() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.09)';
    ctx.fillRect(0, 0, W, H);
    for (let i = 0; i < cols.length; i++) {
      const c = cols[i];
      const x = i * FONT_SIZE;
      if (Math.random() < c.changeRate) {
        c.lastChar = CHARS[Math.floor(Math.random() * CHARS.length)];
      }
      ctx.fillStyle = 'rgba(103, 232, 249, ' + c.brightness + ')';
      ctx.fillText(c.lastChar, x, c.y);
      ctx.fillStyle = 'rgba(34, 211, 238, ' + (c.brightness * 0.3) + ')';
      ctx.fillText(c.lastChar, x, c.y - FONT_SIZE);
      c.y += c.speed;
      if (c.y > H + 20) {
        c.y = -20;
        c.speed = 0.35 + Math.random() * 1.0;
        c.brightness = 0.12 + Math.random() * 0.4;
      }
    }
    const cx = W / 2, cy = H * 0.42;
    const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.min(W, H) * 0.4);
    grad.addColorStop(0, 'rgba(0, 0, 0, 0.36)');
    grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);
  }

  let running = true;
  document.addEventListener('visibilitychange', () => { running = !document.hidden; });
  function loop() {
    if (running) draw();
    requestAnimationFrame(loop);
  }
  window.addEventListener('resize', resize);
  resize();
  loop();
})();
