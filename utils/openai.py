import requests
import base64
import json

# Flask server URL
URL = "http://81.201.57.116:5008"

def send_image_to_server(task_number: int, image_path: str):
    # Load and encode image to base64
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    if task_number == 1:
        prompt = "Please comment on the data trend in this chart. This chart represents number of articles by sex in blogs dataset."
    elif task_number == 2:
        prompt = "Please comment on the data trend in this chart. This chart represents the top 10 topics in blogs dataset."
    elif task_number == 3:
        prompt = "Please comment on the data trend in this chart. This chart represents the top 10 topics vs. zodiac signs in blogs dataset."
    else:
        raise ValueError("Invalid task number. Please provide a task number between 1 and 3.")
    # Define the payload
    payload = {
        "prompt": prompt,
        "image_base64": image_base64
    }

    # Send the POST request
    response = requests.post(URL, json=payload)

    # Print the response
    if response.ok:
        return f'🧠 GPT Response:\n {response.json()["response"]}',
    else:
        return f'❌ Error: {response.status_code}, {response.text}'
