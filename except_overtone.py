import numpy as np
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq, ifft
from pydub import AudioSegment

def get_wave_sexcept_overtone(samples, frame_rate):
    # 窓幅と刻みの設定
    # window_size = len(samples)
    # step_size = len(samples)
    window_size = 500
    step_size = 500
    
    output_wave = []
   
    # 窓をずらしながらフーリエ変換を実行
    if window_size == len(samples):
        num = 1
    else:
        num = len(samples) - window_size
        print(num)
        
    for start in range(0, num, step_size):
        segment = samples[start:start + window_size]
        N = len(segment)
        frequencies = fftfreq(N, 1 / frame_rate)
        spectrum = fft(segment)

        peaks_p, _ = find_peaks(spectrum, height=np.max(spectrum) * 0.1) 
        peaks_n, _ = find_peaks(-spectrum, height=np.max(spectrum) * 0.1)
        peak_freqs_p = frequencies[peaks_p]
        peak_freqs_n = frequencies[peaks_n]
        peak_magnitudes_p = spectrum[peaks_p]
        peak_magnitudes_n = spectrum[peaks_n]

        reconstructed_spectrum = np.zeros_like(spectrum, dtype=complex)

        for j in range(0, len(peaks_p)):
            idx = peaks_p[j]
            reconstructed_spectrum[idx] = peak_magnitudes_p[j]
            
        for j in range(0, len(peaks_n)):
            idx = peaks_n[j]
            reconstructed_spectrum[idx] = peak_magnitudes_n[j]
        
        reconstructed_segment = np.real(ifft(reconstructed_spectrum))
            
        output_wave.extend(reconstructed_segment)
        return output_wave
    
def get_difference(samples, frame_rate):
    reconstructed_wave = get_wave_sexcept_overtone(samples, frame_rate)
    original_wave = samples[0:len(reconstructed_wave)]
    difference_wave = np.abs(original_wave) - np.abs(reconstructed_wave)
    difference = np.sum(difference_wave)
    
    rate_diff = np.sum(difference_wave) / np.sum(original_wave)
    return rate_diff * 100