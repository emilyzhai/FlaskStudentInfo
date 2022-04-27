from flask import Flask,render_template,request
import pymysql
from werkzeug.utils import redirect

app = Flask(__name__)

def conn():
    con = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='db_test'
    )
    return con


#查询数据
@app.route('/studentlist')
def list():
    con =conn()
    sql = "select * from student"
    cur = con.cursor()
    cur.execute(sql)
    datas = cur.fetchall()
    cur.close()
    con.close()
    return render_template('studentlist.html',data=datas)

def insert_student(sno,name,sex,birthday,class1):
    con = conn()
    cur = con.cursor()
    sql = f"insert into student values({sno},'{name}','{sex}','{birthday}','{class1}')"
    print(sql)
    try:
        cur.execute(sql)
        con.commit()
    except:
        con.rollback()
    cur.close()
    con.close()

#插入数据
@app.route('/insert',methods=['GET','POST'])
def insert():
    if request.method == 'POST':
        sno = request.form.get('sno')
        name = request.form.get('name')
        sex = request.form.get('sex')
        birthday = request.form.get('birthday')
        class1 = request.form.get('class1')
        #插入数据
        insert_student(sno,name,sex,birthday,class1)
        return redirect('/studentlist')

    return  render_template('studentinsert.html')

#删除数据
@app.route('/delete')
def delete():
    sno = request.args.get('sno')
    con = conn()
    cur = con.cursor()
    sql = f"delete from student where sno={sno}"
    try:
        cur.execute(sql)
        con.commit()
    except:
        con.rollback()
    cur.close()
    con.close()
    return redirect('/studentlist')

def update_student(sno,name,sex,birthday,class1):
    sql = f"update student set name='{name}',sex='{sex}',birthday='{birthday}',class='{class1}' where sno={sno}"
    con = conn()
    cur = con.cursor()
    # print(sql)
    cur.execute(sql)
    try:
        cur.execute(sql)
        con.commit()
    except:
        con.rollback()
    cur.close()
    con.close()

#修改数据
@app.route('/update',methods=['GET','POST'])
def update():

    if request.method == 'POST':
        sno = request.form.get('sno')
        name = request.form.get('name')
        sex = request.form.get('sex')
        birthday = request.form.get('birthday')
        class1 = request.form.get('class1')
        #更新数据
        update_student(sno,name,sex,birthday,class1)
        return redirect('/studentlist')
    con = conn()
    cur = con.cursor()
    sno = request.args.get('sno')
    sql = f"select * from student where sno={sno}"
    cur.execute(sql)
    data = cur.fetchone()
    cur.close()
    con.close()
    return render_template('studentupdate.html',data=data)


@app.route('/')
def index():
    return "hello web"

if __name__ == '__main__':
    app.run(debug=True)