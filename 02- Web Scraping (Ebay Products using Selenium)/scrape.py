import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options



chrome_options = Options()
chrome_options.add_argument("--no-sandbox")  # 🔹 Disables sandbox (fixes permission issues)
chrome_options.add_argument("--disable-dev-shm-usage")  # 🔹 Prevents crashes
chrome_options.add_argument("--disable-gpu")  # 🔹 Avoids GPU issues
chrome_options.add_argument("--remote-debugging-port=9222")  # 🔹 Helps with debugging
chrome_options.add_experimental_option("detach", True)


service = Service()  # Update path to your ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# driver.get("https://www.ebay.com/str/oliviany/Jewelry-Watches/_i.html?_sacat=281")
driver.get("https://www.ebay.com/str/oliviany/Fine-Jewelry/_i.html?_sacat=4196")
# driver.get("https://www.ebay.com/str/oliviany/Crafts/_i.html?_sacat=14339")
csv_filename = "all_products_with_details.csv"

product_data = []


# ✅ Define Base URL
base_url = "https://www.ebay.com/str/oliviany/Fine-Jewelry/_i.html?_sacat=4196&_pgn={}&rt=nc&_tab=shop"

# ✅ Loop through all pages (10 to 16)
for page_num in range(1, 10):  
    csv_filename_page = f"csv-{page_num}.csv"  # ✅ Unique filename per page
    product_data = []  # ✅ Store products for the current page

    # ✅ Reinitialize WebDriver for each page (Prevents bot detection)
    driver = webdriver.Chrome()
    driver.get(base_url.format(page_num))  # Load the page
    time.sleep(3)  # Wait for the page to load

    print(f"Scraping Page {page_num}...")

    # ✅ Locate all product articles
    articles = driver.find_elements(By.CSS_SELECTOR, 
        "#mainContent .str-items-grid__container article.str-item-card.StoreFrontItemCard")

    for index, article in enumerate(articles, start=1):
        try:
            # ✅ Extract Product Name
            name_element = article.find_element(By.CSS_SELECTOR, 
                ".str-item-card__header-container .str-item-card__header h3 span span")
            product_name = name_element.text.strip()

            # ✅ Extract Product Price
            price_element = article.find_element(By.CSS_SELECTOR, 
                ".str-item-card__signals-container .str-item-card__signals .str-item-card__primary .str-item-card__property-displayPrice")
            product_price = price_element.text.strip()
            
            # ✅ Extract Product Image
            try:
                image_element = article.find_element(By.CSS_SELECTOR, ".str-item-card__property-image img")
                product_image = image_element.get_attribute("src")  # Get image link
            except Exception:
                product_image = "N/A"

            # ✅ Click Product Link (Open in New Tab)
            product_link = article.find_element(By.TAG_NAME, "a")
            product_link.send_keys(Keys.CONTROL + Keys.RETURN)  # Open in new tab
            driver.switch_to.window(driver.window_handles[1])  # Switch to new tab
            time.sleep(3)  # Wait for page to load

            # ✅ Extract Inner Details
            detail_section = driver.find_elements(By.CSS_SELECTOR, 
                ".ux-layout-section-evo.ux-layout-section--features .ux-layout-section-evo__item "
                ".ux-layout-section-evo__row .ux-layout-section-evo__col")

            product_details = {"Name": product_name, "Price": product_price, "Image": product_image}

            for detail in detail_section:
                try:
                    # ✅ Extract Label
                    label_element = detail.find_element(By.CSS_SELECTOR, 
                        ".ux-labels-values__labels .ux-textspans")
                    label = label_element.text.strip()

                    # ✅ Extract Value
                    value_element = detail.find_element(By.CSS_SELECTOR, 
                        ".ux-labels-values__values .ux-textspans")
                    value = value_element.text.strip()

                    product_details[label] = value
                except Exception:
                    continue

            # ✅ Extract Description from iframe
            try:
                driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="desc_ifr"]'))  # Switch to iframe
                description_element = driver.find_element(By.TAG_NAME, "body")  # Get full text inside iframe
                product_details["Description"] = description_element.text.strip()  # Store description
                driver.switch_to.default_content()  # Switch back to main content
            except Exception:
                product_details["Description"] = "N/A"

            # ✅ Store Product Data
            product_data.append(product_details)

            # ✅ Close Product Page and Return to Main Page
            driver.close()
            driver.switch_to.window(driver.window_handles[0])  # Switch back to main tab
            time.sleep(2)

        except Exception:
            print(f"Product {index}: Data not found")

    # ✅ Save Current Page Data to CSV
    with open(csv_filename_page, mode="w", newline="", encoding="utf-8") as file:
        headers = set()
        for product in product_data:
            headers.update(product.keys())
        headers = list(headers)

        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()  # Write column headers
        writer.writerows(product_data)  # Write product data

    print(f"✅ CSV file '{csv_filename_page}' saved successfully!")

    # ✅ Quit WebDriver AFTER Each Page (To Avoid Bot Detection)
    driver.quit()

    # ✅ Random Sleep to Mimic Human Behavior (Avoid Detection)
    time.sleep(5)  