import json
with open("/Users/harishgurram/Documents/GenAI/mcqgen/sample.json", "r") as file:
    print("Type=",type(file))
    print(json.load(file))
