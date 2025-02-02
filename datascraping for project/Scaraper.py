from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import csv

def main():
    driver = webdriver.Firefox()
    driver.get("https://www.iplt20.com/auction/2024#https://documents.iplt20.com/ipl/franchises/1702465555_CSKroundbig.png")
    time.sleep(10)
    table = driver.find_element(By.ID, "equityStockTable")
    thead=table.find_element(By.TAG_NAME,"thead")

    list1=thead.text.split('\n')

    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    list_json=[]
    for ro in rows:
        if ro.text!="":

            col = ro.find_elements(By.TAG_NAME, "td")
            dict={}
            for i in range(0,len(list1)):
                dict[list1[i]]=col[i].text
            list_json.append(dict)
    print(list_json)
    json_array = json.dumps(list_json)
    csv_file = 'output.csv'

    # Writing JSON to CSV
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:

        writer = csv.DictWriter(file, fieldnames=list1)


        writer.writeheader()


        for item in list_json:
            writer.writerow(item)

    print(f"Data written to {csv_file}")

    driver.close()


if __name__ == '__main__':
    main()

