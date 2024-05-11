import pymysql

db = pymysql.connect(
    host='',
    user='',
    password="",
    database=""
)

cursor = db.cursor()

select_query =  "SELECT * FROM applicant"
cursor.execute(select_query)

# 결과 가져오기
results = cursor.fetchall()

# 결과 출력
for row in results:
    print(row)

# 연결 종료
db.close()