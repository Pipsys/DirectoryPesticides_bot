from config import *

r = requests.get("https://www.agroxxi.ru/goshandbook/prep/abakus-praym-se-2.html")
html = BS(r.content, 'html.parser')

for el in html.select(".prepdata > .content"):
    title = el.select('.prephar > p')
    print( title[0].text )

    print("подкл")

print('не подкл')
