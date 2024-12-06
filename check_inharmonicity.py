import numpy as np
from scipy.signal import find_peaks, butter, filtfilt

def get_overtone(samples, frame_rate, end_time): 
    sig = samples
    times = np.linspace(0, len(samples) / frame_rate, num=len(samples))

    dt = 1.0/frame_rate
    
    tms = 0.0 # サンプル開始時間を0にセット
    tme = end_time # サンプル終了時刻
    tm = np.linspace(tms, tme, len(sig), endpoint=False)
    
    N = len(sig)
    X = np.fft.fft(sig)
    f = np.fft.fftfreq(N, dt)

    # ピークの高さが最大値の10%を超える周波数をピーク
    # distance調整いるかも
    magnitude = np.abs(X[0:N//2])
    peaks, _ = find_peaks(magnitude, height=np.max(magnitude) * 0.1, distance=600)
    peak_freqs = f[peaks]
    
    standard = peak_freqs[1] / 2
    rate = np.zeros(len(peak_freqs) - 2)
    
    for i in range(2, len(peak_freqs)):
        k = round(peak_freqs[i] / standard)
        normal_f = k * standard
        rate[i - 2] = peak_freqs[i] / normal_f - 1
        rate[i - 2] *= 100
    
    return rate