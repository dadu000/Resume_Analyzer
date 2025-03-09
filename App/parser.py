import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def parse_text(text, type="resume"):
    prompt = f"""
    Analyze this {type} text and return the following in strict JSON format:
    ```json
    {{
        "skills": ["skill1", "skill2", ...],
        "experience": number_of_years
    }}

    Ensure the response is only valid JSON, no extra text, code blocks, or explanations.
Text:
{text}
"""
    try:
        response = model.generate_content(prompt)
        raw_text = response.text
        cleaned_text = raw_text.replace("json\n", "").replace("\n", "").replace("```", "").strip()
        json.loads(cleaned_text)
        return cleaned_text
    except Exception as e:
        print(f"Error in parse_text: {str(e)}")
        return '{"skills": [], "experience": 0}'

# if __name__ == "__main__":
#     sample_text = "Experienced developer with 5 years in Python and Java."
#     result = parse_text(sample_text, type="resume")
#     print("Test Result:", result)