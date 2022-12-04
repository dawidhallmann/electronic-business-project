import json
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(ChromeDriverManager().install())

categories = [
    "https://www.morele.net/kategoria/monitory-523/",
    # 'https://www.morele.net/kategoria/akcesoria-komputerowe-674/',
    # 'https://www.morele.net/kategoria/gniazda-blatowe-12199/',
    # 'https://www.morele.net/kategoria/przedluzacze-10139/',
    # 'https://www.morele.net/kategoria/stabilizatory-napiecia-12042/',
    # 'https://www.morele.net/kategoria/baterie-i-akumulatorki-311/',
    # 'https://www.morele.net/kategoria/ladowarki-do-akumulatorkow-312/',
    # 'https://www.morele.net/kategoria/rozgalezniki-12198/'
]

# print('Dodawanie 2 karty w liście ')
# for ct in categories:
#     categories.append(ct + ',,,,,,,,0,,,,/2/') # card 2

products = []

print('Linki:')
print(categories)

for ct in categories:
    print('Wczytywanie ' + ct)

    driver.get(ct)
    time.sleep(2)
    products_nodes = driver.find_elements(
        "xpath", '//h2[@class="cat-product-name__header"]/a')
    # print(products_nodes)
    for pt in products_nodes:
        link = pt.get_attribute("href")

        obj = {
            'link': link
        }
        products.append(obj)

    # print(products)

for pd in products:
    print('Wczytywanie ' + pd['link'])
    driver.get(pd['link'])
    time.sleep(2)

    image_high_quality_link = driver.find_element(
        "xpath", '//div[@class="swiper-slide mobx swiper-slide-active"]/picture/img').get_attribute("src")
    category = driver.find_element(
        "xpath", '(//ol[@id="breadcrumbs"]/li/a[@class="main-breadcrumb"]/span)[last()]').text
    name = driver.find_element(
        "xpath", '//h1[@class="prod-name"]').text
    pd['name'] = name

    propertys = driver.find_elements(
        "xpath", '//div[@class="specification__row"]')

    pd['propertys'] = {}
    
    i = 1
    for propertys_item in propertys:
        name = propertys_item.find_element( # (//div[@class="specification__row"])[2]
            "xpath", '(//span[@class="specification__name"])['+str(i)+']').text

        value = propertys_item.find_element(
            "xpath", '(//span[@class="specification__value"])['+str(i)+']').text

        # waga

        # property_translate = {
        #     "waga [kg]": "weight",
        #     "waga [g]": "weight",
        #     "waga": "weight",
        # }

        # for proerty in ["Waga", "wEiGht"]:
        #     property = property.lower()
        #     print(property_translate.get(property, property))
        
        
        name = name.lower()
        
        # if(name in property_translate):
        #     name = property_translate.get(property, property)

        pd['propertys'][name] = value
        i = i + 1
        
        print(name + ' ' + value)

    pd['category'] = category
    # pd['producent'] = producent
    pd['image_high_quality_link'] = image_high_quality_link

    with open('data/products.json', 'w') as f:
        json.dump(products, f)
    
print(products)

driver.close()