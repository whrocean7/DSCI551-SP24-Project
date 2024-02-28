import pymysql
from flask import Flask, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app=app)
app.debug = True
db = pymysql.connect(host='localhost', user='root', password='', database='dsci551')
cursor = db.cursor()  # create curosr


@app.route('/add', methods=['post'])
def add():
    req_data = request.get_data()
    data = json.loads(req_data)
    print(data)
    try:
        sql_data = (float(data['beer_ABV']), int(data['beer_beerId']), int(data['beer_brewerId']), data['beer_name']
                    , data['beer_style'], float(data['review_appearance']), float(data['review_palette']), float(data['review_overall'])
                    , float(data['review_taste']), data['review_profileName'], float(data['review_aroma']), data['review_text']
                    , int(data['review_time']))
        sql = "insert into beer(beer_ABV,beer_beerId,beer_brewerId,beer_name ,beer_style,review_appearance," \
              "review_palette,review_overall,review_taste,review_profileName,review_aroma," \
              "review_text,review_time) " \
              "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        cursor.execute(sql, sql_data)
        db.commit()
        return {'code': 200, 'msg': 'Add data success'}
    except Exception as e:
        print("error:", e)
        db.rollback()
        return {'code': 1000, 'msg': "Add data fail"}


@app.route('/del', methods=['delete'])
def delete():
    deleteId = request.args.get('beer_beerId')
    sql = f'delete from `beer` where beer_beerId="{deleteId}";'
    try:
        cursor.execute(sql)
        db.commit()
        return {'code': 200, 'msg': 'Delete success'}
    except Exception as e:
        print("error:", e)
        db.rollback()
        return {'code': 1000, 'msg': "Delete Fail"}


@app.route('/edit', methods=['put'])
def edit():
    req_data = request.get_data()
    data = json.loads(req_data)
    print('Change：', data)
    try:
        sql = f"update beer set review_text='{data['new_review']}' where beer_beerId='{data['id']}'"
        cursor.execute(sql)
        db.commit()
        return {'code': 200, 'msg': 'Update success'}
    except Exception as e:
        print("error:", e)
        db.rollback()
        return {'code': 1000, 'msg': "Update Fail"}


@app.route('/select', methods=['get'])
def select():
    try:
        cursor.execute("SELECT * FROM beer LIMIT 10")
        array = []
        data = ()
        while isinstance(data, tuple):  # do for loop to get data
            data = cursor.fetchone()  # fetchone to get single line of table
            if (data == None): break
            obj = {}
            obj['beer_ABV'] = data[0]
            obj['beer_beerId'] = data[1]
            obj['beer_brewerId'] = data[2]
            obj['beer_name'] = data[3]
            obj['beer_style'] = data[4]
            obj['review_appearance'] = data[5]
            obj['review_palette'] = data[6]
            obj['review_overall'] = data[7]
            obj['review_taste'] = data[8]
            obj['review_profileName'] = data[9]
            obj['review_aroma'] = data[10]
            obj['review_text'] = data[11]
            obj['review_time'] = data[12]

            array.append(obj)
        return {'code': 200, 'msg': 'Select Success!', 'data': array}
    except Exception as e:
        print("error: ", e)
        db.rollback()
        return {'code': 1000, 'msg': "select Fail"}


if __name__ == '__main__':
    app.run(host="localhost", port='8090')
    cursor.close()
    db.close()
