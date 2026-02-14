import time


def smooth_transition(engine, target_temp, duration, steps=20):
    """
    Smoothly transitions the display to the target temperature over a given duration.
    The transition is done in steps, with each step lasting for a fraction of the total duration.
    """
    current_temp = engine.current_temp
    step_duration = duration / steps
    temp_diff = target_temp - current_temp
    temp_step = temp_diff / steps

    for _ in range(steps):
        current_temp += temp_step
        engine.set_temperature(current_temp)
        time.sleep(step_duration)

    engine.set_temperature(target_temp)
