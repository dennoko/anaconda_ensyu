# 音の倍音成分の大きさをdbで返す関数
# 引数: 音の波形データ: list, 基本周波数: float
# 返り値: 音の倍音成分の大きさ db
import numpy as np

def get_harmonic_amplitude(sound: list, base_frequency: float) -> float:
    # フーリエ変換で周波数成分を取得
    n = len(sound)
    fft_result = np.fft.fft(sound)
    fft_magnitude = np.abs(fft_result)
    freps = np.fft.fftfreq(n, d=1.0/44100)[:n//2]

    # 倍音の周波数リストを作成
    harmonics = {}
    harmonic_num = 1
    harmonic_freq = base_frequency * harmonic_num

    # 可聴域内の倍音成分を取得
    while harmonic_freq < 20000:
        # 倍音周波数に最も近いFFT周波数を取得
        closest_freq = np.argmin(np.abs(freps - harmonic_freq))
        # 振幅をdbで取得
        magnitude_db = 20 * np.log10(fft_magnitude[closest_freq] + 1e-10) # 0割りを防ぐために微小値を足す
        harmonics[harmonic_freq] = magnitude_db

        # 次の倍音周波数を計算
        harmonic_num += 1
        harmonic_freq = base_frequency * harmonic_num

    return harmonics