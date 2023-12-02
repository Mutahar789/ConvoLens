import json
from database import pgvector

db = pgvector()

with open("./build_data/data.json", "r") as file:
    data = json.loads(file.read())

for k in data.keys():
    row = data[k]
    db.insert(row)
