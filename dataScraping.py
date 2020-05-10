import numpy as np 
import pandas as pd
from selenium import webdriver

def extractRouteData():
	driver = webdriver.Chrome()
	driver.get('https://www.14ers.com/php14ers/loginviaforum.php')

	uName = 'fsun71'
	pwd = 'Zh8fgj0q'

	uNameField = driver.find_element_by_name('username')
	pwdField = driver.find_element_by_name('password')
	loginBtn = driver.find_element_by_name('submit')

	uNameField.send_keys(uName)
	pwdField.send_keys(pwd)
	loginBtn.click()

	driver.get('https://www.14ers.com/php14ers/gps_downloads.php')

	parentMountains = []
	shortNames = []
	longNames = []

	routeMetaDF = pd.DataFrame(columns = ['Parent Mountain', 'Short Name', 'Long Name'])

	for i in range(1, 200):
		try:
			gpxRequest = driver.find_element_by_xpath("//table[@id = 'resultsTable']/tbody/tr[" + str(i) +"]/td[3]/a")
			gpxRequest.click()

			gpxConfirmDialogue = driver.find_element_by_xpath("//div[@class = 'ui-dialog-buttonset']/button[1]")
			gpxConfirmDialogue.click()

			mountain = driver.find_element_by_xpath("//table[@id = 'resultsTable']/tbody/tr[" + str(i) +"]/td[1]/a").text
			longName = driver.find_element_by_xpath("//table[@id = 'resultsTable']/tbody/tr[" + str(i) +"]/td[2]/a").text
			routeNameURL = driver.find_element_by_xpath("//table[@id = 'resultsTable']/tbody/tr[" + str(i) +"]/td[2]/a").get_attribute('href')

			if mountain != '':
				parentMountain = mountain

			shortName = routeNameURL.split('=')[1].split('&')[0]

			parentMountains.append(parentMountain)
			shortNames.append(shortName)
			longNames.append(longName)

			print('GPX file successfully acquired for ' + longName)
		
		except:
			pass

	routeMetaDF['Parent Mountain'] = parentMountains
	routeMetaDF['Short Name'] = shortNames
	routeMetaDF['Long Name'] = longNames

	routeMetaDF.to_csv('data/routeMeta.csv')

extractRouteData()