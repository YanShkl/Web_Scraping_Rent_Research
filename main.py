from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Variables what drives while loop
codeRun = True
looping_count = 1

# Creating empty DataFrame
df = pd.DataFrame(columns=["What's the id of the property?", "What's the address of the property?",
                           "What is the area of the property?", "What's the price per month/day?",
                           "What's the link to the property?"])

while codeRun:

    # If statement allows to drive page to scrap
    if looping_count == 1:
        link = 'https://www.ss.lv/en/real-estate/flats/riga/centre/today-5/hand_over/'
        looping_count += 1
    else:
        link = f'https://www.ss.lv/en/real-estate/flats/riga/centre/today-5/hand_over/page{looping_count}.html'
        looping_count += 1

    headers = {
        "Accept-Language": 'en-US',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'
    }

    response = requests.get(link, headers=headers)
    response.raise_for_status()

    print(response.status_code)

    # Detect if all pages are scraped
    if response.history:
        print('All pages are Scraped')
        codeRun = False
        break

    soup = BeautifulSoup(response.text, 'html.parser')

    # Finding necessary data block by id
    data = soup.find(id='filter_frm')

    # Selecting the desired range of data
    cleaned_data = data.find_all('tr')[3:33]

    list_of_ids = []
    list_of_links = []
    list_of_addresses = []
    list_of_prices = []
    list_of_m2 = []

    # Selecting and adding data to lists
    for listing in cleaned_data:

        try:
            link = 'https://www.ss.lv' + listing.find('a')['href']
            list_of_links.append(link)
        except TypeError:
            print('All pages are Scraped')
            codeRun = False
            break

        id = listing.get('id')
        list_of_ids.append(id)

        address = listing.find(class_='msga2-o pp6').text
        list_of_addresses.append(address)

        m2 = int(listing.find_all(class_='msga2-o pp6')[2].text)
        list_of_m2.append(m2)

        price = listing.find_all(class_='msga2-o pp6')[6].text
        list_of_prices.append(price)

    # time.sleep(1)

    xtra = {"What's the id of the property?": list_of_ids,
            "What's the address of the property?": list_of_addresses,
            "What is the area of the property?": list_of_m2,
            "What's the price per month/day?": list_of_prices,
            "What's the link to the property?": list_of_links
            }

    current_df = pd.DataFrame(xtra)

    # df = df.append(pd.DataFrame(xtra))
    df = pd.concat([df, current_df], ignore_index=True, axis=0)
    df.to_csv('SS.LV Research Data', index=False)

    # Selenium Working Area

    LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSepJF4-MQ5t5dEYIu8UEwPopKt3ZlAmYmk6ff5FvijiKwPuTg/viewform?usp=sf_link'
    chrome_driver_path = 'C:\Development\chromedriver.exe'
    ser = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=ser)
    driver.get(LINK)

    time.sleep(5)

    # Adding information to each Google Form row

    for property in range(len(list_of_prices)):
        print(property)

        id = driver.find_element(By.XPATH,
                                 '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        id.send_keys(list_of_ids[property])
        time.sleep(1.5)

        address = driver.find_element(By.XPATH,
                                      '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        address.send_keys(list_of_addresses[property])
        time.sleep(1.5)

        area = driver.find_element(By.XPATH,
                                   '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        area.send_keys(list_of_m2[property])
        time.sleep(1.5)

        price = driver.find_element(By.XPATH,
                                    '/html/body/div/div[2]/form/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
        price.send_keys(list_of_prices[property])
        time.sleep(1.5)

        link = driver.find_element(By.XPATH,
                                   '/html/body/div/div[2]/form/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input')
        link.send_keys(list_of_links[property])

        time.sleep(1.5)

        send = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()
        time.sleep(5)

        once_again = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()
        time.sleep(3)
