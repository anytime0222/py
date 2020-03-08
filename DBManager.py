#db 처리 ,연결 , 해제 , 검색어 가져오기 , 데이터 삽 입
import pymysql as my

class DBHelper:
    '''
    멤버변수 : 커넥션
    '''
    conn = None

    '''
    생성자
    '''
    def __init__(self):
        self.db_init()
    '''
    멤버함수
    '''
    def db_init(self):
        self.conn = my.connect(
                        host='localhost',
                        user='root',
                        password='1234',
                        db='fortest',
                        charset='utf8',
                        cursorclass=my.cursors.DictCursor)
        
    def db_free(self):
        if self.conn:
            self.conn.close()

    def db_selectKeyword(self):

        rows = None    
        with self.conn.cursor() as cursor:
            # Read a single record
            sql = "SELECT	*	FROM	tbl_keyword"
            cursor.execute(sql)
            rows = cursor.fetchall()
            print(rows)       
        
        return rows

    def db_insertCrawlingData(self, title, price, area, contents, keyword):
        with self.conn.cursor() as cursor:
            sql = '''
            insert into  `tbl_crawlingdata`
            (title, price, area, contents, keyword)
            values( %s,%s,%s,%s,%s )
            '''
            cursor.execute(sql, (title, price, area, contents, keyword))
        self.conn.commit()


#단독으로 수행시에만 작동함 > 테스트 코드 삽입하여 사용
if __name__ =='__main__':
    db = DBHelper()
    print(db.db_selectKeyword())
    print(db.db_insertCrawlingData('1','2','3','4','5' ) )

    db.db_free()
