document.getElementById('fileInput').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (!file) { return; }
    const reader = new FileReader();
    reader.onload = function (e) {
        const content = e.target.result;
        const data = parseCSVToObjects(content);
        initCanvas(data);
    };
    reader.readAsText(file);
});

function parseCSVToObjects(csvText) {
    const lines = csvText.trim().split("\n");
    const headers = lines[0].trim().split(",");

    return lines.slice(1).map(line => {
        const values = line.split(",");
        let obj = {};
        headers.forEach((header, index) => {
            let value = values[index].trim();
            if (value.toLowerCase() === "true" || value.toLowerCase() === "false") {
                value = value.toLowerCase() === "true";
            } else if (!isNaN(value) && value.trim() !== "") {
                value = parseFloat(value);
            }
            obj[header] = value;
        });
        return obj;
    });
}

function getColor(left_button_holding, right_button_holding) {
    if (left_button_holding && right_button_holding) {
        return { r: 255, g: 0, b: 0 };
    } else if (left_button_holding) {
        return { r: 0, g: 0, b: 255 };
    } else if (right_button_holding) {
        return { r: 0, g: 255, b: 0 };
    } else {
        return { r: 32, g: 32, b: 32 };
    }
}

function initCanvas(data) {
    const canvas = document.getElementById('mouseCanvas');
    if (canvas.getContext) {
        const progressBar = document.getElementById('progressBar');
        const customCursor = document.getElementById('customCursor');
        const clearCanvasButton = document.getElementById('clearCanvasButton');
        const progressContainer = document.getElementById('progressContainer');
        const canvasContainer = document.getElementById('canvasContainer');
        canvasContainer.style.display = 'block';

        const ctx = canvas.getContext('2d');
        let animationId = null;
        let isPaused = false;
        let paths = [];
        let currentIndex = 0;
        const totalFrames = data.length;
        const fadeDuration = 1000;
        const { minX, maxX, minY, maxY } = data.reduce((acc, { x, y }) => ({
            minX: Math.min(x, acc.minX),
            maxX: Math.max(x, acc.maxX),
            minY: Math.min(y, acc.minY),
            maxY: Math.max(y, acc.maxY),
        }), { minX: Infinity, maxX: -Infinity, minY: Infinity, maxY: -Infinity });
        const scale = 1.2;
        canvas.width = (maxX - minX) * scale;
        canvas.height = (maxY - minY) * scale;
        canvasContainer.style.width = `${canvas.width}px`;

        function updateProgressBar(currentIndex) {
            progressBar.style.width = `${(currentIndex / totalFrames) * 100}%`;
        }

        function updateCursor(snapshot) {
            customCursor.className = snapshot.left_button_holding && snapshot.right_button_holding ? 'both-click' :
                snapshot.left_button_holding ? 'left-click' :
                    snapshot.right_button_holding ? 'right-click' : '';
        }

        function drawPath(path) {
            const age = performance.now() - path.timestamp;
            const opacity = path.permanent ? 1 : 1 - age / fadeDuration;
            if (opacity < 0) return false;
            ctx.strokeStyle = `rgba(${path.color.r}, ${path.color.g}, ${path.color.b}, ${opacity})`;
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(path.startX, path.startY);
            ctx.lineTo(path.endX, path.endY);
            ctx.stroke();
            return true;
        }

        function animate() {
            if (isPaused) return;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            paths = paths.filter(drawPath);
            if (currentIndex < data.length) {
                const snapshot = data[currentIndex];
                const x = (snapshot.x - minX) * scale;
                const y = canvas.height - (snapshot.y - minY) * scale;
                if (currentIndex > 0) {
                    customCursor.style.left = `${x - 5}px`;
                    customCursor.style.top = `${y - 5}px`;
                    updateCursor(snapshot);
                    const lastSnapshot = data[currentIndex - 1];
                    const lastX = (lastSnapshot.x - minX) * scale;
                    const lastY = canvas.height - (lastSnapshot.y - minY) * scale;
                    const left_button_holding = snapshot.left_button_holding;
                    const right_button_holding = snapshot.right_button_holding;
                    const color = getColor(left_button_holding, right_button_holding);
                    const permanent = left_button_holding || right_button_holding;
                    paths.push({ startX: lastX, startY: lastY, endX: x, endY: y, color, permanent, timestamp: performance.now() });
                }
                currentIndex++;
                updateProgressBar(currentIndex);
            }
            animationId = window.requestAnimationFrame(animate);
        }

        canvas.addEventListener('click', function () {
            isPaused = !isPaused;
            if (isPaused) {
                if (animationId !== null) {
                    cancelAnimationFrame(animationId);
                    animationId = null;
                }
                drawPlayIcon();
            } else {
                animate();
            }
        });

        function drawPlayIcon() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.25)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.beginPath();
            ctx.moveTo(canvas.width / 2 - 30, canvas.height / 2 - 30);
            ctx.lineTo(canvas.width / 2 - 30, canvas.height / 2 + 30);
            ctx.lineTo(canvas.width / 2 + 30, canvas.height / 2);
            ctx.fillStyle = 'white';
            ctx.fill();
        }

        clearCanvasButton.addEventListener('click', () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            if (isPaused) {
                drawPlayIcon();
            }
            paths = [];
        });

        progressContainer.addEventListener('click', function (event) {
            const clickX = event.offsetX;
            const totalWidth = this.offsetWidth;
            const clickedFraction = clickX / totalWidth;

            const newProgress = clickedFraction * totalFrames;
            currentIndex = Math.floor(newProgress);

            if (isPaused) {
                updateProgressBar(currentIndex);
            } else {
                cancelAnimationFrame(animationId);
                animate();
            }
        });

        animationId = window.requestAnimationFrame(animate);
    }
}