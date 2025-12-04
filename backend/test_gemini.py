import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Try the actual model we'll use
    print("Testing models/gemini-2.5-flash...")
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content("Say hello in 5 words")
    print(f"✅ Success! Response: {response.text}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
