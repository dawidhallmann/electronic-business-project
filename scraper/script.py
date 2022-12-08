import json
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import codecs
import markdownify

# driver = webdriver.Chrome(ChromeDriverManager().install())

driver = webdriver.Chrome(executable_path="chromedriver")

save_to = 'data/products.json'
save_to_l = 'data/product_links.json'
save_to_l_2 = 'data/product_links_done.json'

limit = 551

categories = []
categories_initial = [
    'https://www.morele.net/kategoria/laptopy-31/',
    "https://www.morele.net/kategoria/monitory-523/",
    'https://www.morele.net/kategoria/akcesoria-komputerowe-674/',
    'https://www.morele.net/kategoria/gniazda-blatowe-12199/',
    'https://www.morele.net/kategoria/przedluzacze-10139/',
    'https://www.morele.net/kategoria/stabilizatory-napiecia-12042/',
    'https://www.morele.net/kategoria/baterie-i-akumulatorki-311/',
    'https://www.morele.net/kategoria/ladowarki-do-akumulatorkow-312/',
    'https://www.morele.net/kategoria/rozgalezniki-12198/',
    'https://www.morele.net/kategoria/glosniki-komputerowe-6/',
    'https://www.morele.net/kategoria/czytniki-e-book-542/',
    'https://www.morele.net/kategoria/klucze-udarowe-i-pneumatyczne-10235/',
    'https://www.morele.net/kategoria/frezarki-10051/',
    'https://www.morele.net/kategoria/wyrzynarki-10162/',
]
# cat data/product_links.json | uniq | wc -l

for ct in categories_initial:
    categories.append(ct)
    categories.append(ct + ',,,,,,,,0,,,,/2/')

products = []
products_links = []
products_links_done = []

with open(save_to_l) as f:
    fc = f.read()
products_links = json.loads(fc)

if(len(products_links) < limit):
    for ct in categories:
        print('Wczytywanie ' + ct)
    
        driver.get(ct)
        time.sleep(1)
        products_nodes = driver.find_elements(
            "xpath", '//h2[@class="cat-product-name__header"]/a')
    
        for pt in products_nodes:
            link = pt.get_attribute("href")
    
            if (not any(x for x in products_links if x == link)):
                products_links.append(link)
    
            if (len(products_links) >= limit):
                break
    
        print('Znaleziono '+str(len(products_links)) +
              '/'+str((limit))+' unikatowych produktów.')
    
        if (len(products_links) >= limit):
            break
    
    with codecs.open(save_to_l, 'w', encoding='utf-8') as f:
        json.dump(products_links, f, ensure_ascii=False)

with open(save_to) as f:
    fc = f.read()
products = json.loads(fc)
with open(save_to_l_2) as f:
    fc = f.read()
products_links_done = json.loads(fc)

print('Znaleziono '+str(len(products_links)) +
      '/'+str((limit))+' unikatowych produktów.')
print('Znaleziono '+str(len(products_links_done)) +
      '/'+str((limit))+' pobranych produktów.')

# with codecs.open(save_to_l, 'w', encoding='utf-8') as f:
#     json.dump(products_links, f, ensure_ascii=False)

for pd_link in products_links:
    if (not any(x for x in products_links_done if x == pd_link)):
        try:
            print('Wczytywanie ' + pd_link)
            driver.set_page_load_timeout(15)
            driver.get(pd_link)
            time.sleep(1)
    
            pd = {
                'link': pd_link
            }
    
            image_high_quality_link = driver.find_element(
                "xpath", '//div[@data-rel="primaryGallery"]/picture/img').get_attribute("src")
            category = driver.find_element(
                "xpath", '(//ol[@id="breadcrumbs"]/li/a[@class="main-breadcrumb"]/span)[last()]').text
            name = driver.find_element(
                "xpath", '//h1[@class="prod-name"]').text
    
            pd['name'] = name
    
            price = driver.find_element(
                "xpath", '//div[@id="product_price_brutto"]').get_attribute("data-default")
    
            pd['price'] = price
    
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
    
            # description
            desc = driver.find_element(
                "xpath", '//div[@class="panel-description"]')
    
            desc_html = desc.get_attribute('innerHTML')
    
            description_md = markdownify.markdownify(
                desc_html, heading_style="ATX")
    
            pd['description'] = {
                'markdown': description_md,
                'text': desc.text
            }
    
            products.append(pd)
    
            products_links_done.append(pd_link)
    
            with codecs.open(save_to, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False)
            with codecs.open(save_to_l_2, 'w', encoding='utf-8') as f:
                json.dump(products_links_done, f, ensure_ascii=False)
    
            print('Progress '+str(len(products_links_done)) +
                  '/'+str(len(products_links)))
        except (TimeoutException, NoSuchElementException) as ex:
            print("Exception has been thrown. " + str(ex))

print('Zapisywanie pliku do ' + save_to)

driver.close()
