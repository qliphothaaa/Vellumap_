import json

with open('./json/iseki.json', "r") as file:
    raw_data = file.read()
    data = json.loads(raw_data, encoding='utf-8')
    
    for i in data['object_types']:
        print(i)


