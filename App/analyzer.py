import os                          # Import os module for operating system interactions
from dotenv import load_dotenv    # Import load_dotenv to load environment variables from .env
import google.generativeai as genai  # Import Gemini AI library for text generation
import json                        # Import json module for JSON handling

load_dotenv()                      # Load environment variables from .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Configure Gemini with API key from .env
model = genai.GenerativeModel("gemini-1.5-flash")     # Initialize Gemini model with specified version

def generate_suggestions(resume_text, job_text, match_data):  # Define function to generate suggestions
    prompt = f"""                    # Start f-string for prompt to Gemini
    Given this resume and job description, provide suggestions to improve the resume in strict JSON format:  # Instruction for Gemini
    ```json                         # Start JSON format example
    ["suggestion 1", "suggestion 2", ...]  # Expected output structure as a list of strings
    ```                             # End JSON format example
    Ensure the response is only valid JSON, no extra text, code blocks, or explanations.  # Instruction to return only JSON
    Resume: {resume_text[:500]}...  # Include first 500 characters of resume text
    Job Description: {job_text[:500]}...  # Include first 500 characters of job text
    Current Match: {json.dumps(match_data)}  # Include current match data as JSON string
    """                             # End f-string prompt
    try:                            # Start try block for error handling
        response = model.generate_content(prompt)  # Send prompt to Gemini and get response
        raw_text = response.text    # Extract raw text from response
        cleaned_text = raw_text.replace("```json\n", "").replace("\n```", "").replace("```", "").strip()  # Clean response by removing code blocks and whitespace
        json.loads(cleaned_text)    # Validate that cleaned text is proper JSON
        return cleaned_text         # Return cleaned JSON string
    except Exception as e:          # Catch any exceptions
        print(f"Error in generate_suggestions: {str(e)}")  # Print error message
        return '["Error generating suggestions"]'  # Return fallback JSON string