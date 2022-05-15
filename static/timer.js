const set_button = document.getElementById('set');
set_button.addEventListener('click', timer, false);


const pause_button = document.getElementById('pause');
pause_button.addEventListener('click', togglePause, false);


let timerInterv;
let isPaused = false;


function timer() {
    // Timer based on the following tutorial: https://youtu.be/x7WJEmxNlEs

    // If another interval is already set, clear that interval before starting a new one
    if (timerInterv) {
        clearInterval(timerInterv);
    }

    // Get minutes and seconds from document and store them as integer values
    const userMinutes = parseInt(document.getElementById("min").value);
    const userSeconds = parseInt(document.getElementById("sec").value);

    // Calculate total time in seconds
    let time = (userMinutes * 60) + userSeconds;

    // Get the element that is going to be changed each second
    const countdownElement = document.getElementById('timer');

    // Set an interval that ticks every second
    timerInterv = setInterval(updateCountdown, 1000);

    // Execute the following code each time the interval ticks
    function updateCountdown() {

        // Check if the countdown is paused
        if(!isPaused) {

            // Resolve total time back to minutes and seconds
            let minutes = Math.floor(time / 60);
            let seconds = time % 60;

            // If minutes or seconds have less than two digits, add a leading zero
            minutes = minutes < 10 ? '0' + minutes : minutes; 
            seconds = seconds < 10 ? '0' + seconds : seconds;

            // Update the element
            countdownElement.innerHTML = `${minutes}:${seconds}`;
            
            // Check if time is still greater than zero
            if (time > 0) {
                time--;
            }
            else {
                // TODO: Play sound? Alert? Flash "00:00" a couple of times?
                alert("TIME'S UP!");
                clearInterval(timerInterv);
                return;
            }
        }
    }
}


function togglePause() {
    if (isPaused) {
        isPaused = false;
        pause_button.innerHTML = 'Pause';
    } else {
        isPaused = true;
        pause_button.innerHTML = 'Continue';
    }
}