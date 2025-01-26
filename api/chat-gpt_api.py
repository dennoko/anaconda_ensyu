import requests

# OPENAI_API_KEY
API_KEY = "OPENAI_API_KEY"

# ChatGPTのエンドポイント
ENDPOINT = "https://api.openai.com/v1/chat/completions"

# リクエストヘッダ
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# リクエストボディ
def create_request_body(): # 分析する値を引数で渡し、プロンプトに含める
    data = {
        "model": "gpt-3.5-turbo", # 使用するモデル
        "messages": [ # メッセージ
            {"role": "system", "content": "."}, # AIにロールを設定する
            {"role": "user", "content": "こんにちは"} # プロンプト        ]
        ]
    }

    return data

def chat_gpt_api(data):
    response = requests.post(ENDPOINT, json=data, headers=headers)
    return response.json()

if __name__ == "__main__":
    data = create_request_body()
    response = chat_gpt_api(data)
    print(response)