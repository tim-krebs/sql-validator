from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import tkinter as tk


# Open browser
driver = webdriver.Edge()
driver.get('https://www.coderstool.com/sql-syntax-checker/')
driver.find_element(By.ID, 'in_file').send_keys('C:\\Users\\timkrebs\\Desktop\\test.sql')
driver.find_element(By.XPATH, '//button[@type="Submit"]').send_keys(Keys.ENTER)

content = driver.find_element(By.ID, 'editorOut').text
#driver.find_element(By.ID, 'out_copy_data').send_keys(Keys.ENTER)


trans_dict = {49: None, 10: None, 50: None, 10: None, 51: None, 10: None, 91: None, 10: None}

content.replace('1','')

print(content)


driver.close()

# Get data from clipboard
#win32clipboard.OpenClipboard()
#filename_format = win32clipboard.RegisterClipboardFormat('FileName')
#data = win32clipboard.GetClipboardData(filename_format).decode('utf-8')
#win32clipboard.CloseClipboard()
#1\n2\n3\n[\n 