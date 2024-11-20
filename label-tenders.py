import ollama
import csv
import json
import re

limit = 10
prompt = """
You are a labeling bot that only outputs JSON values. 
You'll get to see the text of a EU Tender and will try and find out whether it is urgent or not.
The tender will be in Dutch.
You look for words that indicate haste, or speed, such as 'spoed', 'haast', 'zeer urgent' or English variants like 'urgent'.
You will answer with a JSON object in the following format: {'urgent': urgent}, where urgent is a javascript boolean (uncapitalized), according to whether the tender is urgent or not. 
You will only answer with the JSON. No explanation given. JUST THE JSON.
"""

def label_file(file, limit):
    labeled_rows = []

    with open(file, "r") as csv_file:
        reader = csv.reader(csv_file)

        for index, row in enumerate(reader):
            if index > 0 and index <= limit:
                print(f"Now labeling row nr {index} - id {row[0]}")

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
                        row.append(ollama_object.get("urgent"))
                    
                    labeled_rows.append(row)

                except Exception as e:
                    print(f"Failing to parse Ollama answer: {e}")

    return labeled_rows

with open("urgent_tenders_labeled.csv", "w") as urgent_output_file:
    urgent_csv_writer = csv.writer(urgent_output_file)
    urgent_csv_writer.writerow(["id", "name", "urgent_label", "process_code", "description", "process_description"])

    labeled_rows = label_file("urgent_tenders.csv", limit)

    for row in labeled_rows:
        urgent_csv_writer.writerow([row[0], row[1], row[5], row[2], row[3], row[4]])

with open("all_tenders_labeled.csv", "w") as all_output_file:
    all_csv_writer = csv.writer(all_output_file)
    all_csv_writer.writerow(["id", "name", "urgent_label", "process_code", "description", "process_description"])

    labeled_rows = label_file("all_tenders.csv", limit)

    for row in labeled_rows:
        all_csv_writer.writerow([row[0], row[1], row[5], row[2], row[3], row[4]])

            
