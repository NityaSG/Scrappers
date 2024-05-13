from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
# Setup Chrome and Selenium
options = webdriver.ChromeOptions()
options.headless = True  # Run in headless mode (no browser UI)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL of the page you want to scrape
url = 'https://www.azafashions.com/new?sort=new_arrivals'

# Use Selenium to get the page
driver.get(url)

# Get the HTML content after JavaScript execution
html = driver.page_source

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all section tags containing products
product_sections = soup.find_all('section')

# Prepare to store product details
product_details = []

# Extract links from each product section
for section in product_sections:
    a_tag = section.find('a', href=True)
    if a_tag:
        link = a_tag['href']
        full_link = f'https://www.azafashions.com{link}' if not link.startswith('http') else link
        
        # Navigate to product page
        driver.get(full_link)
        time.sleep(3)  # Wait a few seconds for the page to fully load
        product_html = driver.page_source
        product_soup = BeautifulSoup(product_html, 'html.parser')

        # Extract the title, image, and description
        # Note: You'll need to adjust these selectors based on actual page structure
        title = product_soup.find('h1').get_text(strip=True) if product_soup.find('h1') else 'No Title'
        image_tag = product_soup.find('img')
        image = image_tag['src'] if image_tag else 'No Image'
        description_tag = product_soup.find('div', class_='description')
        description = description_tag.get_text(strip=True) if description_tag else 'No Description'

        # Save details
        product_details.append({
            'title': title,
            'image': image,
            'description': description,
            'link': full_link
        })

# Print product details
for product in product_details:
    print(product)
output_file = "aza_fashion_products.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(product_details, file, indent=4, ensure_ascii=False)

print(f"Data saved to {output_file}")
driver.quit()
