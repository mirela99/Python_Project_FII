from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pymongo

url = "https://www.forbes.com/billionaires/"
driver = webdriver.Chrome('D:\\chromedriver\\chromedriver.exe')
driver.get(url)

try:
   element = WebDriverWait(driver,10).until(
      EC.presence_of_element_located((By.TAG_NAME, "h1"))
   )
except TimeoutException:
   print("Loading took just too much, sorry")
finally:
   print("Page loaded succesfully !")

page_source = driver.page_source

soup = BeautifulSoup(page_source, "html.parser")
name_list =[]
names_selector = soup.find_all("div", class_="personName")
for name in names_selector:
   name_list.append(name.get_text())

print(name_list)


link_list =[]
link_selector = soup.find_all("div", class_="bio-button-container")
for div in link_selector:
   link_list.append(div.a['href'])

print(link_list)
print(len(link_list))


people =[]
for i in range(0, len(link_list)):
   page = requests.get(link_list[i])
   soup = BeautifulSoup(page.content, 'html.parser')

   for item in soup.select('.profile-stats'):
      person= {}
      person['name'] = name_list[i+1]
      person['age'] = item.select_one('.profile-stats__text').get_text()
      people.append(person)


print(people)