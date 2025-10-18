import google.generativeai as genai
import os
from dotenv import load_dotenv

# 載入 .env 文件
load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel('gemini-2.5-flash')

chat = model.start_chat(history=[]) 

response = model.generate_content('怎麼使用 model context protocol在 gemini pro 裡面？')


print(response.text)