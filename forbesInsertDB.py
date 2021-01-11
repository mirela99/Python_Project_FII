from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pymongo
from pymongo import MongoClient

url = "https://www.forbes.com/billionaires/"
driver = webdriver.Chrome('D:\\chromedriver\\chromedriver.exe')
driver.get(url)

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
except TimeoutException:
    print("Loading took just too much, sorry")
finally:
    print("Page loaded succesfully !")

page_source = driver.page_source

soup = BeautifulSoup(page_source, "html.parser")

name_list = []
names_selector = soup.find_all("div", class_="personName")
for name in names_selector:
    name_list.append(name.get_text())

print(name_list)

link_list = []
link_selector = soup.find_all("div", class_="bio-button-container")
for div in link_selector:
    link_list.append(div.a['href'])

print(link_list)
print(len(link_list))

peoples = []
for i in range(0, len(link_list)):
    page = requests.get(link_list[i])
    soup = BeautifulSoup(page.content, 'html.parser')

    for item in soup.select('.profile-stats'):
        person = {}
        score_list = []
        person['name'] = name_list[i + 1]

        age = item.find(text="Age")
        if age is None:
            person['age'] = ""
        else:
            person['age'] = age.find_next('span').contents[0]

        sourceOfWealth = item.find(text="Source of Wealth")
        if sourceOfWealth is None :
            person['sourceOfWealth'] = ""
        else:
            person['sourceOfWealth'] = sourceOfWealth.find_next('span').contents[0]

        selfScore = item.find(text="Self-Made Score")
        if selfScore is None:
            person['selfMadeScore'] = ""
        else:
            person['selfMadeScore'] = selfScore.find_next('span').contents[0]

        philanthropyScore = item.find(text="Philanthropy Score")
        if philanthropyScore is None:
            person['philanthropyScore'] = ""
        else:
            person['philanthropyScore'] = philanthropyScore.find_next('span').contents[0]

        residence = item.find(text="Residence")
        if residence is None:
            person['residence'] = ""
        else:
            person['residence'] = residence.find_next('span').contents[0]

        citizenship = item.find(text="Citizenship")
        if citizenship is None:
            person['citizenship'] = ""
        else:
            person['citizenship'] = citizenship.find_next('span', {}).contents[0]

        maritalStatus = item.find(text="Marital Status")
        if maritalStatus is None:
            person['maritalStatus'] = ""
        else:
            person['maritalStatus'] = maritalStatus.find_next('span').contents[0]
        children = item.find(text="Children")
        if children is None:
            person['children'] = ""
        else:
            person['children'] = children.find_next('span').contents[0]

        education = item.find(text="Education")
        if education is None:
            person['education'] = ""
        else:
            person['education'] = education.find_next('span').contents[0]

        peoples.append(person)

# conexiunea cu baza de datee
conn = MongoClient('mongodb://localhost:27017')
db = conn.forbesBillionaires
collection = db.people200

try:
    collection.insert_many(peoples)
    print(f'inserted {len(peoples)} profile info stats')
except:
    print('error, could not store')
