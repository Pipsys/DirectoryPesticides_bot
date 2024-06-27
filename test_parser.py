from config import *

r = requests.get("https://www.agroxxi.ru/goshandbook/prep/abakus-praym-se-2.html")
html = BS(r.content, 'html.parser')

h1_name = html.find("h1")
print(h1_name.text)

h2_group = html.find(attrs={'itemprop': 'category'})
print(h2_group.text)

prephar = html.find("div", class_="prephar")
# print(prephar.text)

pesticide_info = {}

paragraphs = prephar.find_all('p')

for paragraph in paragraphs:
    bold_text = paragraph.find('b')
    if bold_text:
        key = bold_text.get_text(strip=True).rstrip(':')
        value = paragraph.get_text().replace(bold_text.get_text(), '').strip()
        pesticide_info[key] = value

for key, value in pesticide_info.items():
    print(f"{key}: {value}")

# import json
# with open('pesticide_info.json', 'w', encoding='utf-8') as f:
#     json.dump(pesticide_info, f, ensure_ascii=False, indent=4)