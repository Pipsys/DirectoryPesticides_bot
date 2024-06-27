from config import *

r = requests.get("https://www.agroxxi.ru/goshandbook/prep/abakus-praym-se-2.html")
html = BS(r.content, 'html.parser')

page_all_p = html.find_all("p")

for item in page_all_p:
    print(item.text)

# data = BS.find("div", class="prepdata").find(".prephar")
# print(data.text)