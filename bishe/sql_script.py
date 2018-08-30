# _*_ coding:utf-8 _*_
import pymysql

db = pymysql.connect('localhost', 'root', '123456', 'bishe')
cursor = db.cursor()
for i in range(1, 600, 1):
    i = str(i)
    a = '题目' + i
    b = '选项a' + i
    d = '选项b' + i
    e = '选项c' + i
    f = '选项d' + i
    if int(i) % 4 == 0:
        g, c = 'a', '数学'
    elif int(i) % 4 == 1:
        g, c = 'b', '语文'
    elif int(i) % 4 == 2:
        g, c = 'c', '英语'
    else:
        g, c = 'd', '物理'
    sql = "insert into learn_question(question,option_A, option_B,\
    option_C, option_D, q_key, Q_subject) values ('%s', '%s','%s','%s','%s','%s', '%s')" % \
        (a, b, d, e, f, g, c)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print('出现错误已回滚', i)
db.close()
