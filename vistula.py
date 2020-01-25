from bs4 import BeautifulSoup
import requests


result_vistula = requests.get("https://vistula.pl/garnitury")

src_vistula = result_vistula.content

soup = BeautifulSoup(src_vistula, features="lxml")

suits_vistula = soup.find_all("li", class_="picture_on_list js--picture-hover")


dict_vistula = {}
dict_vistula['suits'] = []

for index, suit in enumerate(suits_vistula):

    # getting suit info
    product_info = suit.find("div", class_="product__info")
    name = product_info.find("h3").get_text()
    link = suit.find("a", href=True)["href"]

    #getting the price before and after a discount
    price_before = product_info.find("del").text.split()[0].replace(",", ".")
    price_now = product_info.find("em").text.split()[0].replace(",", ".")
    
    #getting discount and discount percentage
    discount = round(float(price_now) * 100 / float(price_before), 2)
    discount_percentage = round(100 - float(discount), 2)

    #creating an item and adding it to dict_vistula['suits'] list
    suit_data = {
        "name": name,
        "link": link,
        "price_before": price_before,
        "price_now": price_now,
        "discount": discount,
        "discount_percentage": discount_percentage
        }

    dict_vistula['suits'].append(suit_data)

    # print(index, price_before, price_now, str(discount_percentage) + "%")


# sorting by discount_percentage
s_dict_vistula = sorted(dict_vistula['suits'], key=lambda x: x.get('discount_percentage'), reverse=True)
print(s_dict_vistula)

