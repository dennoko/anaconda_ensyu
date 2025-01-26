from openai import OpenAI

def chat_gpt_api_request(prompt):
    """
    引数: prompt: string
    
    返り値: answer: string
    
    引数として渡すpromptは、init_prompt関数で生成したものにadd_prompt関数でデータや追加の指示を加えたものとする。
    返り値はinit_prompt関数で指定したJSON形式に合わせて、promptに基づいて生成されたJSON形式のstringとなる。
    """

    client = OpenAI(api_key="OPENAI_API_KEY")

    print("Chat-GPT request -> chat-gpt")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.0, # tempratureとは、生成されるテキストの多様性を調整するためのパラメータ。0.0に設定すると、生成されるテキストは最も確信度の高いものになる。
        messages=[
            {"role": "system", "content": "音の専門家でありギターに精通している。今回はギターの音の数値データを元にしたレビュー記事の作成を手伝うことになっている。"},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )
    
    answer = response.choices[0].message.content
    
    return answer

def init_prompt(guitar_name):
    """
    引数: guitar_name: string

    返り値: prompt: string

    引数にはギター名を指定する。
    返り値はプロンプトの基本部分と、返り値のJSON形式を含むstringとなる。

    Chat-GPTのレスポンスのJSONデータ構造を変更したい場合は、この関数の期待されるJSONレスポンスを変更する。
    """

    guitar_name = guitar_name

    base_prompt = f"""
    ### 回答ルール
    以下の回答ルールは最優先で守ってください。
    - ユーザーが提供する情報を元に、指定されたJSON形式に合わせて各項目の文章を生成してください。
    - 文章は、提供された数値データにしたがって論理的に展開してください。
    - 文章中には具体的な数値データを含めてください。
    - また、メーカーとメーカーの国についてはギター名に基づいて決めてください。
    - 各項目について、300文字以上のレビューを生成し、ピックアップポジションの違いによる差についても書いてください。
    - ギター名は{guitar_name}です。
    """ + """
    ### 期待されるJsonレスポンス
    ```json
    {
        "ギター名": "ギター名",
        "メーカー": "メーカー",
        "メーカーの国": "メーカーの国",
        "音のバランスの評価": "音のバランスの評価",
        "サステインの評価": "サステインの評価",
        "レスポンスの評価": "レスポンスの評価",
        "倍音の評価": "倍音の評価",
        "トーンの評価": "トーンの評価",
        "総合評価": "総合評価"
    }
    ```

    """

    return base_prompt
    
def add_prompt(prompt, add_prompt):
    # promptを改行してadd_promptを追加する
    return prompt + "\n" + add_prompt
