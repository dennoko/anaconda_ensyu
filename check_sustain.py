import numpy as np
from pydub import AudioSegment

# ピークから-40dB小さくなるまでの時間
def get_sustain(samples, sample_rate, max_db, threshold_db=-40):
    max_amplitude = 2147483647
    threshold_amplitude = max_amplitude * 10 ** ((threshold_db + max_db) / 20)
    end_index = len(samples)
    for i in range(len(samples)- 1, -1, -1):
        if np.abs(samples[i]) > threshold_amplitude:
            end_index = i
            break
    
    end_time_seconds = end_index / sample_rate

    return end_time_seconds
