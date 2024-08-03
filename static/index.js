document.getElementById("video-form").addEventListener('submit', function(event) {
    event.preventDefault();
    const url = document.getElementById("url").value;
    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'url=' + encodeURIComponent(url),
    })
    .then(response => {
        if (!response){
            throw new Error('Network response was not ok');   
        }
        return response.blob();
    })
    .then(blob => {
        const videoUrl = URL.createObjectURL(blob);
        const videoPlayer = videojs('video-player');
        videoPlayer.src({ type: 'video/mp4', src: videoUrl });
        videoPlayer.play();
    })
    .catch(error => console.error('Error:', error));
});
