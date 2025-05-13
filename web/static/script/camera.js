const cv2 = document.getElementById('videoCanvas');
const ctx2 = cv2.getContext('2d');

const img = new Image();
img.src = '/video_feed';


const ERROR_FPS = 10;



img.onload = async function() {
    drawFrame();
};

async function drawFrame() {
    try {
        ctx2.drawImage(img, 0, 0, cv2.width, cv2.height);
    } catch (error) { }
    img.src = '/video_feed?rand=' + Math.random();
}

img.onerror = async function() {
    setTimeout(() => {
        img.src = '/video_feed?rand=' + Math.random();
    }, 1000 / ERROR_FPS);
};
