import numpy as np
from pydub import AudioSegment
# import matplotlib.pyplot as plt
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
    peaks, _ = find_peaks(magnitude, height=np.max(magnitude) * 0.1, distance = 600)
    peak_freqs = f[peaks]
    peak_magnitudes = magnitude[peaks]
    
    # plt.xlim(0, 2000)
    # plt.xlabel('frequency (Hz)')

    # plt.ylabel('|X|/N')
    # plt.plot(f, np.abs(X)/N) # 振幅スペクトル

    # plt.show()
    # plt.savefig("output2.png")
    # plt.close()
    return peak_freqs, peak_magnitudes
    