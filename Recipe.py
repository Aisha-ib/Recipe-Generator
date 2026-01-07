import requests
import json
import os
from dotenv import load_dotenv

# Load API Key from e.env file
env_path = "/Users/e.env"
load_dotenv(env_path)
api_key = os.getenv("FIREWORKS_API_KEY")

# API URL
url = "https://api.fireworks.ai/inference/v1/chat/completions"

# Get ingredients from user
ingredients = input("Please enter the available ingredients (comma-separated): ")

# Define the JSON payload for the API request
payload = {
    "model": "accounts/fireworks/models/deepseek-v3",
    "max_tokens": 1000, # max number of tokens to generate
    "temperature": 0,  #lower temperature for Deterministic response and the same pattern every time, high temperature less structured and may sometimes adds extra details 
    "messages": [
        {
            "role": "user",
            # Prompt for the model, well-structured prompt ensures consistent output
          "content": f"Please create a recipe using the following ingredients: {ingredients}. "
           "Include a creative name with 'Recipe Title:' and a short introduction, "
           "ingredients with 'Ingredients:', and cooking steps with 'Cooking Steps:'. "
           "Also, include 'Nutritional Info' with the estimated calories, protein, fat, and carbs per serving, "
           "all formatted as strings (e.g., 'Calories': '350', 'Protein': '20g'). "
           "If necessary, suggest common pantry items like salt, pepper, or oil, "
           "but do not introduce new main ingredients. "
           "Format your response strictly as JSON, without any Markdown, asterisks (**), or extra text."
           

        }
    ]
}

# Define headers
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Send the API request
response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code != 200: # Check if the API request was successful
    print("An error occurred while sending the API request. Please try again.")
    exit()

response_data = response.json()
print(response_data)

data = response_data["choices"][0]["message"]["content"]

try: 
        recipe = json.loads(data)
except json.JSONDecodeError: # Check if the JSON response is valid 
    print("An error occurred while parsing the JSON response. Please try again.")
    exit()

for k in recipe.keys(): # Handle incomplete or strange results.
    if recipe[k] == "":
        print("An error occurred while generating the recipe. Please try again.")
        exit()

print("\nRecipe Title: " + recipe["Recipe Title"] + "\n")
print("Introduction: " + recipe["Introduction"] + "\n")

print("Ingredients:")
for i in recipe["Ingredients"]:
    print("- " + i)

print("\nCooking Steps:")
for j, step in enumerate(recipe["Cooking Steps"], 1):
    print(str(j) + "- " + step)

print("\nNutritional Info:")
for m, value in recipe["Nutritional Info"].items():
    print(f"{m}: {value}")

print("\nEnjoy your meal! ") 
