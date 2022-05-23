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


def find_player(first_name, last_name):
	opts = Options()
	opts.add_argument('--headless')
	browser = webdriver.Chrome(service=Service('/Users/darren/Documents/Coding_projects/chromedriver'), options=opts)
	browser.get('https://www.juniorgolfscoreboard.com/junior-golf-rankings-display.asp?gender=B')
	browser.find_element(By.ID, 'ranking-1').click()
	browser.find_element(By.LINK_TEXT, 'X Close').click()

	browser.find_element(By.CLASS_NAME, 'accordion-item-toggle').click()
	browser.implicitly_wait(10) #makes the search area actually open
	browser.find_element(By.NAME, 'FNAME').send_keys(first_name)
	browser.find_element(By.NAME, 'LNAME').send_keys(last_name)
	browser.find_element(By.NAME, 'submit').click()
	
	scoring_avg = browser.find_element(By.CSS_SELECTOR, "table > tbody td[data-title='(65%) SCORING DIFF.']").text
	rank = browser.find_element(By.CSS_SELECTOR, "table > tbody > td[data-title='OVERALL']").text

	browser.close()

	return scoring_avg


def find_player_list(url):
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
	return players




if __name__ == '__main__':
	start_time = time.time()
	players = find_player_list('view-source:https://scpgajt.bluegolf.com/bluegolf/scpgajt22/event/scpgajt2257/contest/1/leaderboard.htm')
	wb = Workbook()
	sheet1 = wb.add_sheet('Sheet 1')
	sheet1.write(0,0, 'First Name')
	sheet1.write(0,1, 'Last Name')
	sheet1.write(0,2, 'Scorring Diff.')
	sheet1.write(0,3, 'Ranking')
	
	for i in range(1, len(players)-1):
		s = players[i].split()
		fname = s[0]
		if '(' in players[i]:
			lname = s[2]
		else:
			lname = s[1]

		try: 
			ret = find_player(fname, lname)
		except:
			ret = 'NA'

		sheet1.write(i,0,fname)
		sheet1.write(i,1,lname)
		sheet1.write(i,2,ret)

	wb.save('t.xls')

	print('Total time: ' + str(time.time()-start_time))

