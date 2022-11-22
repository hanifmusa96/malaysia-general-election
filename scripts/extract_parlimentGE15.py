from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import re
import os

options=webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver=webdriver.Chrome('/usr/bin/chromedriver',chrome_options=options)

driver.get('https://www.myundi.com.my/pru15/johor/parlimen')
page_source=driver.page_source
list_states_html=BeautifulSoup(page_source,'lxml')
list_state=[]
for urls_state in list_states_html.find_all('a',class_=re.compile('rtitle d-flex align-items-center position-relative py-20-px border-bottom px-1')):
    list_state.append(urls_state['href'])

list_state.pop(0) #remove first subdomain "/parlimen"
# list_state=['/pru15/wp-labuan/parlimen/labuan']
# list_state=['/pru15/wp-kuala-lumpur/parlimen']

file_dir = os.path.dirname(os.path.realpath('__file__'))
file_name=file_dir+'/results/parliment_ge15.csv'


with open(file_name, 'w+') as f:
    writer=csv.writer(f)
    writer.writerow(('State', 'Parliment', 'Name', 'Party', 'Vote', 'Result'))

    for url_state in list_state:
        driver.get('https://www.myundi.com.my' + url_state)
           
        page_source=driver.page_source
        soup=BeautifulSoup(page_source,'lxml')
        if ((url_state != '/pru15/wp-labuan/parlimen/labuan') & (url_state != '/pru15/wp-putrajaya/parlimen/putrajaya')):
            
            reviews_selector=soup.find_all('div',class_='h-100 mb-2 p-3 bg-menang') #will collect all location 

            for i in range(len(reviews_selector)):
                location=reviews_selector[i].find_all('h5', class_='mb-2 text-uppercase title-dun') #will select 1 location from list
                candidates_all=reviews_selector[i].find_all('div', class_='text-uppercase title-calon') #will select all candidates that compete at particular location
                votes=reviews_selector[i].find_all('div', class_='px-1 rasmi-vote') #collect all votes in particular location
                results=reviews_selector[i].find_all('div', class_='px-2 text-right text-success text-uppercase title-calon font-weight-bold')

                for j in location:
                    for count,candidate in enumerate(candidates_all): #info on each candidate (name, party, no. of votes)
                        parliment=j.contents[4]
                        party=candidate.next_sibling
                        candidate=candidate.contents[0]
                        party=party.contents[0]
                        no_of_votes=re.sub(r",", '',votes[count].contents[-1])
                        state=re.sub(r"\-", ' ',url_state.split('/')[2])

                        if state=='wp kuala lumpur':
                            state='W.P Kuala Lumpur'

                        try:
                            result=results[count].contents[0]
                        except:
                            result='Kalah'

                        writer.writerow((state.title(), parliment.title(), candidate.title(), party.title(), no_of_votes, result.title()))

        else:
            reviews_selector=soup.select('div.stitle.d-flex.align-items-center.justify-content-between')
            location=soup.select('div.title.d-flex.align-items-center h1')[0].contents[0]

            for i in range(len(reviews_selector)):
                candidate=reviews_selector[i].select('div .col-lg-4.text-left h4')[0].contents[0]
                party=reviews_selector[i].select('div.col-lg-4.text-center.text-uppercase')[0].contents[1]
                votes=reviews_selector[i].select('div.col-lg-3.text-right title')
                list_r=reviews_selector[i].select('div.col-lg-3.text-right p')

                if (len(list_r)>1):
                    no_of_votes=list_r[1].select('b')[0].contents[0]
                    result=list_r[0].select('b')[0].contents[0]
                    print
                else:
                    no_of_votes=list_r[0].select('b')[0].contents[0]
                    result='Kalah'

                writer.writerow((location.title(), location.title(), candidate.title(), party.title(), no_of_votes, result.title()))