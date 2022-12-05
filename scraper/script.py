import json
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import codecs

# driver = webdriver.Chrome(ChromeDriverManager().install())

driver = webdriver.Chrome(executable_path="chromedriver")

save_to = 'data/products.json'

categories = []
categories_initial = [
    'https://www.morele.net/kategoria/laptopy-31/'
    # "https://www.morele.net/kategoria/monitory-523/",
    # 'https://www.morele.net/kategoria/akcesoria-komputerowe-674/',
    # 'https://www.morele.net/kategoria/gniazda-blatowe-12199/',
    # 'https://www.morele.net/kategoria/przedluzacze-10139/',
    # 'https://www.morele.net/kategoria/stabilizatory-napiecia-12042/',
    # 'https://www.morele.net/kategoria/baterie-i-akumulatorki-311/',
    # 'https://www.morele.net/kategoria/ladowarki-do-akumulatorkow-312/',
    # 'https://www.morele.net/kategoria/rozgalezniki-12198/'
    # 'https://www.morele.net/kategoria/glosniki-komputerowe-6/'
    # 'https://www.morele.net/kategoria/czytniki-e-book-542/'
]
# 600 

for ct in categories_initial:
    categories.append(ct) 
    categories.append(ct + ',,,,,,,,0,,,,/2/')

products = []

print('Linki:')
print(categories)

for ct in categories:
    print('Wczytywanie ' + ct)

    driver.get(ct)
    time.sleep(2)
    products_nodes = driver.find_elements(
        "xpath", '//h2[@class="cat-product-name__header"]/a')

    for pt in products_nodes:
        link = pt.get_attribute("href")

        obj = {
            'link': link
        }
        products.append(obj)

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
        name = propertys_item.find_element(  # (//div[@class="specification__row"])[2]
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

        pd['propertys'][name] = value
        i = i + 1

    variants = driver.find_elements(
        "xpath", '//div[@class="variants-items"]/div[@class="variant variant-buttons"]')

    pd['variants'] = {}

    i = 1
    for variants_item in variants:
        name = variants_item.find_element(
            "xpath", '(//div[@class="variants-items"]/div[@class="variant variant-buttons"]/div[@class="variant-f_head"])['+str(i)+']').text

        name = name[:-1]

        items = variants_item.find_elements(
            "xpath", '(//div[@class="variants-items"]/div[@class="variant variant-buttons"]/div/ul)['+str(i)+']/li')

        pd['variants'][name] = []


        i2 = 1
        for item in items:
            x = '((//div[@class="variants-items"]/div[@class="variant variant-buttons"]/div/ul)[' + \
                str(i)+']/li)['+str(i2)+']'
            v = item.find_element(
                "xpath", x)

            name2 = v.text  # v.get_attribute('data-dropdown-label')
            price = v.get_attribute('data-price-brutto')
            image = v.get_attribute('data-product-image')

            nv = {
                'name': name2,
                'price_brutto': price,
                'image': image,
            }


            pd['variants'][name].append(nv)
            i2 = i2 + 1

        i = i + 1

    pd['category'] = category
    pd['image_high_quality_link'] = image_high_quality_link

    with codecs.open(save_to, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False)


print('Zapisywanie pliku do ' + save_to)

driver.close()
