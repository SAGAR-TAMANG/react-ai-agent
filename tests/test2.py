from typing import Any
from dotenv import load_dotenv
import google.generativeai as genai 
import os, re

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API'))

model = genai.GenerativeModel('gemini-1.5-flash')

chat = model.start_chat(history=[])

response = chat.send_message('Hi')

print(response.text)