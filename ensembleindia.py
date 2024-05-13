from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

options = webdriver.ChromeOptions()
options.headless = True  # Run in headless mode
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = 'https://www.ensembleindia.com/new-now/men.html'

driver.get(url)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

product_list = soup.find('div', class_='listing-product')

product_details = []

if product_list:
    # Find all divs that contain individual products
    product_divs = product_list.find_all('div', class_=lambda value: value and value.startswith('product product-list'))
    
    for div in product_divs:
        link_element = div.find('a')
        if link_element and 'href' in link_element.attrs:
            link = link_element['href']
            driver.get(link)
            time.sleep(3)  # Wait for the page to load
            
            product_html = driver.page_source
            product_soup = BeautifulSoup(product_html, 'html.parser')
            
            # Extract the title
            title_element = product_soup.find('div', class_='product-head').find('a', class_='note')
            title = title_element.text.strip() if title_element else "Title Not Found"
            
            # Extract the image
            image_element = product_soup.find('div', class_='img-slot swiper-slide swiper-slide-active')
            image = image_element.find('img')['src'] if image_element and image_element.find('img') else "Image Not Found"
            
            # Extract the description
            description_element = product_soup.find('div', class_='ensem-product-detail').find('div', class_='text')
            description = description_element.text.strip() if description_element else "Description Not Found"
            
            # Save details
            product_details.append({
                'title': title,
                'image': image,
                'description': description,
                'link': link
            })

# Optionally, save the data to a JSON file
with open('product_details.json', 'w') as f:
    json.dump(product_details, f, indent=4)



# Print product details
for product in product_details:
    print(product)

output_file = "ensembleindia_products.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(product_details, file, indent=4, ensure_ascii=False)

print(f"Data saved to {output_file}")
driver.quit()
