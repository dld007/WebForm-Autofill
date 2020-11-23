from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import date
import sys
from selenium.webdriver.support.ui import Select

#Format shift date and time
date = date.today().strftime("%m/%d")
shiftTime = sys.argv[1]
shiftDateTime = date + ", " + shiftTime

#Instantiate webdriver and go to form
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://auburn.qualtrics.com/jfe/form/SV_6KEgNQ7fQh0wzkN")

#Inputs
driver.find_element_by_id("QR~QID6").send_keys("Dana Davis")
time.sleep(2)
driver.find_element_by_id("QR~QID7").send_keys(shiftDateTime)
time.sleep(2)
driver.find_element_by_id("QR~QID8~4").click()
time.sleep(2)
select = Select(driver.find_element_by_id("QR~QID9"))
select.select_by_visible_text(sys.argv[2]) #Area office of completed shift
time.sleep(2)
driver.find_element_by_css_selector("label[for='QR~QID11~2']").click()
time.sleep(2)
driver.find_element_by_css_selector("label[for='QR~QID12~1']").click()
time.sleep(2)
driver.find_element_by_id("QR~QID12~1~TEXT").send_keys("0")
time.sleep(2)
driver.find_element_by_css_selector("label[for='QR~QID13~2']").click()
time.sleep(2)
driver.find_element_by_id("QR~QID14").send_keys("0")
time.sleep(2)
driver.find_element_by_id("QR~QID15").send_keys("Homework.")
time.sleep(2)
driver.find_element_by_id("NextButton").click()
time.sleep(2)
driver.close()
