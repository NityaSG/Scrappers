from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json


options = webdriver.ChromeOptions()
options.headless = True  
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


url = 'https://www.ogaan.com/just-in?sorting=new-arrival'


driver.get(url)


html = driver.page_source


soup = BeautifulSoup(html, 'html.parser')


product_list = soup.find('div', class_='listing product-listing')


product_details = []

if product_list:
   
    product_divs = product_list.find_all('div', class_=lambda value: value and value.startswith('listing-content plp-'))
    
    for div in product_divs:
        link = div.find('a')['href']
        if link:
            
            driver.get(link)
            time.sleep(1)  
            product_html = driver.page_source
            product_soup = BeautifulSoup(product_html, 'html.parser')

         
            title = product_soup.find('div', class_='sub-title').get_text(strip=True)
            image_div = product_soup.find('div', class_='big-image zoomimage')
            image = image_div['data-image'] if image_div and 'data-image' in image_div.attrs else None
            description_elements = product_soup.find('div', class_='para').find_all('li')
            description = ' '.join([li.get_text(strip=True) for li in description_elements])

    
            product_details.append({
                'title': title,
                'image': image,
                'description': description,
                'link': link
            })


for product in product_details:
    print(product)

output_file = "ogaan_products.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(product_details, file, indent=4, ensure_ascii=False)

print(f"Data saved to {output_file}")
driver.quit()
