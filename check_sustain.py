import numpy as np
# from pydub import AudioSegment

def get_db_at_time(samples, sample_rate, time_seconds, max_db):
    """
    指定された時間における音量(dBFS)を計算します。

    Args:
        samples (array): 音声サンプルデータ (array.array 型)
        sample_rate (int): サンプリングレート
        time_seconds (float): 時間（秒）
        max_db (float): 音声全体の最大音量(dBFS)

    Returns:
        float: 指定時間の音量(dBFS) または None
    """
    # array.array を NumPy 配列に変換
    samples = np.array(samples)

    start_index = int(time_seconds * sample_rate)
    end_index = min(start_index + sample_rate, len(samples))  # 1秒分のサンプルを使用
    segment = samples[start_index:end_index]
    
    if len(segment) == 0:
        return None  # データが存在しない場合
    
    # サンプルデータの正規化（例: 16ビットPCMの場合）
    segment = segment.astype(np.float32) / np.max(np.abs(samples))
    
    # RMS値を計算
    rms = np.sqrt(np.mean(segment ** 2))
    if rms == 0 or np.isnan(rms):
        return -float('inf')  # 無音または異常値の場合は -∞ を返す
    
    return max_db - 20 * np.log10(rms)  # 最大音量との差を計算


# def main():
#     # ギターのWAVファイルを読み込む
#     sound = AudioSegment.from_wav("./data/processed/FENDER_STRAT/ST_CENTER/ST_CENTER_6.wav")
#     samples = sound.get_array_of_samples()  # array.array 型
#     sample_rate = sound.frame_rate  # サンプリングレート
    
#     # 最大音量（dBFS）
#     max_db = sound.max_dBFS
#     print(f"最大音量: {max_db:.2f} dBFS")
    
#     # 3秒後の音量（dBFS）
#     time_after_3_seconds = 3.0
#     db_at_3_seconds = get_db_at_time(samples, sample_rate, time_after_3_seconds, max_db)
    
#     print(db_at_3_seconds)

# if __name__ == '__main__':
#     main()
