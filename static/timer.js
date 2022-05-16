// Get seconds from document and store them as integer values
const userSeconds = parseInt(document.getElementById("sec").value) + (parseInt(document.getElementById("min").value) * 60);

let timerInterv;
let isPaused = false;

const set_button = document.getElementById('set');
set_button.addEventListener('click', startTimer(userSeconds), false);

function startTimer(totalSeconds) {
    // Timer based on the following tutorial: https://youtu.be/x7WJEmxNlEs

    // Unpause the timer on start if it was paused before
    if (isPaused) {
        isPaused = false;
        pause_button.innerHTML = 'Pause';
    }

    // If another interval is already set, clear that interval before starting a new one
    if (timerInterv) {
        clearInterval(timerInterv);
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
                // TODO: Play sound? Alert? Flash "00:00" a couple of times?
                alert("totalSeconds'S UP!");
                clearInterval(timerInterv);
                return;
            }
        }
    }
}


const pause_button = document.getElementById('pause');
pause_button.addEventListener('click', togglePause, false);

function togglePause() {
    if (isPaused) {
        isPaused = false;
        pause_button.innerHTML = 'Pause';
    } else {
        isPaused = true;
        pause_button.innerHTML = 'Continue';
    }
}

const preset_buttons = document.getElementsByName('preset');
console.log(preset_buttons);

preset_buttons.forEach(element => {
    element.addEventListener('click', event => {
        if (isPaused) {
            isPaused = false;
            pause_button.innerHTML = 'Pause';
        }

        startTimer(element.value);
    })
})
