import os
import openai
openai_api_key = "hoge"
openai.api_key = openai_api_key

messages = [{"role": "system", "content": "あなたは高飛車なお嬢様です"},
            {"role": "system", "content": "語尾はですわにしてください"}
]

completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
# 応答の取得 / 表示 / messagesへの追加
res_message = completion["choices"][0]["message"]["content"]
print("出力： " + res_message)
messages.append({"role": "assistant", "content": res_message})

# token数の取得と表示
tokens = completion["usage"]["total_tokens"]
print("今回のToken数： " + str(tokens))

while True:
    # 入力 / messagesへの追加
    your_message = input("入力: ")
    if your_message == "quit":  # quitと入力されたら終了
        exit()
    messages.append({"role": "user", "content": your_message})

    # API呼び出し
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
    except (openai.error.RateLimitError, openai.error.InvalidRequestError) as e:
        print(e.user_message)
        exit()

    # 応答の取得 / 表示 / messagesへの追加
    res_message = completion["choices"][0]["message"]["content"]
    print("出力： " + res_message)
    messages.append({"role": "assistant", "content": res_message})

    # token数の取得と表示
    tokens = completion["usage"]["total_tokens"]
    print("今回のToken数： " + str(tokens))
