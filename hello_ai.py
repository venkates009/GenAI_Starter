import os
from dotenv import load_dotenv
from google import genai

# 1. Load the API Key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY or API_KEY == "your_api_key_here":
    print("❌ Error: API Key is missing!")
    exit(1)

# 2. Configure the New Gemini API Client
client = genai.Client(api_key=API_KEY)

print("⏳ Sending request to Gemini AI using gemini-flash-latest...")

prompt = "Enakku career gap irukku, aana naan AI developer aaganum nu aasa padren. Enakku Tamil la oru short motivational advice kudu."

try:
    # 3. Generate content using gemini-flash-latest (Most stable standard model)
    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=prompt,
    )
    
    print("\n" + "="*50)
    print("🤖 AI Response:")
    print("="*50)
    print(response.text)
    print("="*50)
    
except Exception as e:
    print(f"\n❌ An error occurred: {e}")
