from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import selenium 
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import random,os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
def writeToFile(links,company,date,month,year):
	try:
		os.makedirs('links')
	except Exception as e:
		pass
	
	f = open(os.path.join(BASE_PATH,"links","results_"+comp+"_"+sd+"_"+sm+"_"+sy+'.data'),'a+')
	for i,j in links:
		f.write(str(i)+"::"+str(j)+"\n")
		os.makedirs('data')
	except Exception as e:
		pass
	
	f = open(os.path.join(BASE_PATH,"data","results_"+comp+"_"+sd+"_"+sm+"_"+sy+'.data'),'a+')
	for i in links:
		f.write(str(i)+"\n")

	f.close()
driver_path = ''

if os.name == 'nt':
	driver_path = os.path.join(os.path.dirname(BASE_PATH),"Scripts")+'\chromedriver.exe'
elif os.name == 'posix':
	driver_path = os.environ['HOME']+'/beautiful_soup/chromedriver'
else:
	driver_path = None

print("#"*8+" Enter the details to scrape separated by SPACE.")
sd,sm,sy=input("Enter starting day month year ").split(" ")
ed,em,ey=input("Enter ending day month year ").split(" ")
webp=input("Enter website to scrape- ")
comp=input("Enter company data to scrape -")


driver = webdriver.Chrome(executable_path=driver_path)
driver.implicitly_wait(15)
start_url="https://www.google.co.in/search?num=100&biw=1040&bih=635&tbs=cdr%3A1%2Ccd_min%3A"+"{smonth}"+r"%2F"+"{sday}"+r"%2F"+"{syear}"+r"%2Ccd_max%3A"+"{emonth}"+r"%2F"+"{eday}"+r"%2F"+"{eyear}"+r"%2Csbd%3A1&tbm=nws&q=site%3A"+"{webpage}+%22{company}%22&&oq=site%3A{webpage}"+"%22{company}%22&gs_l=serp.3...0.0.0.1565.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.IfKqhHBbtbY"
driver.get(start_url.format(smonth=sm,sday=sd,syear=sy,emonth=em,eday=ed,eyear=ey,webpage=webp,company=comp))
data={}
date=[]
next_page=""
wait = WebDriverWait(driver, random.randint(10,20))
i=0
time.sleep(random.randint(8,13))
previous=next_page
try:
	while next_page is not None or previous is not None:
			if i >= 80:
				break
			time.sleep(random.randrange(20,30))
			list_links=[]
			dat = []
			time.sleep(random.randrange(15,20))
			list_links=[]
			try:
				next_page = wait.until(EC.element_to_be_clickable((By.ID,'navcnt')))
				next_page = driver.find_element_by_link_text('Next')
				element=driver.find_elements_by_xpath("*//h3/a")

				dat = driver.find_elements_by_xpath('//*[@id="rso"]/div/div/div/div/div[1]/span[3]')
			except Exception as e:
				print (e)
				next_page=None
				#this is for the last page when no next option will be available
				element=driver.find_elements_by_xpath("*//h3/a")

				dat = driver.find_elements_by_xpath('//*[@id="rso"]/div/div/div/div/div[1]/span[3]')
				
			for ele in element:
				list_links.append(ele.get_attribute("href"))
			
			for d in dat:
				date.append(d.text);

			data[i]=list_links
			list_links = zip(date,list_links)

			for ele in element:
				list_links.append(ele.get_attribute("href"))
			data[i]=list_links

			writeToFile(list_links,comp,sd,sm,sy)
			i+=1
			if next_page is not None:
				next_page.click()
			else:
				break
except Exception as e:
	print(e)

finally:
	print("*"*8+"Finished fetching all the urls"+"*"*8)
	count=0
	for i in data.keys():
		count+=len(data[i])
	print("#"*8+"Fetched "+str(count))