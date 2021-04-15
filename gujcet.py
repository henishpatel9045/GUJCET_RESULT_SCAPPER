from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor
import time
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Edge()

starting_roll_number = int(input('Starting Roll Number: '))
ending_roll_number = int(input('Ending Roll Number: '))
driver.get('http://www.gseb.org/')
text_file = open('gujcet.txt', 'w')

for i in range(starting_roll_number, ending_roll_number + 1):
    action = ActionChains(driver)
    
    textbox = driver.find_element_by_xpath('//*[@id="studentnumber"]')
    submit_button = driver.find_element_by_xpath('//*[@id="middle"]/div/div/div[1]/center[1]/input[2]')
    
    action.click(textbox).send_keys(i).click(submit_button).perform()
    
    driver.switch_to_frame('marksheet')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    table = soup.findAll('table')
    try:
        extra = Extractor(table[0])
        extra.parse()
    
        text_file.write(f"""\n{i}-->
{extra.return_list()[0][0]}
{extra.return_list()[2][0]}
{extra.return_list()[3][0]}
{extra.return_list()[7][0]}
{extra.return_list()[9][0]}
""")
    except IndexError:
        print('Student number has problem.')
        pass
    
    driver.refresh()
    

text_file.close()
