import numpy as np
from pydub import AudioSegment

# ピークになるまでにかかる時間
def get_attack_time(samples, sample_rate):
    peak_volume = max(np.abs(samples))
    end_index = 0
    for i in range(0, len(samples)):
        if np.abs(samples[i]) == peak_volume:
            end_index = i
            break
            
    end_time_seconds = end_index / sample_rate

    return end_time_seconds

