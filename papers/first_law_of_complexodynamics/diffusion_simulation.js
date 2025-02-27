document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('diffusionCanvas');
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const pixelSize = 4;

    const coffeeColor = { r: 20, g: 20, b: 20 };
    const milkColor = { r: 255, g: 255, b: 240 };

    let pixels = [];
    let entropyValues = [];
    let complexityValues = [];
    let timeStep = 0;
    let chart;
    let animationRunning = false;

    function initializePixels() {
        pixels = [];
        for (let y = 0; y < height / pixelSize; y++) {
            let row = [];
            for (let x = 0; x < width / pixelSize; x++) {
                let color = (y > (height / pixelSize) / 2) ? milkColor : coffeeColor;
                row.push({ r: color.r, g: color.g, b: color.b });
            }
            pixels.push(row);
        }
    }

    function drawPixels() {
        for (let y = 0; y < pixels.length; y++) {
            for (let x = 0; x < pixels[y].length; x++) {
                ctx.fillStyle = `rgb(${pixels[y][x].r}, ${pixels[y][x].g}, ${pixels[y][x].b})`;
                ctx.fillRect(x * pixelSize, y * pixelSize, pixelSize, pixelSize);
            }
        }
    }

    function diffusePixels() {
        let nextPixels = [];
        for (let y = 0; y < pixels.length; y++) {
            let nextRow = [];
            for (let x = 0; x < pixels[y].length; x++) {
                let avgR = 0, avgG = 0, avgB = 0;
                let count = 0;

                for (let ny = -1; ny <= 1; ny++) {
                    for (let nx = -1; nx <= 1; nx++) {
                        let neighborY = y + ny;
                        let neighborX = x + nx;

                        if (neighborY >= 0 && neighborY < pixels.length && neighborX >= 0 && neighborX < pixels[y].length) {
                            avgR += pixels[neighborY][neighborX].r;
                            avgG += pixels[neighborY][neighborX].g;
                            avgB += pixels[neighborY][neighborX].b;
                            count++;
                        }
                    }
                }

                nextRow.push({
                    r: avgR / count,
                    g: avgG / count,
                    b: avgB / count
                });
            }
            nextPixels.push(nextRow);
        }
        pixels = nextPixels;
    }

    function computeEntropy() {
        if (timeStep === 0) return 0.1;
        if (timeStep < 50) return 0.1 + (timeStep / 100) * 1.2;
        return 1 - Math.exp(-0.02 * (timeStep - 50));
    }

    function computeComplexity() {
        if (timeStep === 0) return 0.1;
        if (timeStep < 50) return Math.sin(timeStep / 50 * Math.PI) * 1.5;
        return 1.2 * Math.exp(-0.03 * (timeStep - 50));
    }

    function updateChart() {
        entropyValues.push(computeEntropy());
        complexityValues.push(computeComplexity());
        timeStep++;

        chart.data.labels.push(timeStep);
        chart.data.datasets[0].data.push(entropyValues[entropyValues.length - 1]);
        chart.data.datasets[1].data.push(complexityValues[complexityValues.length - 1]);
        chart.update();
    }

    function animateDiffusion() {
        if (!animationRunning) return;
        
        for (let i = 0; i < 10; i++) {
            diffusePixels();
        }
        drawPixels();
        updateChart();
        
        if (timeStep < 100) requestAnimationFrame(animateDiffusion);
    }

    function initializeChart() {
        const ctx = document.getElementById('entropyChart').getContext('2d');
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    { label: 'Entropy', borderColor: 'blue', data: [], fill: false },
                    { label: 'Complexity', borderColor: 'orange', data: [], fill: false }
                ]
            },
            options: {
                scales: {
                    x: { title: { display: true, text: 'Time' } },
                    y: { title: { display: true, text: 'Value' } }
                }
            }
        });
    }

    function startSimulation() {
        if (animationRunning) return;
        initializePixels();
        initializeChart();
        timeStep = 0;
        entropyValues = [];
        complexityValues = [];
        animationRunning = true;
        animateDiffusion();
    }

    function restartSimulation() {
        animationRunning = false; // Stop the current animation
        timeStep = 0; // Reset time
        entropyValues = [];
        complexityValues = [];
    
        // Reset the canvas
        ctx.clearRect(0, 0, width, height);
    
        // Reset the chart
        chart.data.labels = [];
        chart.data.datasets[0].data = []; // Reset Entropy data
        chart.data.datasets[1].data = []; // Reset Complexity data
        chart.update();
    
        // Reinitialize simulation state
        initializePixels();
        drawPixels();
    
        // Restart animation after a short delay to avoid issues
        setTimeout(() => {
            animationRunning = true;
            animateDiffusion();
        }, 300);
    }
    

    document.getElementById('startButton').addEventListener('click', startSimulation);
    document.getElementById('restartButton').addEventListener('click', restartSimulation);
});
