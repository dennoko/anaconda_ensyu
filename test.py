# 関数等のテスト用のファイル
# 書き方は適当で良い

from data_processor.get_harmonic_amplitude import get_harmonic_amplitude
import os
from pydub import AudioSegment
import numpy as np

# 音声データを data/processed/GIBSON_SG_SPETIAL/SG_SPETIAL_CENTERから取得
# フォルダのパス
data_path = "data/original_32bit/ST32/ST32_CENTER"
print("test.py: " + data_path)
# フォルダ内の各ファイルでループを回す
for root, dirs, files in os.walk(data_path):
    for filename in files:
        # ファイルのパス
        file_path = os.path.join(root, filename)
        # ファイルネームの末尾の文字列に応じて基本周波数を設定
        base_frequency = 440
        if "_12_1" in filename:
            base_frequency = 329.628 * 2
        elif "_12_2" in filename:
            base_frequency = 246.942 * 2
        elif "_12_3" in filename:
            base_frequency = 195.998 * 2
        elif "_12_4" in filename:
            base_frequency = 146.832 * 2
        elif "_12_5" in filename:
            base_frequency = 110.000 * 2
        elif "_12_6" in filename:
            base_frequency = 82.407 * 2
        elif "_1" in filename:
            base_frequency = 329.628
        elif "_2" in filename:
            base_frequency = 246.942
        elif "_3" in filename:
            base_frequency = 195.998
        elif "_4" in filename:
            base_frequency = 146.832
        elif "_5" in filename:
            base_frequency = 110.000
        elif "_6" in filename:
            base_frequency = 82.407

        # 音声ファイルを読み込み
        sound_file = AudioSegment.from_wav(file_path)
        # 音声データをリストに変換
        sound = sound_file.get_array_of_samples()
        # 音の倍音成分の大きさをdbで取得
        harmonics = get_harmonic_amplitude(sound, base_frequency)
        print(harmonics)
        break
    break