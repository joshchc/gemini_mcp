import google.generativeai as genai

genai.configure(api_key = 'AIzaSyDsSAvfkANfOrQTawrm_m2Wg3SRwdyoldk')

model = genai.GenerativeModel('gemini-2.5-flash')

chat = model.start_chat(history=[]) 

response = model.generate_content('怎麼使用 model context protocol在 gemini pro 裡面？')


print(response.text)