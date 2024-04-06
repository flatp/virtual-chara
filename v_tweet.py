import tweepy
import openai
import requests
import cv2
import random
import datetime

# Twitterの認証情報
B_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAFGkpwEAAAAArjixo8rnU10Q%2BbE83bK2ClMbIaY%3DbbdsarfObdyCXRoLUCkIC5jxpsRFr1zGl0WaNiWjRhD7yyjmuY'
C_KEY = 'Na31sGRdUqcIBv2PxT0Zr4px5'
C_SEC = 'HglySZ4L153kh2gPcTFyxxWFNGcOdK2NEuCGWUormonmafDNbh'
A_TOKEN = '1701511944795193344-3UUOFkScjnawq2VBhKxRlZ4VyLNKvG'
A_SEC = 'dY26H7kYF3MdD4GLth80RXGxCCnFO7215ZfTF8Gylqk3h'

auth = tweepy. OAuthHandler ( C_KEY, C_SEC)
auth. set_access_token(A_TOKEN, A_SEC)

api = tweepy.API (auth)
client = tweepy.Client(bearer_token=B_TOKEN, 
                    consumer_key=C_KEY, consumer_secret=C_SEC,
                    access_token=A_TOKEN, access_token_secret=A_SEC)

openai_api_key = "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"
openai.api_key = openai_api_key

def create_image_from_text(text):
    
    # 応答設定 
    response = openai.Image.create(
                  prompt = text,             # 画像生成に用いる説明文章
                  n = 1,                     # 何枚の画像を生成するか
                  size = '1024x1024',          # 画像サイズ
                  response_format = "url"    # API応答のフォーマット
                )

    # API応答から画像URLを指定
    image_url = response['data'][0]['url']
    
    # 画像をローカルに保存
    image_data = requests.get(image_url).content
    with open("chat-gpt-generated-image.jpg", "wb") as f:
        f.write(image_data)
        
    return image_url

def rayer():
    flag = random.randint(1, 3)
    if flag == 1:
        fore = "test11.png"
    elif flag == 2:
        fore = "test22.png"
    else:
        fore = "test33.png"
    fore_img = cv2.imread(fore, cv2.IMREAD_UNCHANGED)
    back_img = cv2.imread('v_chara.jpg')
    dx = 0    # 横方向の移動距離
    dy = 349    # 縦方向の移動距離
    h, w = fore_img.shape[:2]
    back_img[dy:dy+h, dx:dx+w] = back_img[dy:dy+h, dx:dx+w] * (1 - fore_img[:, :, 3:] / 255) + \
                      fore_img[:, :, :3] * (fore_img[:, :, 3:] / 255)
    #back_img[dy:dy+h, dx:dx+w] = fore_img
    

    
    cv2.imwrite('final.jpg', back_img)

messages = [{"role": "user", "content": "なにか物あるいは風景を対象として、その物や雰囲気を具体的に補足してひとつ指定してください"}
]

completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

ppt = completion["choices"][0]["message"]["content"]
print(ppt)

messages = [{"role": "system", "content": "応答文は必ず120文字以内で、ツイートのに文章を生成してください"},
            {"role": "system", "content": "あなたは明るく元気な女の子です"},
            {"role": "system", "content": "あなたは進学校に通っている高校生です"},
            {"role": "system", "content": "あなたは部活動では軽音楽部に入っていて、担当はギターです"},
            {"role": "system", "content": "あなたは天然なところがありますが自分では気づいていません"},
            {"role": "system", "content": "くだけた言葉遣いで短めに話してください"},
            {"role": "system", "content": "あなたは休日は家にいることが多いです"},
            {"role": "user", "content": "\""+ppt+"\"のような画像を添付する日常のツイートの文章を考えてください"}
]
completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

res_message = completion["choices"][0]["message"]["content"]
print(res_message)

if (res_message[0] == "「" and res_message[-1] == "」") or (res_message[0] == "\"" and res_message[-1] == "\""):
    res_message = res_message[1:-1]

img = create_image_from_text(ppt)
response = requests.get(img)
image = response.content
with open("v_chara.jpg", "wb") as f:
    f.write(image)

#rayer()
# 自動投稿
media = api. media_upload (filename="v_chara.jpg")
client.create_tweet(text=res_message+" #AIキャラクター #AIart", media_ids= [media.media_id])