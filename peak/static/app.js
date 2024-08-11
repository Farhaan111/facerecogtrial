async function onOpenCVReady() {
    // Load models
    await faceapi.nets.tinyFaceDetector.loadFromUri('/static/weights');
    await faceapi.nets.faceLandmark68Net.loadFromUri('/static/weights');
    await faceapi.nets.faceRecognitionNet.loadFromUri('/static/weights');

    // Set up video
    const video = document.getElementById('videoInput');
    const canvas = document.getElementById('canvasOutput');
    const ctx = canvas.getContext('2d');

    // Set up camera
    const stream = await navigator.mediaDevices.getUserMedia({ video: {} });
    video.srcObject = stream;
    await new Promise(resolve => video.onloadedmetadata = resolve);

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    video.addEventListener('play', () => {
        setInterval(async () => {
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks();
            
            faceapi.draw.drawDetections(canvas, detections);
            faceapi.draw.drawFaceLandmarks(canvas, detections);
        }, 100);
    });
}

window.onload = onOpenCVReady;
