import numpy as np
import re
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq, ifft
from pydub import AudioSegment
import matplotlib.pyplot as plt

def get_wave_sexcept_overtone(samples, frame_rate, string_num, octave):
    # 窓幅と刻みの設定
    # window_size = len(sample)
    # step_size = len(sample)
    window_size = 2000
    step_size = 2000
    
    output_wave = []
   
    # 窓をずらしながらフーリエ変換を実行
    if window_size == len(samples):
        num = 1
    else:
        num = len(samples) - window_size
    
    # samples = sample/np.max(sample)
    
    for start in range(0, num, step_size):
        segment = samples[start:start + window_size]
        N = len(segment)
        frequencies = fftfreq(N, 1 / frame_rate)
        spectrum = fft(segment)
        
        spectrum_magnitude = np.abs(spectrum)
        
        base = extract_string_base_freq(string_num[0])
        if octave == True:
            base *= 2
        peaks, _ = find_peaks(spectrum_magnitude, height=0.05*np.max(spectrum_magnitude), distance = base//frequencies[1]) 
        peak_freqs = frequencies[peaks]
        peak_spectrum = spectrum[peaks]
        if start == 0:
            print(base)
            print(peak_freqs)
        # 倍音のみのスペクトルに再構築
        reconstructed_spectrum = np.zeros_like(spectrum, dtype=complex)
        for j in range(0, len(peaks)):
            idx = peaks[j]
            reconstructed_spectrum[idx] = peak_spectrum[j]
        # 波形を再構築
        reconstructed_segment = np.real(ifft(reconstructed_spectrum))
        output_wave.extend(reconstructed_segment)
    
    return output_wave

# ギターの基準の基本周波数
def extract_string_base_freq(string_num):
    if string_num == 1:
        base_freq = 329.628
    elif string_num == 2:
        base_freq = 246.0942
    elif string_num == 3:
        base_freq = 195.998
    elif string_num == 4:
        base_freq = 146.832
    elif string_num == 5:
        base_freq = 110.0
    else:
        base_freq = 82.407
    return base_freq

# ギターの倍音か確認(使ってない)
def filter_get_overtone(string_num, peak_freq):
    base_freq = extract_string_base_freq(string_num)
    overtone_idx = []
    overtone_num = 1
    for i in range(0, len(peak_freq)):
        if abs(base_freq * overtone_num - peak_freq[i]) < 10:
            overtone_idx.append(i)
            overtone_num += 1
    return overtone_idx

# 元の波形と再構築した波形の差を出力
def get_difference(samples, frame_rate, string_num, octave):
    reconstructed_wave = get_wave_sexcept_overtone(samples, frame_rate, string_num, octave)
    original_wave = np.abs(samples[0:len(reconstructed_wave)])
    difference_wave = np.abs(original_wave - np.abs(reconstructed_wave))
    
    rate_diff = np.sum(difference_wave) / np.sum(original_wave)
    return rate_diff * 100

if __name__ == '__main__':
    # ギターのWAVファイルを読み込む
    file_name = "./data/processed/ST32_CENTER/ST_CENTER_12_2.wav"
    sound = AudioSegment.from_wav(file_name)
    samples = np.array(sound.get_array_of_samples())
    sample_rate = sound.frame_rate # サンプリングレート

    extension = ".wav"
    string_num = []
    base_name = file_name[:-len(extension)]
    if base_name[-1].isdigit():
        string_num.append(int(base_name[-1]))
        
    match = re.search(r'(\d+)_\d+$', base_name)
    octave = False
    if match:
        octave = True
    # if 
    print(octave)

    #音量エンベロープをプロット
    print(get_difference(samples, sample_rate, string_num, octave))