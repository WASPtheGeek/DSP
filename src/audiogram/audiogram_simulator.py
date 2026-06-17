import time

import numpy as np

def simulate_patient_response(
    current_volume: float,
    patient_threshold: float, 
    noise_std=2.0
):
    """
    Stimulates a patient response on a sound.
    Use sigmoid function for the response probability calculation.
    """
    diff = current_volume - patient_threshold
    # use the sigmoid for the response probability
    probability = 1 / (1 + np.exp(-diff / noise_std))

    return np.random.rand() < probability

def run_adaptive_audiogram(patient_threshold: float):
    """
    Stimulates a real-world audiogram performing on a patient.
    """

    print(f"Patient threshold is set to {patient_threshold}")
    print(f"Running an adaptive test (by Houson-Westlake)...\n")

    time.sleep(1)

    # Starting with the loud noise
    current_volume = 40.0

    history = []
    threshold_candidates = {}

    step = 1
    max_steps = 20

    while step <= max_steps:
        heard = simulate_patient_response(current_volume, patient_threshold)
        response_str = "🔊 POSITIVE" if heard else "🔇 NEGATIVE"

        print(f"Step {step:02d}: Volume at {current_volume:5.1f} dB SPL ---> Response: {response_str}")

        if heard:
            if step > 1 and not history[-1]["heard"]:
                # uprising "heard"
                threshold_candidates[current_volume] = threshold_candidates.get(current_volume, 0) + 1

                # 2 times positive, uprising
                if threshold_candidates[current_volume] == 2:
                    print(f"Test finished with stimulating patient's threshold {patient_threshold}!")
                    print(f"The hearing threshold is: {current_volume} db SPL")
                    print(f"Error: {abs(current_volume - patient_threshold):.1f} db SPL")

                    return
                
            history.append({'vol': current_volume, 'heard': True})
            current_volume -= 10
        else:
            history.append({'vol': current_volume, 'heard': False})
            current_volume += 5

        step += 1
        time.sleep(0.4)


if __name__ == "__main__":
    run_adaptive_audiogram(17.5)