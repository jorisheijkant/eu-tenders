import os
import xml.etree.ElementTree as ET
import csv

urgent_files = []
urgent_tenders = []
all_files = []
all_tenders = []

for (folder, x, files) in os.walk("data/known_urgent"):
    for file in files:
        urgent_files.append(f"data/known_urgent/{file}")
        all_files.append(f"data/known_urgent/{file}")

for (folder, x, files) in os.walk("data/random_tenders"):
    for file in files:
        all_files.append(f"data/random_tenders/{file}")

print(f"Found {len(urgent_files)} urgent files and a total of {len(all_files)} to parse")

def parse_file(file):
    print(f"Now parsing file {file}")
    # TO DO: add all necessary properties here
    project_id = file.split(".")[0]
    project_name = ""
    project_description = ""
    project_process_description = ""
    project_process_code = ""

    try:
        namespaces = {"cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2", "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"} # See the root of the XML file
        tree = ET.parse(file)
        root = tree.getroot() 
        for project in root.findall("cac:ProcurementProject", namespaces):  
            project_name_element = project.find("cbc:Name", namespaces)
            if project_name_element is not None:
                project_name = project_name_element.text
            project_description_element = project.find("cbc:Description", namespaces)
            if project_description_element is not None:
                project_description = project_description_element.text
        tendering_process_element = root.find("cac:TenderingProcess", namespaces)
        if tendering_process_element is not None:
            procedure_code_element = tendering_process_element.find("cbc:ProcedureCode", namespaces)
            if procedure_code_element is not None:
                project_process_code = procedure_code_element.text
            
            process_justification_element = tendering_process_element.find("cac:ProcessJustification", namespaces)
            if process_justification_element is not None:                
                process_name_element = process_justification_element.find("cbc:ProcessReason", namespaces)
                if process_name_element is not None:
                    project_process_description = process_name_element.text

        return {
            "id": project_id,
            "name": project_name,
            "description": project_description,
            "process_code": project_process_code,
            "process_description": project_process_description
        }
          
    except Exception as e:
        print(f"Failed to parse XML for file {file}: {e}")
        return {}

for file in urgent_files:
    parsed_file = parse_file(file)
    print(parsed_file)
    if parsed_file.get("id"):
        urgent_tenders.append(parsed_file)

for file in all_files:
    parsed_new_file = parse_file(file)
    if parsed_new_file.get("id"):
        all_tenders.append(parsed_new_file)

with open("urgent_tenders.csv", "w") as urgent_csv_output:
    urgent_csv_writer = csv.writer(urgent_csv_output)
    urgent_csv_writer.writerow(["id", "name", "process_code", "description", "process_description"])
    for tender in urgent_tenders:
        urgent_csv_writer.writerow([tender["id"], tender["name"], tender["process_code"], tender["description"], tender["process_description"]])

with open("all_tenders.csv", "w") as all_csv_output:
    all_csv_writer = csv.writer(all_csv_output)
    all_csv_writer.writerow(["id", "name", "process_code", "description", "process_description"])
    for tender in all_tenders:
        all_csv_writer.writerow([tender["id"], tender["name"], tender["process_code"], tender["description"], tender["process_description"]])