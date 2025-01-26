# プログラムのメイン関数
import os
from pydub import AudioSegment

# 関数のインポート
from processed_file import processed_file
from check_volume import get_db

def main():
    # データの前処理
    processed_file()

    # 整形済みデータに対する処理
    processed_folder_path = './data/processed'
    for root, dirs, files in os.walk(processed_folder_path):
        for filename in files:
                if filename.endswith('.wav'):
                    processed_file_path = os.path.join(root, filename)
                    
                    sound = AudioSegment.from_wav(processed_file_path)
                    samples = sound.get_array_of_samples()
                    
                    # 音量測定
                    print(get_db(samples))
    
    
if __name__ == '__main__':
    main()