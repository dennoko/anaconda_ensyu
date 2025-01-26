import os
import csv
from pydub import AudioSegment
import re
import json

# 関数のインポート
from check_volume import get_db
from check_overtone import get_overtone
from check_attack_time import get_attack_time
from check_sustain import get_db_at_time
from processed_file import processed_file
from except_overtone import get_difference
from api.chatgpt_api_with_openai import chat_gpt_api_request
from api.chatgpt_api_with_openai import init_prompt
from api.chatgpt_api_with_openai import add_prompt

def process_audio_files(input_dir, output_dir):
    data_by_pickup = {}
    processed_file()
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".wav"):
                processed_file_path = os.path.join(root, file)

                # ファイル名から情報を取得
                relative_path = os.path.relpath(processed_file_path, input_dir)
                parts = relative_path.split(os.sep)
                if len(parts) < 3:
                    continue
                guitar_name, pickup_position, file_name = parts[-3:]
                parts_guitar = file_name.split("_")
                fret_info = parts_guitar[-1].split(".")[0]  # 例: "12_1"
                if not fret_info.isdigit():
                    continue
                fret = int(fret_info)  # フレット番号
                
                fret12 = parts_guitar[-2]
                fret12_flag = False
                if fret12.isdigit():
                    fret12_flag = True
                    fret12 = fret * 100 + int(fret12) 

                # 出力CSVキー
                csv_key = (guitar_name, pickup_position)
                if csv_key not in data_by_pickup:
                    data_by_pickup[csv_key] = {"Volume":{}, "Attack Time": {}, "Sustain": {}, "Overtones": {}, "Except_Overtone": {}}

                csv_path = os.path.join(output_dir, f"{guitar_name}_{pickup_position}.csv")
                os.makedirs(os.path.dirname(csv_path), exist_ok=True)
                
                # CSVファイルの存在確認
                if os.path.exists(csv_path):
                    print(f"CSV already exists. Skipping: {csv_path}")
                    continue 
                
                # 音声ファイルを読み込み
                sound = AudioSegment.from_wav(processed_file_path)
                samples = sound.get_array_of_samples()

                # 処理結果の取得
                max_db = sound.max_dBFS
                attack_time = get_attack_time(samples, sound.frame_rate)
                sustain = get_db_at_time(samples, sound.frame_rate, 3.0, max_db)
                overtone_freqs, overtone_mags = get_overtone(samples, sound.frame_rate, sound.duration_seconds)
                overtone_formatted = "_".join([f"{freq:.2f}:{mag:.2e}" for freq, mag in zip(overtone_freqs, overtone_mags)])
                extension = ".wav"
                string_num = []
                base_name = file_name[:-len(extension)]
                if base_name[-1].isdigit():
                    string_num.append(int(base_name[-1]))
                    
                match = re.search(r'(\d+)_\d+$', base_name)
                octave = False
                if match:
                    octave = True
                except_overtone = get_difference(samples, sound.frame_rate, string_num, octave)
                
                if fret12_flag == True:
                    data_by_pickup[csv_key]["Volume"][fret12] = max_db
                    data_by_pickup[csv_key]["Attack Time"][fret12] = attack_time
                    data_by_pickup[csv_key]["Sustain"][fret12] = sustain
                    data_by_pickup[csv_key]["Overtones"][fret12] = overtone_formatted
                    data_by_pickup[csv_key]["Except_Overtone"][fret12] = except_overtone
                else:
                    data_by_pickup[csv_key]["Volume"][fret] = max_db
                    data_by_pickup[csv_key]["Attack Time"][fret] = attack_time
                    data_by_pickup[csv_key]["Sustain"][fret] = sustain
                    data_by_pickup[csv_key]["Overtones"][fret] = overtone_formatted
                    data_by_pickup[csv_key]["Except_Overtone"][fret] = except_overtone

    # chat-gptのプロンプトを生成して、chat-gptにリクエストを送信
    prompt = init_prompt(guitar_name)
                    
    # 各ピックアップのデータをCSVに書き込み
    for (guitar_name, pickup_position), data in data_by_pickup.items():
        csv_path = os.path.join(output_dir, f"{guitar_name}_{pickup_position}.csv")
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        if os.path.exists(csv_path):
            print(f"CSV already exists. Skipping: {csv_path}")
            continue 
        
        # 出力データの準備
        headers = ["処理名", "1弦(12フレット)", "2弦(12フレット)", "3弦(12フレット)", "4弦(12フレット)", "5弦(12フレット)", "6弦(12フレット)"]
        rows = []

        for process_name in ["Volume", "Attack Time", "Sustain", "Overtones", "Except_Overtone"]:
            row = [process_name]
            for string_number in range(1, 7):  # 1弦～6弦
                fret_data_12 = data[process_name].get(string_number * 100 + 12)
                fret_data = data[process_name].get(string_number)
                if fret_data and fret_data_12:
                    row.append(f"{fret_data}|{fret_data_12}")
                else:
                    row.append("")
            rows.append(row)

        # CSV書き込み
        with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(headers)
            csv_writer.writerows(rows)

        print(f"Processed data for {guitar_name} - {pickup_position} -> {csv_path}")
        

        with open(csv_path, "r") as f:
            data = f.read()

        prompt = add_prompt(prompt, "以下は{guitar_name}のピックアップポジション{pickup_position}の音に関するcsvデータです。これを元に、指定した項目について評価してください。")
        prompt = add_prompt(prompt, data)

    # chat-gptのレスポンスをguitar.jsonに追加
    # guitar.jsonのフォーマットは以下の通り
    # [
    #     {
    #       "ギター名": "ギター名",
    #       "メーカー": "メーカー",
    #       "メーカーの国": "メーカーの国",
    #       "音のバランスの評価": "音のバランスの評価",
    #       "サステインの評価": "サステインの評価",
    #       "レスポンスの評価": "レスポンスの評価",
    #       "倍音の評価": "倍音の評価",
    #       "トーンの評価": "トーンの評価",
    #       "総合評価": "総合評価"
    #     }
    # ]
    # responseは配列の要素の形式で返ってくるので、配列に追加する
    response = chat_gpt_api_request(prompt)

    with open("guitar.json", "r") as f:
        guitar_json = json.load(f)

    guitar_json.append(response)

    with open("guitar.json", "w") as f:
        json.dump(guitar_json, f, ensure_ascii=False, indent=4)

    print(f"Chat-GPT response for {guitar_name} - {pickup_position} -> guitar.json")

# 入力ディレクトリと出力ディレクトリを設定
processed_file()
input_directory = "./data/processed"
output_directory = "./output"

process_audio_files(input_directory, output_directory)

