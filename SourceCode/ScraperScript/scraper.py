from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep 
from parsel import Selector
import re
import csv
import os
import sys

collection = []
users = {}

def backToGlobal():
	driver.get("https://www.linkedin.com/search/results/people/?origin=DISCOVER_FROM_SEARCH_HOME")

def returnQueries(query):
	search = driver.find_element_by_name('q')
	search.send_keys(query)
	search.send_keys(Keys.RETURN)
	urls = []

	wait = WebDriverWait(driver,20)
	page_counter=2
	links_counter=1
	# wait.until(EC.element_to_be_clickable((By.XPATH,'(//*[@id="gsr"][' + str(links_counter) + ']')))
	pages=driver.find_elements_by_xpath("//*[@id='nav']/tbody/tr/td/a")
	elem1=driver.find_elements_by_xpath("//h3[@class='r']/a")
	print(len(elem1))
	print(len(pages))
	driver.maximize_window()
	for page in pages:
		sleep(1)
		link = driver.find_elements_by_class_name('iUh30')
		# print("page")
		for thing in link:
			urls.append(thing.text)
		for e in elem1:
			my_link = driver.find_element_by_xpath("(//h3[@class='r']/a)[" + str(links_counter) + "]")
			my_link.click()
			driver.back()
			links_counter+=1
		my_page = driver.find_element_by_xpath("//a[text() = '" + str(page_counter) + "']")
		my_page.click()
		page_counter+=1

	return urls

def parse(collection):
	new_collection = []
	for item in collection:
		if "..." in item:
			continue
		text = item.replace(" › ", "/in/")
		text = '\"' + text + '\",' 
		new_collection.append(text)

	return new_collection

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

# TODO: finish thissssssssssssss
def collectUserData(user):
	driver.get(user)
	sleep(5)

	sel = Selector(text=driver.page_source)
	username = sel.xpath('//*[@id="ember48"]/div[2]/div[2]/div[1]/ul[1]/li[1]').extract_first()
	print(cleanhtml(username).strip())

	# more = driver.find_element_by_class_name("pv-skill-categories-section")
	# coordinates = more.location_once_scrolled_into_view
	# driver.execute_script('window.scrollTo({}, {});'.format(coordinates['x'], coordinates['y']))
	driver.execute_script("window.scrollBy(0, -150);")

	sleep(1)
	# sel = Selector(text=driver.page_source)
	skills = sel.xpath('//*[starts-with(@class, "pv-skill-category-entity__name-text")]/text()').extract()
	for skill in skills:
		print(cleanhtml(skill).strip())
	
profiles = {}
chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get('https://www.linkedin.com')


#login credentials
user = []
with open("credentials.txt", "r") as file:
	for line in file:
		user.append(line)


login = driver.find_element_by_class_name("nav__button-secondary")
login.click()

sleep(1)

username = driver.find_element_by_name("session_key")
username.send_keys(user[0])

password = driver.find_element_by_name("session_password")
password.send_keys(user[1])

sign_in = driver.find_element_by_class_name("btn__primary--large")
sign_in.click()

# backToGlobal()

driver.get('https:www.google.com')
sleep(2)

#'site:linkedin.com/in/ AND "Software Engineering"'
collection = returnQueries(input("enter query: "))
collection = parse(collection)
for thing in collection:
	print(thing)
	# collectUserData(thing)



#remove at final run time
driver.close()
