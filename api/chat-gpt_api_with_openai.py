from openai import OpenAI

def chat_gpt_api_request(prompt):
    """
    引数: prompt: string
    
    返り値: answer: string
    
    引数として渡すpromptは、init_prompt関数で生成したものにadd_prompt関数でデータや追加の指示を加えたものとする。
    返り値はinit_prompt関数で指定したJSON形式に合わせて、promptに基づいて生成されたJSON形式のstringとなる。
    """

    client = OpenAI(api_key="OPENAI_API_KEY")

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

    base_prompt = """
    ### 回答ルール
    - ユーザーが提供する情報を元に、指定されたJSON形式に合わせて各項目の文章を生成してください。
    - 文章は、提供された数値データにしたがって論理的に展開してください。
    - ギター名は{guitar_name}です。

    ### 期待されるJsonレスポンス
    ```json
    {
        "ギター名": "ギター名",
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

if __name__ == "__main__":
    guitar_name = "Fender Stratocaster"
    prompt = init_prompt(guitar_name)
    add_prompt_str = "10段階評価で音の大きさを評価すると、高音域8, 中音域7, 低音域6となる。"
    prompt = add_prompt(prompt, add_prompt_str)
    add_prompt_str = "10段階評価でサステインを評価すると、高音域8, 中音域7, 低音域6となる。"
    prompt = add_prompt(prompt, add_prompt_str)
    add_prompt_str = "10段階評価でレスポンスを評価すると、高音域8, 中音域7, 低音域6となる。"
    prompt = add_prompt(prompt, add_prompt_str)
    response = chat_gpt_api_request(prompt)
    print(response)