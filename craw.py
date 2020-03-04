from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


main_url = 'http://tour.interpark.com/'
keyword = '로마'

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

            print('------------------------------------------')

    except Exception as e1:
        print('오류', e1)


#ㅎㅇ