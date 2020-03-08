from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from DBManager import DBHelper as Db

from bs4 import BeautifulSoup as bs


import time
from Tour import TourInfo

db = Db() 
main_url = 'http://tour.interpark.com/'
keyword = '로마'
#상품 정보 담는 TourInfo 리스트
tour_list = []

driver = wd.Chrome(executable_path='chromedriver.exe')

driver.get(main_url)

driver.find_element_by_id('SearchGNBText').send_keys(keyword)

driver.find_element_by_css_selector('button.search-btn').click()


try:
    element = WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located( (By.CLASS_NAME, 'oTravelBox'))

    )
except Exception as e:
    print('오류발생',e)

#여행정보 페이지로 이동
driver.find_element_by_css_selector('.oTravelBox>.boxList>.moreBtnWrap>.moreBtn').click()


#리스트 페이징 스크립트 실행 searchModule.SetCategoryList(2, '')
for page in range(1,2):
    try:
        driver.execute_script("searchModule.SetCategoryList(%s, '')" % page)
        time.sleep(2)
        print("%s 페이지이동" %page)

        #페이지 이동하면서 크롤링
        #크롤링 할 때 데이터 확인하기.
        
        try:
            element = WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located( (By.CLASS_NAME, 'oTravelBox'))

            )
        except Exception as e:
            print('오류발생',e)
            
        boxItems = driver.find_elements_by_css_selector('.oTravelBox>.boxList>li')
        
        for li in boxItems:

            print('썸네일 : ' ,li.find_element_by_css_selector('img').get_attribute('src'))
            print('링크  : ' ,li.find_element_by_css_selector('a').get_attribute('onclick'))
            print('상품명 : ' , li.find_element_by_css_selector('h5.proTit').text)
            print('코멘트 : ' , li.find_element_by_css_selector('p.proSub').text)
            print('기간 : ' , li.find_element_by_css_selector('p.proInfo').text)

            for info in li.find_elements_by_css_selector('.info-row .proInfo'):
                print( info.text)

            print('금액 : ' , li.find_element_by_css_selector('strong.proPrice').text)

            print('------------------------------------------')

            #데이터 모음 (Tour에 삽입)
            obj = TourInfo(
                li.find_element_by_css_selector('h5.proTit').text,
                li.find_element_by_css_selector('strong.proPrice').text,
                li.find_elements_by_css_selector('.info-row .proInfo')[1].text,
                li.find_element_by_css_selector('a').get_attribute('onclick'),
                li.find_element_by_css_selector('img').get_attribute('src')
             )
            tour_list.append( obj )

    except Exception as e1:
        print('오류', e1)

print( tour_list,len(tour_list))

#수집한 정보의 갯수만큼 루프 / 페이지 방문 / 콘텐츠 획득 > db
for tour in tour_list:
    print( type(tour) )

    #링크 데이터에서 (새창이 뜸) 실 데이터 획득
    #분해
    arr = tour.link.split(',')

    if arr:
        #대체
        link = arr[0].replace('searchModule.OnClickDetail(','')

        #슬라이싱 >>> 앞의 ', 뒤에 ' 를 제거함
        detail_url = link[1:-1]

        driver.get( detail_url )

        time.sleep(2)

        #현재 페이지를 bs의 dom으로 구성
        soup = bs(driver.page_source,'html.parser')

        #여행상세정보 페이지에서 schedule 정보 긁기
        data = soup.select('.tip-cover')

        print( type(data) , len(data))



        #디비에 입력함
        content_final = ''
        for c in data[0].contents:
            content_final = str(c)


        db.db_insertCrawlingData(
            tour.title,
            tour.price,
            tour.area,
            content_final,
            keyword
        )





#종료
driver.close()
driver.quit()
import sys
sys.exit()