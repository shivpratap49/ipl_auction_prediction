from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import json



def main(year):
    url="https://www.iplt20.com/stats/"+year
    # Initialize the WebDriver (make sure you have the right driver for your browser)
    driver = webdriver.Firefox()  # or webdriver.Chrome()

    # Open the target webpage
    driver.get(url)  # Replace with the actual URL

    # Wait for the cookie consent button to be present and clickable
    try:
        # Adjust the selector based on the actual button on the website
        cookie_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept cookies']"))
            # Replace with actual text or selector
        )
        cookie_button.click()  # Click to accept cookies

        print("Cookies accepted successfully!")
    except Exception as e:
        print(f"Error accepting cookies: {e}")
        # Wait for the 'View All' button to become clickable
    view_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@ng-click="showAllBattingStatsList()"]'))
    )

    # Click the 'View All' button






    # Click the link
    driver.execute_script("""
           var element = arguments[0];
           element.addEventListener('click', function(e) {
  return "undefined" != typeof S && S.event.triggered !== e.type ? S.event.dispatch.apply(t, arguments) : void 0
});
           element.click();  // Trigger the click to invoke the event
       """, view_all_button)
    print("Clicked the 'View All' button successfully.")
    time.sleep(5)
    stats_table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//table[@class="st-table statsTable ng-scope archiveseason"]'))
    )
    rows = stats_table.find_elements(By.TAG_NAME, 'tr')
    thead = stats_table.find_elements(By.TAG_NAME, "th")
    list1=[i.text for i in thead]
    list1.append('Year')
    list_json = []
    for row in rows[1:]:
        columns = row.find_elements(By.TAG_NAME, 'td')  # Extract columns from each row
        col = [col1.text for col1 in columns]  # Collect text from each column
        print(col)

        dict = {}
        for i in range(0, len(col)):
            dict[thead[i].text] = col[i]
            dict['Year']=url[-4:]
        list_json.append(dict)
    print(list_json)
    json_array = json.dumps(list_json)
    file_names='iplstats'+url[-4:]+'.csv'
    csv_file = file_names

    # Writing JSON to CSV
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:

        writer = csv.DictWriter(file, fieldnames=list1)

        writer.writeheader()

        for item in list_json:
            writer.writerow(item)

    print(f"Data written to {csv_file}")

        # element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#autab3-2022"]'))
        #     # Replace with your href
        # )
        # element.click()
        #elements = driver.find_element(By.CLASS_NAME, 'tab-n-view')
        # li=elements.find_elements(By.XPATH, '#autab3-2022')
        # for i in li:
        #     print(i.text)

        # Continue with other actions on the page
        # li_element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, 'li.some-class'))  # Adjust the selector as needed
        # )
        #
        # # Find the link (<a>) within the <li> element
        # link = li_element.find_element(By.TAG_NAME, 'a')

        # Click the link
        # link.click()


        # Close the driver
    driver.quit()


if __name__ == '__main__':

    list1=[str(i)for i in range(2008,2017)]
    list1.sort(reverse=True)
    for j in list1:
        main(j)

