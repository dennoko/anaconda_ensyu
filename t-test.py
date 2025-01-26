import os
import shutil
import time
import json
from main import process_audio_files

def monitor_and_process_files(source_dir, target_root_dir, json_file, interval=5):
    """
    指定されたディレクトリを監視し、ファイルが見つかった場合に別のフォルダに移動して処理を実行します。

    Args:
        source_dir (str): 監視するディレクトリのパス
        target_root_dir (str): ファイルを移動する先のルートディレクトリのパス
        interval (int): チェック間隔（秒）
    """
    if not os.path.exists(source_dir):
        print(f"エラー: ソースディレクトリが存在しません: {source_dir}")
        return

    if not os.path.exists(target_root_dir):
        os.makedirs(target_root_dir)
        print(f"ターゲットルートディレクトリを作成しました: {target_root_dir}")

    print(f"監視を開始します: {source_dir}")
    while True:
        # ソースディレクトリ内のファイルを取得
        files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

        if files:
            for file_name in files:
                source_path = os.path.join(source_dir, file_name)

                # ファイル名から情報を解析
                parts = file_name.split('_')
                file_num = next((len(parts) - 1 - i for i in range(len(parts)) if not parts[len(parts) - 1 - i].isdigit()), 0)

                if file_num <= 1:
                    print(f"無効なファイル名形式: {file_name}")
                    continue

                # ギター名とピックアップ名を取得
                guitar_name_parts = parts[:(file_num - 2)]
                pick_up_parts = parts[:(file_num - 1)]

                # パーツを結合して不要な '_' を防ぐ
                guitar_name = "_".join(filter(None, guitar_name_parts))
                pick_up = "_".join(filter(None, pick_up_parts))

                dir_path = os.path.join(target_root_dir, guitar_name, pick_up)

                # 必要なディレクトリを作成
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                    print(f"ターゲットディレクトリを作成しました: {dir_path}")

                # ファイルを移動
                target_path = os.path.join(dir_path, file_name)
                shutil.move(source_path, target_path)
                print(f"ファイルを移動しました: {source_path} → {target_path}")

                # ファイル処理を呼び出す
            write_directory_to_json(target_root_dir, json_file)
            process_audio_files(dir_path, "./output")

        # 指定された間隔だけ待機
        time.sleep(interval)

def write_directory_to_json(directory, json_file):
    """
    指定されたディレクトリ内の各ファイルが格納されている1つ前のディレクトリ名をJSON形式で保存します。

    Args:
        directory (str): ファイルを探索するディレクトリ
        json_file (str): 保存するJSONファイルのパス
    """
    parent_dirs = set()  # 重複を防ぐためにセットを使用

    for root, _, files in os.walk(directory):
        for file in files:
            parent_dir = os.path.basename(root)  # 1つ前のディレクトリ名を取得
            parent_dirs.add(parent_dir)  # セットに追加

    # セットをリストに変換してJSON形式で保存
    data = {"directories": list(parent_dirs)}
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"ディレクトリ名一覧をJSONに保存しました: {json_file}")
    
# 使用例
source_directory = "./src/uploads"  # 監視するディレクトリ
target_root_directory = "./data/original"  # 移動先のルートディレクトリ
output_json = "./src/static/js/file_list.json"

monitor_and_process_files(source_directory, target_root_directory, output_json)
