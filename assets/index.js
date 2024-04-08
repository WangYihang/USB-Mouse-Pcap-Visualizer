document.addEventListener('DOMContentLoaded', function () {
    loadCSVFile();
});

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

function loadCSVFile() {
    fetch('/example/XNUCA/data.csv')
        .then(response => response.text())
        .then(csvText => {
            const data = parseCSVToObjects(csvText);
            initCanvas(data);
        })
        .catch(error => console.error('Error loading CSV file:', error));
}

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
        let playbackSpeed = 1;

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

        const screenWidth = window.innerWidth;
        const canvasWidth = screenWidth * 0.6;
        const originalWidth = maxX - minX;
        const originalHeight = maxY - minY;
        const aspectRatio = originalHeight / originalWidth;
        canvas.width = canvasWidth;
        canvas.height = canvasWidth * aspectRatio;
        canvasContainer.style.width = `${canvas.width}px`;
    
        const scaleX = canvas.width / originalWidth * 0.8;
        const scaleY = canvas.height / originalHeight * 0.8;

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

        function formatTimestamp(timestamp) {
            var date = new Date(timestamp);
            var formattedDate = date.toLocaleDateString("en-US");
            var formattedTime = date.toLocaleTimeString("en-US");
            return formattedDate + ' ' + formattedTime;
        }

        function drawInfo(snapshot) {
            ctx.fillStyle = 'black';
            ctx.font = '16px Arial';
            ctx.fillText(`Speed: x${playbackSpeed}`, 10, 20);
            ctx.fillText(`Frame: ${currentIndex} / ${totalFrames}`, 10, 40);
            ctx.fillText(`Time: ${formatTimestamp(snapshot.timestamp *1000)}`, 10, 60);
            ctx.fillText(`X: ${snapshot.x}`, 10, 80);
            ctx.fillText(`Y: ${snapshot.y}`, 10, 100);
            ctx.fillText(`Left button: ${snapshot.left_button_holding}`, 10, 120);
            ctx.fillText(`Right button: ${snapshot.right_button_holding}`, 10, 140);
        }

        function animate() {
            if (isPaused) return;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            paths = paths.filter(drawPath);
            if (currentIndex < data.length) {
                const snapshot = data[currentIndex];
                const x = (snapshot.x - minX) * scaleX;
                const y = canvas.height - (snapshot.y - minY) * scaleY;
    
                if (currentIndex > 0) {
                    customCursor.style.left = `${x - 5}px`;
                    customCursor.style.top = `${y - 5}px`;
                    updateCursor(snapshot);
                    const lastSnapshot = data[currentIndex - 1];
                    const lastX = (lastSnapshot.x - minX) * scaleX;
                    const lastY = canvas.height - (lastSnapshot.y - minY) * scaleY;
                    const left_button_holding = snapshot.left_button_holding;
                    const right_button_holding = snapshot.right_button_holding;
                    const color = getColor(left_button_holding, right_button_holding);
                    const permanent = left_button_holding || right_button_holding;
                    paths.push({ startX: lastX, startY: lastY, endX: x, endY: y, color, permanent, timestamp: performance.now() });
                }

                currentIndex += playbackSpeed;
                currentIndex = Math.min(currentIndex, data.length);

                updateProgressBar(currentIndex);
             drawInfo(snapshot);
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

        function handleKeyboardEvent(event) {
            const frameStep = 64;
            if (event.keyCode === 37) {
                currentIndex = Math.max(currentIndex - frameStep, 0);
            } else if (event.keyCode === 39) {
                currentIndex = Math.min(currentIndex + frameStep, totalFrames - 1);
                   } else if (event.keyCode === 38) { 
                playbackSpeed = Math.min(playbackSpeed + 1, 10); 
            } else if (event.keyCode === 40) { 
                playbackSpeed = Math.max(playbackSpeed - 1, 1); 
            }
            if (isPaused) {
                updateProgressBar(currentIndex);
            } else {
                cancelAnimationFrame(animationId);
                animate();
            }
        }
    
        window.addEventListener('keydown', handleKeyboardEvent);
    

        animationId = window.requestAnimationFrame(animate);
    }
}
