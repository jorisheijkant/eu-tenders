import ollama
import csv
import json
import re

labeled_rows = []
limit = 3
prompt = """
You are a labeling bot that only outputs JSON values. 
You'll get to see a EU Tender and will try and find out whether it is urgent or not.
The tender will be in Dutch.
You look for words that indicate haste, such as 'spoed', 'haast' or English variants like 'urgent'.
You will answer with a JSON object in the following format: {'urgent': urgent}, where urgent is a boolean (uncapitalized). 
You will only answer with the JSON. No explanation given. JUST THE JSON.
"""

with open("urgent_tenders.csv", "r") as csv_bestand:
    reader = csv.reader(csv_bestand)

    for index, row in enumerate(reader):
        if index > 0:
            print(f"Now labeling row {row[0]}")

            messages = [
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": f"{row[1]} - {row[3]} - {row[4]}"
                }
            ]

            #NB: change this to a model that you have installed if needed
            response = ollama.chat(model='llama3', messages=messages)

            try:
                ollama_response = response['message']['content']

                json_pattern = r'\s*\{[^}]*\}\s*'
                json_match = re.search(json_pattern, ollama_response)

                if json_match:
                    json_object = json_match.group()
                    ollama_object = json.loads(json_object)

                    print(ollama_object)
            except Exception as e:
                print(f"Failing to parse Ollama answer: {e}")
            
