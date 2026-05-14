/* Aetherneum hero canvas — code-rain particles + faint hooded silhouette echo.
   Performance: capped DPR, pause when tab hidden. */
(function () {
    const canvas = document.getElementById('hero-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let W = 0, H = 0;
    const DPR = Math.min(window.devicePixelRatio || 1, 2);
    let cols = [];
    const FONT_SIZE = 14;
    const CHARS = '0123456789ABCDEF·∴⋄◇◆▪▫░▒▓ÆÆØΩæþƎ⌬⎔⏣';

    function resize() {
        W = window.innerWidth;
        H = window.innerHeight;
        canvas.width = W * DPR;
        canvas.height = H * DPR;
        canvas.style.width = W + 'px';
        canvas.style.height = H + 'px';
        ctx.scale(DPR, DPR);
        ctx.font = FONT_SIZE + 'px JetBrains Mono, monospace';
        const colCount = Math.floor(W / FONT_SIZE);
        cols = new Array(colCount).fill(0).map(() => ({
            y: Math.random() * H,
            speed: 0.4 + Math.random() * 1.2,
            brightness: 0.12 + Math.random() * 0.45,
            lastChar: CHARS[Math.floor(Math.random() * CHARS.length)],
            changeRate: 0.05 + Math.random() * 0.08,
        }));
    }

    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.08)';
        ctx.fillRect(0, 0, W, H);

        for (let i = 0; i < cols.length; i++) {
            const c = cols[i];
            const x = i * FONT_SIZE;
            if (Math.random() < c.changeRate) {
                c.lastChar = CHARS[Math.floor(Math.random() * CHARS.length)];
            }
            ctx.fillStyle = 'rgba(103, 232, 249, ' + c.brightness + ')';
            ctx.fillText(c.lastChar, x, c.y);
            ctx.fillStyle = 'rgba(34, 211, 238, ' + (c.brightness * 0.35) + ')';
            ctx.fillText(c.lastChar, x, c.y - FONT_SIZE);
            c.y += c.speed;
            if (c.y > H + 20) {
                c.y = -20;
                c.speed = 0.4 + Math.random() * 1.2;
                c.brightness = 0.12 + Math.random() * 0.45;
            }
        }

        /* Faint hooded silhouette: a soft radial dim at the upper-center */
        const cx = W / 2;
        const cy = H * 0.42;
        const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.min(W, H) * 0.35);
        grad.addColorStop(0, 'rgba(0, 0, 0, 0.42)');
        grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, W, H);
    }

    let running = true;
    function loop() {
        if (running) draw();
        requestAnimationFrame(loop);
    }

    document.addEventListener('visibilitychange', () => {
        running = !document.hidden;
    });

    window.addEventListener('resize', resize);
    resize();
    loop();
})();
