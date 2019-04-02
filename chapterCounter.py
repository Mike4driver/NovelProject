import json

with open("novels.json", 'r') as f:
    novelJson = json.load(f)

novelList = novelJson['Novels']

count = 0
for novel in novelList:
    i+=len(novel['Chapters'])

print(f'there are {count} chapters')