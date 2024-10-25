import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def processed_file():
    # 元のフォルダのパス
    original_folder_path = './data/original'
    # 処理したファイルを保存するフォルダパス
    processed_folder_path = './data/processed'

    # 処理したファイルを保存するフォルダが存在しない場合は作成
    if not os.path.exists(processed_folder_path):
        os.makedirs(processed_folder_path)

    for root, dirs, files in os.walk(original_folder_path):
        # 新しいフォルダのパスを再現
        relative_path = os.path.relpath(root, original_folder_path)
        new_folder_path = os.path.join(processed_folder_path, relative_path)

        # 新しいフォルダが存在しない場合は作成
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            
            for filename in files:
                if filename.endswith('.wav'):
                    original_file_path = os.path.join(root, filename)
                    # print(f"Processing file: {original_file_path}")

                    # 音声ファイルを読み込み
                    sound = AudioSegment.from_wav(original_file_path)
                    
                    # 無音部分の検出
                    nonsilent_ranges = detect_nonsilent(sound, min_silence_len=100, silence_thresh=sound.dBFS-16)
                    
                    if nonsilent_ranges:
                        # トリミング位置を決定
                        start_trim = nonsilent_ranges[0][0]
                        trimmed_sound = sound[start_trim:]

                        # 加工後のファイルの保存先パスを設定
                        processed_file_path = os.path.join(new_folder_path, filename)
                        
                        # 加工後のファイルを保存
                        trimmed_sound.export(processed_file_path, format="wav")
                        # print(f"Processed file saved to: {processed_file_path}")
                else:
                    print(f"No significant sound found in file: {original_file_path}")
