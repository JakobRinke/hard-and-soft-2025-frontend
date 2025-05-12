const cv2 = document.getElementById('videoCanvas');
const ctx2 = cv2.getContext('2d');

const img = new Image();
img.src = '/video_feed';

img.onload = function() {
    drawFrame();
};

function drawFrame() {
    ctx2.drawImage(img, 0, 0, canvas.width, canvas.height);
    // Loop by creating a new image object each time
    img.src = '/video_feed?rand=' + Math.random(); // Prevent caching
}

img.onerror = function() {
    console.error("Error loading frame, retrying...");
    setTimeout(() => {
        img.src = '/video_feed?rand=' + Math.random();
    }, 100);
};