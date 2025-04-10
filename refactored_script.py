import logging
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import urllib.parse
import re
import os

logging.basicConfig(
    filename='whatsapp_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

invalid_logger = logging.getLogger('invalid_numbers')
invalid_logger.setLevel(logging.INFO)
invalid_handler = logging.FileHandler('invalid_numbers.log')
invalid_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
invalid_logger.addHandler(invalid_handler)

def setup_driver():
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    service = Service("./msedgedriver.exe")
    return webdriver.Edge(service=service, options=edge_options)

def load_phone_numbers(file_path):
    try:
        extention = file_path.split(".")[-1]
        if extention == "xlsx":
            df = pd.read_excel(file_path)
        elif extention == "csv":
            df = pd.read_csv(file_path)
        logging.info("Successfully loaded the CSV file.")
        print("Successfully loaded the CSV file.")
        return df["Phone Number"].astype(str).tolist()
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        print(f"Error reading CSV file: {e}")
        return None

def validate_phone_number(phone):
    pattern = re.compile(r"^1[0-9]{9}$")
    return bool(pattern.match(str(phone)))

def load_processed_numbers(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return {line.strip() for line in file}
    return set()

def save_processed_number(file_path, phone_number):
    with open(file_path, 'a') as file:
        file.write(f"{phone_number}\n")

def send_whatsapp_message(driver, phone_number, encoded_message):
    try:
        logging.info(f"Processing phone number: +20{phone_number}")
        print(f"Processing phone number: +20{phone_number}")
        url = f"https://api.whatsapp.com/send?phone=+20{phone_number}&text=" + encoded_message
        driver.get(url)
        return True
    except Exception as e:
        logging.error(f"Error with phone number +20{phone_number}: {e}")
        print(f"Error processing +20{phone_number}: {e}")
        return False

def process_numbers(driver, valid_numbers, processed_numbers_file, encoded_message):
    processed_numbers = load_processed_numbers(processed_numbers_file)
    iteration_count = 0
    flag = True

    for phone_number in valid_numbers:
        if phone_number in processed_numbers:
            logging.info(f"Skipping already processed phone number: +20{phone_number}")
            print(f"Skipping already processed phone number: +20{phone_number}")
            continue

        if send_whatsapp_message(driver, phone_number, encoded_message):
            try:
                if flag:
                    input("Accept WhatsApp API and press enter to continue...")
                    flag = False

                if not validate_phone_number(phone_number):
                    logging.warning(f"Invalid phone number format: {phone_number}")
                    print(f"Invalid phone number format: {phone_number}")
                    continue  

                WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@title='Share on WhatsApp']"))
                ).click()

                WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='use WhatsApp Web']"))
                ).click()

                WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send']"))
                ).click()

                logging.info(f"Message sent successfully to +20{phone_number}")
                print(f"Message sent successfully to +20{phone_number}")
                save_processed_number(processed_numbers_file, phone_number)
                iteration_count += 1

                if iteration_count % 7 == 0:
                    logging.info("Pausing for 5 seconds after 7 iterations.")
                    print("Pausing...")
                    time.sleep(1)

            except Exception as e:
                logging.error(f"Error while sending message to +20{phone_number}: {e}")
                print(f"Error sending to +20{phone_number}: {e}")

if __name__ == "__main__":
    separator = "\n" + "=" * 50 + f" NEW RUN STARTED: {time.strftime('%Y-%m-%d %H:%M:%S')} " + "=" * 50 + "\n"
    logging.info(separator)

    phone_numbers_file = 'New Microsoft Excel Worksheet.csv'
    processed_numbers_file = 'processed_numbers.txt'

    message = '''
    test message
    '''
    encoded_message = urllib.parse.quote(message)

    phone_numbers = load_phone_numbers(phone_numbers_file)
    if phone_numbers is None:
        print("No phone numbers. Exiting...")
        exit()

    valid_numbers = []
    for num in phone_numbers:
        if validate_phone_number(num):
            valid_numbers.append(num)
        else:
            invalid_logger.info(f"Invalid phone number: {num}")
            print(f"Invalid phone number logged: {num}")

    valid_numbers = [num for num in phone_numbers if validate_phone_number(num)]

    if not valid_numbers:
        print("No valid phone numbers. Exiting...")
        exit()

    driver = setup_driver()
    driver.get("https://web.whatsapp.com/")
    input("Please scan the QR code and press Enter to continue...")

    process_numbers(driver, valid_numbers, processed_numbers_file, encoded_message)

    logging.info("All phone numbers processed. Exiting...")
    print("Exiting...")
    time.sleep(5)
    driver.quit()