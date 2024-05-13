import requests
from bs4 import BeautifulSoup
import json


base_url = "https://www.anitadongre.com"


url = "https://www.anitadongre.com/WOMEN/New-Arrivals?srule=new-arrivals&start=0&sz=30page=3"


response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")


product_divs = soup.find_all("div", class_="product-tile")


products = []
for product in product_divs:
    product_info = {}

 
    product_anchor = product.find("a", class_="product-tile__anchor")
    product_url = product_anchor.get('href') if product_anchor else None
    if product_url:
        product_info['url'] = base_url + product_url if product_url.startswith('/') else product_url

   
    product_image = product.find("img", class_="product-tile__image")
    product_info['image'] = product_image.get('data-src') if product_image else None

  
    if product_info.get('url'):
        product_response = requests.get(product_info['url'])
        product_soup = BeautifulSoup(product_response.content, "html.parser")

        
        product_title = product_soup.find("h1", class_="pdp__name heading-type fluid-type--hecto-h6 text-line--normal")
        product_info['title'] = product_title.text.strip() if product_title else None

        
        product_description = product_soup.find("div", class_="cms-generic-copy", attrs={"data-product-component": "longDescription-message"})
        product_info['description'] = product_description.text.strip() if product_description else None

    if product_info['url'] and product_info['image']:
        products.append(product_info)

print(json.dumps(products, indent=4))

output_file = "anitadongre_products.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(products, file, indent=4, ensure_ascii=False)

print(f"Data saved to {output_file}")
