let startTime = {{ session.get('start_time', 0)|float }};
let timeLeft = {{ time_left }};

function updateTimer() {
    let currentTime = new Date().getTime();
    let elapsedTime = Math.floor((currentTime / 1000) - startTime);
    timeLeft = Math.max(0, 600 - elapsedTime);

    let minutes = Math.floor(timeLeft / 60);
    let seconds = timeLeft % 60;

    document.getElementById("timer").textContent = `Time Left: ${minutes}:${seconds.toString().padStart(2, '0')}`;

    if (timeLeft <= 0) {
        clearInterval(timerInterval);
        window.location.href = "/result";
    }
}

updateTimer();
let timerInterval = setInterval(updateTimer, 1000);