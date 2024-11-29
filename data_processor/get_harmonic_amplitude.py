# 音の倍音成分の大きさをdbで返す関数
# 引数: 音の波形データ: list, 基本周波数: float
# 返り値: 音の倍音成分の大きさ db
import numpy as np
import math

def get_harmonic_amplitude(sound: list, base_frequency: float) -> float:
    # フーリエ変換で周波数成分を取得
    n = len(sound)
    fft_result = np.fft.fft(sound)
    fft_magnitude = np.abs(fft_result)[:n//2] / n
    freps = np.fft.fftfreq(n, d=1.0/44100)[:n//2]

    # 倍音の周波数リストを作成
    harmonics = {}
    harmonic_num = 1
    harmonic_freq = base_frequency * harmonic_num

    # 倍音の周波数が22050Hzを超えるまで繰り返す 
    while harmonic_freq < 22050:
        # 倍音周波数に最も近いFFT周波数を取得
        closest_freq = np.argmin(np.abs(freps - harmonic_freq))
        # 信号は32bitでサンプリングされているので、正の振幅は2の31乗マイナス1
        max_32bit = 2**31 - 1
        magnitude_db = 20 * math.log10(fft_magnitude[closest_freq] / max_32bit)
        harmonics[harmonic_freq] = magnitude_db

        # 次の倍音周波数を計算
        harmonic_num += 1
        harmonic_freq = base_frequency * harmonic_num
    
    return harmonics
