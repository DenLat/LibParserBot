from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
import logging

config = configparser.ConfigParser()
config.read("config.ini")

def check_book_availability():
    url = config["site"]["url"]
    search_query = config["site"]["search_query"]

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        logging.info(f"Opened page: {url}")

        # Explicit wait for the search field to appear
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "Autosuggest"))
        )
        search_box.clear()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        logging.info(f"Search query sent: {search_query}")

        # Explicit wait for the first book's link to appear
        result_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".rList_col.rList_titel a"))
        )
        book_title = result_link.text
        logging.info(f"Book found: {book_title}")
        result_link.click()

        # Explicit wait for the availability table row to appear
        row = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr.rTable_tr_even"))
        )
        cells = row.find_elements(By.CSS_SELECTOR, "td.rTable_td_text")

        if len(cells) < 5:
            raise Exception("Not enough cells in the table row")

        # Extracting data
        library_name = cells[0].text.strip()
        location = cells[1].text.strip()
        signature = cells[2].text.strip()
        order_status = cells[3].text.strip()
        availability_info = cells[4].text.strip()

        # Creating message depending on the availability status
        if availability_info.lower().startswith("ausgeliehen"):
            availability_text = f"❌ '{book_title}' (Ausgeliehen)."
        else:
            availability_text = (
                f"📘 {book_title}\n"
                f"📍 Library: {library_name}\n"
                f"📚 Section: {location}\n"
                f"🆔 Signature: {signature}\n"
                f"🔒 Status: {order_status}\n"
                f"📅 Availability: {availability_info}"
            )

        return availability_text

    except Exception as e:
        logging.error(f"Parsing error: {e}")
        return None

    finally:
        driver.quit()
