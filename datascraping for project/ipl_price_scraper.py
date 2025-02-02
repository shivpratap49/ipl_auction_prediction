from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import json



def main():

    driver = webdriver.Firefox()  # or webdriver.Chrome()
    url="https://www.iplt20.com/auction/2013"

    driver.get(url)  # Replace with the actual URL


    try:

        cookie_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept cookies']"))
            # Replace with actual text or selector
        )
        cookie_button.click()  # Click to accept cookies

        print("Cookies accepted successfully!")
    except Exception as e:
        print(f"Error accepting cookies: {e}")
    li_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'auction-tab-switch'))
    )

    # Find the <a> tag within the <li> element
    link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#autab35"]'))
            # Replace with your href
         )


    driver.execute_script("""
           var element = arguments[0];
           element.addEventListener('click', function(e) {
               e.preventDefault();
               v._jQueryInterface.call($(element), 'show');
           });
           element.click();  // Trigger the click to invoke the event
       """, link)
    time.sleep(5)
    tablelist = driver.find_elements(By.ID, "t1")
    list_json = []
    for table in tablelist:
        thead = table.find_element(By.TAG_NAME, "thead")

        list1 =['PLAYER','NATIONALITY','TYPE','PRICE PAID','Year']


        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        print(tbody.text)

        for ro in rows:
            if ro.text != "":

                col = ro.find_elements(By.TAG_NAME, "td")
                dict = {}
                for i in range(0, len(col)):
                    dict[list1[i]] = col[i].text
                dict['Year']=url[-4:]
            list_json.append(dict)
    print(list_json)
    json_array = json.dumps(list_json)
    file_name='ipl'+url[-4:]+'.csv'
    csv_file = file_name


    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:

        writer = csv.DictWriter(file, fieldnames=list1)

        writer.writeheader()

        for item in list_json:
            writer.writerow(item)

    print(f"Data written to {csv_file}")


    driver.quit()


if __name__ == '__main__':


    main()

