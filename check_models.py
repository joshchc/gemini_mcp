import google.generativeai as genai

genai.configure(api_key = 'AIzaSyDsSAvfkANfOrQTawrm_m2Wg3SRwdyoldk')

print("可用的模型：")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"- {model.name}")