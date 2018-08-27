import RPi.GPIO as GPIO
import time
import os
import signal
import subprocess

GPIO.setmode(GPIO.BCM)

PERSON_1_GPIO_PINS = (18, 23,  4, 17)
PERSON_2_GPIO_PINS = (27, 22, 10, 9)
PERSON_3_GPIO_PINS = (11, 5,  6, 13)

person_pids = [None, None, None]

AUDIO_FILENAMES = (
    "gal-gadot.opus.mp3",
    "compilation.opus.mp3",
    "grilling.m4a.mp3",
    "sleep.opus.mp3"
 )

ALL_PERSONS_GPIO_PINS = (
    PERSON_1_GPIO_PINS + PERSON_2_GPIO_PINS + PERSON_3_GPIO_PINS
)


def kill_process(pid):
    """Kills the process with PID `pid` using SIGTERM."""
    if pid is not None:
        print("Killing process with PID: {} ...".format(pid))
        os.killpg(os.getpgid(pid), signal.SIGTERM)


def launch_process(cmd_as_list):
    """Launches a subprocess who is a process group leader.
    Returns: `PID` of the newly launched process

    See: https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true/4791612#4791612"""
    process = subprocess.Popen(cmd_as_list, preexec_fn=os.setsid)
    return process.pid


def get_high_pin_idx_pull_up(pin_input_values):
    """Returns the index of the first high pin value. Assumes Pull UP mode. i.e. a stronger force will pull the pin value down to 0. If no high pins were found, None is returned."""
    high_pin_idx = (
        pin_input_values.index(False) if False in pin_input_values else None
    )
    return high_pin_idx


def handle_persons(person_1_inputs, person_2_inputs, person_3_inputs):
    """Handle GPIO PIN Inputs related the persons listening to ASMR."""
    global person_pids

    person_high_pin_idxs = (
        map(get_high_pin_idx_pull_up,
            (person_1_inputs, person_2_inputs, person_3_inputs)
            )
    )

    for i, v in enumerate(person_high_pin_idxs):
        person_idx = i
        if v is not None:
            kill_process(person_pids[person_idx])
            pid = launch_process([
                    "./play_track.sh",
                    "{}".format(
                            AUDIO_FILENAMES[person_high_pin_idxs[person_idx]]
                        ),
                    person_idx + 1
                ])
            person_pids[person_idx] = pid


if __name__ == "__main__":

    for i in ALL_PERSONS_GPIO_PINS:
        GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while True:
        person_1_inputs = [GPIO.input(i) for i in PERSON_1_GPIO_PINS]
        person_2_inputs = [GPIO.input(i) for i in PERSON_2_GPIO_PINS]
        person_3_inputs = [GPIO.input(i) for i in PERSON_3_GPIO_PINS]

        print(person_1_inputs)
        print(person_2_inputs)
        print(person_3_inputs)
        print("\n\n\n\n")

        handle_persons(person_1_inputs, person_2_inputs, person_3_inputs)

        time.sleep(0.2)
