from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import requests 
import re
import bs4 as bs
import time
import xlwt
from xlwt import Workbook
import multiprocessing as mp

def find_player_rankings(player_list):
	ret = list()
	opts = Options()
	opts.add_argument('--headless')
	browser = webdriver.Chrome(service=Service('/Users/darren/Documents/Coding_projects/chromedriver'), options=opts)
	browser.get('https://www.juniorgolfscoreboard.com/junior-golf-rankings-display.asp?gender=B')
	browser.find_element(By.ID, 'ranking-1').click()
	browser.find_element(By.LINK_TEXT, 'X Close').click()

	for first_name, last_name in player_list:
		scoring_avg = 'NA'
		browser.find_element(By.CLASS_NAME, 'accordion-item-toggle').click()
		browser.implicitly_wait(10) #makes the search area actually open
		browser.find_element(By.NAME, 'FNAME').clear()
		browser.find_element(By.NAME, 'FNAME').send_keys(first_name)
		browser.find_element(By.NAME, 'LNAME').clear()
		browser.find_element(By.NAME, 'LNAME').send_keys(last_name)
		browser.find_element(By.NAME, 'submit').click()
		
		start_time = time.time()

		while (time.time()-start_time) < 1:
			try:
				scoring_avg = browser.find_element(By.CSS_SELECTOR, "table > tbody td[data-title='(65%) SCORING DIFF.']").text
				break
			except:
				break

		print(time.time()-start_time)

		#rank = browser.find_element(By.CSS_SELECTOR, "table > tbody > td[data-title='OVERALL']").text
		ret.append(scoring_avg)

	browser.close()

	return ret


def find_player_list(url):
	url = 'view-source:' + url
	ret = list()
	players = list()
	opts = Options()
	opts.add_argument('--headless')
	browser = webdriver.Chrome(service=Service('/Users/darren/Documents/Coding_projects/chromedriver'),options=opts)
	browser.get(url)
	html = browser.page_source
	page = bs.BeautifulSoup(html, 'lxml').get_text()
	players = re.findall(r'<span class=\"d-none d-md-inline\">(.{0,20})</span><span class="d-md-none">', page)
	players.pop(0)
	players.pop(0)
	for i in range(0, len(players)-1):
		s = players[i].split()
		fname = s[0]
		if '(' in players[i]:
			lname = s[2]
		else:
			lname = s[1]
		if ',' in lname:
			lname = lname[:len(lname)-1]
		ret.append((fname,lname))
	return ret




if __name__ == '__main__':
	start_time = time.time()
	url = input('Enter leaderboard URL: ')
	players = find_player_list(url)
	wb = Workbook()
	sheet1 = wb.add_sheet('Sheet 1')
	sheet1.write(0,0, 'First Name')
	sheet1.write(0,1, 'Last Name')
	sheet1.write(0,2, 'Scorring Diff.')
	sheet1.write(0,3, 'Ranking')

	scorings_avgs = find_player_rankings(players)

	for i in range(0,len(players)):
		sheet1.write(i+1,0,players[i][0])
		sheet1.write(i+1,1,players[i][1])
		sheet1.write(i+1,2,scorings_avgs[i])

	wb.save('t.xls')

	print('Total time: ' + str(time.time()-start_time))

