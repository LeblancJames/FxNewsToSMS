from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re


def scrape():
    url = 'https://www.forexfactory.com/'

    driver = webdriver.Chrome()
    driver.get(url)
    event_list = []  # for df

    try:
        time = "12:00am"
        count = 0
        # get the table from the website
        table = driver.find_element(By.CLASS_NAME, 'calendar__table')
        for row in table.find_elements(By.TAG_NAME, "tr"):  # iterate through rows
            # list comprehension to get each cell's data and filter out empty cells
            row_data = list(
                filter(None, [td.text for td in row.find_elements(By.TAG_NAME, "td")]))

            if row_data == []:
                continue
            # get date and remove date from first row
            if count == 0:
                date = row_data[0].replace('\n', ' ')
                row_data.pop(0)
                count += 1

            # Check if the row_data contains a valid time (HH:mma format)
            if len(row_data) >= 1 and re.match(r'\d{1,2}:\d{2}[ap]m', row_data[0], re.IGNORECASE) or re.match(r'Tentative', row_data[0]) or re.match(r'All Day', row_data[0]):
                time = row_data[0]
                row_data.pop(0)

            # add impact
            impact_ele = row.find_element(
                By.CSS_SELECTOR, 'td.calendar__impact span')
            impact = impact_ele.get_attribute('title')
            row_data.insert(0, impact)
            row_data.insert(0, time)  # Add the time

            row_data = row_data[0:4]  # only get what you need

            [time, impact, currency, event] = row_data  # destructure

            event_item = {
                'time': time,
                'impact': impact,
                'currency': currency,
                'event': event,
            }

            event_list.append(event_item)

    except Exception as e:
        print(e)
    finally:
        driver.quit()

    df = pd.DataFrame(event_list)
    return df
