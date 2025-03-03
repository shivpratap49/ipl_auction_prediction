from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



def main():
    
    driver = webdriver.Firefox()  

    
    driver.get("https://www.iplt20.com/auction/2024")  


    try:

        cookie_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept cookies']"))

        )
        cookie_button.click()

        print("Cookies accepted successfully!")
    except Exception as e:
        print(f"Error accepting cookies: {e}")
    li_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'auction-tab-switch'))
    )

    
    link = li_element.find_element(By.TAG_NAME, 'a')

    
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
    teamlist = driver.find_elements(By.TAG_NAME, "")

    print(teamlist)


    driver.quit()


if __name__ == '__main__':


    main()

