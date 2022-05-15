// Based on the following tutorial: https://youtu.be/x7WJEmxNlEs

const startingMinutes = 10;
let time = startingMinutes * 60;

const countdownEl = document.getElementById('timer');

setInterval(updateCountdown, 1000);

function updateCountdown() {
    let minutes = Math.floor(time / 60);
    let seconds = time % 60;

    seconds = seconds < 10 ? '0' + seconds : seconds; 
    minutes = minutes < 10 ? '0' + minutes : minutes; 

    countdownEl.innerHTML = `${minutes}:${seconds}`;
    
    if (time > 0) {
        time--;
    }
    else {
        // TODO: Play sound? Alert?
        alert("TIME'S UP!");
    }
}