// Get seconds from document and store them as integer values
let timerInterv;
let blinkInterv;
let isPaused = false;

const set_button = document.getElementById('set');
set_button.addEventListener('click', event => {
    
    if (parseInt(document.getElementById("min").value) > 360) {
        document.getElementById("min").value = 360;
    } else if (parseInt(document.getElementById("min").value) < 0) {
        document.getElementById("min").value = 0;
    }

    if (parseInt(document.getElementById("sec").value) > 60) {
        document.getElementById("min").value = 60;
    } else if (parseInt(document.getElementById("sec").value) < 0) {
        document.getElementById("min").value = 0;
    }

    if (parseInt(document.getElementById("min").value) == 0 && parseInt(document.getElementById("sec").value) == 0) {
        return;
    }

    startTimer(parseInt(document.getElementById("sec").value) + (parseInt(document.getElementById("min").value) * 60));
});

function startTimer(totalSeconds) {
    // Timer based on the following tutorial: https://youtu.be/x7WJEmxNlEs

    // Unpause the timer on start if it was paused before
    if (isPaused) {
        isPaused = false;
        pause_button.innerHTML = 'Pause';
    }

    // If another timer interval is already set, clear that interval before starting a new one
    if (timerInterv) {
        clearInterval(timerInterv);
    }

    // If a blink interval is already set, clear that interval before starting the timer
    if (blinkInterv) {
        clearInterval(blinkInterv);
    }

    // Get the element that is going to be changed each second
    const countdownElement = document.getElementById('timer');

    // Set an interval that ticks every second
    timerInterv = setInterval(updateCountdown, 1000);

    // Execute the following code each time the interval ticks
    function updateCountdown() {

        // Check if the countdown is paused
        if(!isPaused) {

            // Resolve totalSeconds back to minutes and seconds
            let minutes = Math.floor(totalSeconds / 60);
            let seconds = totalSeconds % 60;

            // If minutes or seconds have less than two digits, add a leading zero
            minutes = minutes < 10 ? '0' + minutes : minutes; 
            seconds = seconds < 10 ? '0' + seconds : seconds;

            // Update the element
            countdownElement.innerHTML = `${minutes}:${seconds}`;
            
            // Check if totalSeconds is still greater than zero
            if (totalSeconds > 0) {
                totalSeconds--;
            }
            else {
                ding();
                clearInterval(timerInterv);
                return;
            }
        }
    }
}


const pause_button = document.getElementById('pause');
pause_button.addEventListener('click', togglePause, false);

function togglePause() {
    if (!blinkInterv) {
        if (isPaused) {
            isPaused = false;
            pause_button.innerHTML = 'Pause';
        } else {
            isPaused = true;
            pause_button.innerHTML = 'Continue';
        }
    }
}


const preset_buttons = document.getElementsByName('preset');

preset_buttons.forEach(element => {
    element.addEventListener('click', event => {
        startTimer(element.value);
    });
});


function ding() {
    // The file path is relative to the HTML file that executes the script, not to the script itself
    var audio = new Audio('../static/ding.mp3');    
    audio.play();
}
