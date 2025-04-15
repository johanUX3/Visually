import requests
from utils.vision import describe_image

HF_API_KEY = ""
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"

def analyze_image_prompt(image_file, user_prompt):
    try:
        caption = describe_image(image_file)  # Get caption from the image
        if not caption:  # In case caption is None
            return None, "Error: Unable to generate image caption."
        
        comparison_prompt = f"Compare the caption with user prompt: {user_prompt}"
        # Add logic to generate feedback (styling suggestions, etc.)
        feedback = "Styling suggestions: Increase contrast, adjust brightness."
        
        return caption, feedback  # Return caption and feedback as a tuple
    except Exception as e:
        # Log the error message and return a default message
        return None, f"Error: {str(e)}"


def generate_styling_suggestions(image_file, user_prompt):
    # This is a mock function that generates styling suggestions
    return [
        "Increase contrast for better visibility.",
        "Adjust brightness to match the user's mood.",
        "Consider adding warmer tones for a more inviting feel.",
        "Try a blur effect for a softer aesthetic."
    ]

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 500}
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        try:
            output = response.json()
            generated = output[0]["generated_text"]
            return caption, generated
        except Exception as e:
            return caption, f"❌ Error parsing Hugging Face response: {str(e)}"
    else:
        return caption, f"❌ Hugging Face API Error: {response.status_code} – {response.text}"
