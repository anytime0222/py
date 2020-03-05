#상품정보 담는 클래스
class TourInfo:
    #멤버 변수(원하는 데이터들 다 생성해도됨.)
    title = ''
    price = ''
    area = ''
    link = ''
    img = ''

    #생성자
    def __init__(self, title, price, area, link, img):
        self.title = title
        self.price = price
        self.area = area
        self.link = link
#erg
    