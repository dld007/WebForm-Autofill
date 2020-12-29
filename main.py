from selenium import webdriver
import time
from datetime import date
import sys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import configparser
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tkinter import *


def create_interface():
    #Window set-up
    root = Tk()
    root.geometry('510x150')
    root.winfo_toplevel().title("End of Shift Form Autofill")

    #Input box for shift time
    shiftTimeLabel = Label(root, text='Shift time: ', font=('Helvetica', 10))
    entryBox = Entry(root, width=30, font=('Helvetica', 10))

    #Create dropdown menu for Area Office
    areaLabel = Label(root, text='Area office worked (Leave blank if default):',font=('Helvetica', 10))
    areaVar = StringVar(root)
    areaVar.set(" ")  # default value
    areaOptions = OptionMenu(root, areaVar, "Cambridge", "Broun", "South Donahue", "Aubie", "Sasnett", "160 Ross")
    areaOptions.config(width=30, font=('Helvetica', 10))

    #Create checkbox for displaying webdriver
    checkVar = IntVar()
    chk = Checkbutton(root, text="Display form being filled", variable=checkVar)

    #Wrapper function for fill_form. Close window when form filling starts
    def fill_form_wrapper(event):
        area = areaVar.get()
        shiftTime = entryBox.get()
        showing = False if checkVar.get() == 0 else True
        root.destroy()
        fill_form(shiftTime, showing, area)

    #Create submit button and bind button click & return to fill_form_wrapper
    submitButton = Button(root, text='Enter')
    submitButton.bind('<Button-1>', fill_form_wrapper)
    root.bind('<Return>', fill_form_wrapper)

    #Format window
    shiftTimeLabel.grid(row=0,column=0)
    entryBox.grid(row=0, column=1)
    areaLabel.grid(row=1, column=0)
    areaOptions.grid(row=1, column=1)
    chk.grid(row=2, column=0)
    submitButton.grid(row=3, column=0)

    root.mainloop()


def fill_form(timeofshift, showing, officeofwork):
    sleepTime = 0.25
    # Format shift date, time, RA name, and RA area
    curDate = date.today().strftime("%m/%d")
    shiftTime = timeofshift
    shiftDateTime = curDate + ", " + shiftTime
    config = configparser.ConfigParser()
    config.read("settings.cnf")

    try:
        name = config['Settings']['name']
    except KeyError:
        print("Missing name from config file.")
        exit(-1)

    try:
        area = config['Settings']['area']
    except KeyError:
        print("Missing area from config file.")
        exit(-1)

    if officeofwork != " ":
        officeWorked = officeofwork
    else:
        officeWorked = config['Settings']['defaultOffice']

    # Instantiate webdriver and go to form
    driver = webdriver.Chrome()
    if showing is True:
        driver.maximize_window()
    else:
        driver.set_window_position(-10000, 0)
    driver.get("https://auburn.qualtrics.com/jfe/form/SV_6KEgNQ7fQh0wzkN")

    # Wait until page is visible
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.ID, "QR~QID6")))

    # Inputs
    driver.find_element_by_id("QR~QID6").send_keys(name)
    time.sleep(sleepTime)
    driver.find_element_by_id("QR~QID7").send_keys(shiftDateTime)
    time.sleep(sleepTime)
    select1 = Select(driver.find_element_by_id("QR~QID8"))

    try:
        select1.select_by_visible_text(area)
    except NoSuchElementException:
        print("Invalid area. Check spelling and/or capitalization.")
        driver.close()
        exit(-1)
    time.sleep(sleepTime)

    select = Select(driver.find_element_by_id("QR~QID9"))
    try:
        select.select_by_visible_text(officeWorked)  # Area office of completed shift
    except NoSuchElementException:
        print("Invalid area office. Check spelling and/or capitalization.")
        driver.close()
        exit(-1)
    time.sleep(sleepTime)

    driver.find_element_by_css_selector("label[for='QR~QID11~2']").click()
    time.sleep(sleepTime)
    driver.find_element_by_css_selector("label[for='QR~QID12~1']").click()
    time.sleep(sleepTime)
    driver.find_element_by_id("QR~QID12~1~TEXT").send_keys("0")
    time.sleep(sleepTime)
    driver.find_element_by_css_selector("label[for='QR~QID13~2']").click()
    time.sleep(sleepTime)
    driver.find_element_by_id("QR~QID14").send_keys("0")
    time.sleep(sleepTime)
    driver.find_element_by_id("QR~QID15").send_keys("Homework.")
    time.sleep(sleepTime)
    driver.find_element_by_id("NextButton").click()
    time.sleep(sleepTime)
    driver.close()
    exit(0)


def main():
    create_interface()


if __name__ == '__main__':
    main()
