from pydub import AudioSegment
import numpy as np
import math

def get_db(samples): 
    peak_volume = max(samples)
    # 16ビットPCMの最大値
    max_amplitude = 32767
    peak_db = 20 * math.log10(abs(peak_volume) / max_amplitude)
    return peak_db
