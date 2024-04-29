# import pymysql
# from flask import Flask, request, render_template, jsonify
# import json
# from flask_cors import CORS
# import hashlib
# import uuid

# app = Flask(__name__, static_url_path='/static')
# CORS(app=app)
# app.debug = True
# db1 = pymysql.connect(host='localhost', user='root', password='hhwswhrO1209', database='ratemybeer1')
# db2 = pymysql.connect(host='localhost', user='root', password='hhwswhrO1209', database='ratemybeer2')
# cursor1 = db1.cursor()  # create curosr
# cursor2 = db2.cursor()  # create curosr




# def hash_uuid(uuid_str):
#     # use SHA-256 hash function
#     hash_value = hashlib.sha256(uuid_str.encode()).hexdigest()
#     # int last character
#     last_digit = int(hash_value[-1], 16)
#     # do hash
#     if last_digit % 2 == 0:
#         return "db1"
#     else:
#         return "db2"




# @app.route('/add_review', methods=['POST'])
# def add_review():
#     # get review
#     data = request.json

#     # check data
#     if 'beername' not in data or 'beertype' not in data or 'review_text' not in data or 'rating' not in data:
#         return jsonify({"error": "beername, beertype, review_text, and rating are required"}), 400

#     # extract data
#     beername = data['beername']
#     beertype = data['beertype']
#     review_text = data['review_text']
#     rating = data['rating']

#     # extract beer from either beer table
#     cursor1.execute("SELECT beer_id FROM beer WHERE beer_name = %s AND beer_type = %s", (beername, beertype))
#     existing_beer = cursor1.fetchone()

#     if not existing_beer:
#         # if it's a new beer
#         beer_id = str(uuid.uuid4())  # 使用 uuid 库生成唯一的 beer_id
#         cursor1.execute("INSERT INTO beer (beer_id, beer_name, beer_type) VALUES (%s, %s, %s)",
#                        (beer_id, beername, beertype))
#         db1.commit()
#         cursor2.execute("INSERT INTO beer (beer_id, beer_name, beer_type) VALUES (%s, %s, %s)",
#                         (beer_id, beername, beertype))
#         db2.commit()
#     else:
#         # if it's a existing beer
#         beer_id = existing_beer[0]
#     print(beer_id, "aaaaaaa")

#     # generate uuid
#     review_id = str(uuid.uuid4())
#     db_name = hash_uuid(review_id)
#     print(db_name, 'bbbbbbb')
#     if db_name == 'db1':
#         # insert into db1
#         cursor1.execute("INSERT INTO Review (review_id, beer_id, review_text, rating) VALUES (%s, %s, %s, %s)",
#                         (review_id, beer_id, review_text, rating))
#         db1.commit()
#         return jsonify({"message": "Review added into db1 successfully"})
#     else:
#         # insert into db2
#         cursor2.execute("INSERT INTO Review (review_id, beer_id, review_text, rating) VALUES (%s, %s, %s, %s)",
#                         (review_id, beer_id, review_text, rating))
#         db2.commit()
#         return jsonify({"message": "Review added into db2 successfully"})



# @app.route('/delete_review', methods=['DELETE'])
# def delete_review():
#     # get data
#     data = request.json

#     # check review_id
#     if 'review_id' not in data:
#         return jsonify({"error": "review_id is required"}), 400

#     # extract review_id
#     review_id = data['review_id']

#     # find out which database to operate
#     assigned_db = hash_uuid(review_id)

#     # delete review data
#     if assigned_db == "db1":
#         db_connection = db1
#         db_name = "db1"
#     else:
#         db_connection = db2
#         db_name = "db2"

#     cursor = db_connection.cursor()

#     # construct SQL
#     delete_query = "DELETE FROM Review WHERE review_id = %s"

#     # execute SQL
#     cursor.execute(delete_query, (review_id,))
#     db_connection.commit()

#     return jsonify({"message": f"Review deleted successfully from {db_name}"})




# @app.route('/update_review', methods=['POST'])
# def update_review():
#     # get data
#     data = request.json

#     # check review_id
#     if 'review_id' not in data:
#         return jsonify({"error": "review_id is required"}), 400

#     # extract data
#     review_id = data['review_id']
#     review_text = data.get('review_text')
#     rating = data.get('rating')

#     # find out which to operate
#     assigned_db = hash_uuid(review_id)

#     # update review
#     if assigned_db == "db1":
#         db_connection = db1
#     else:
#         db_connection = db2

#     cursor = db_connection.cursor()

#     # construct SQL
#     update_query = "UPDATE Review SET "
#     update_values = []

#     if review_text:
#         update_query += "review_text = %s, "
#         update_values.append(review_text)
#     if rating:
#         update_query += "rating = %s, "
#         update_values.append(rating)

#     # delete last ","
#     update_query = update_query.rstrip(', ')

#     # add filter
#     update_query += " WHERE review_id = %s"
#     update_values.append(review_id)

#     # execute
#     cursor.execute(update_query, update_values)
#     db_connection.commit()

#     return jsonify({"message": f"Review updated successfully in {assigned_db}"})


# @app.route('/select', methods=['GET'])
# def select():
#     # get filter
#     filter_data = request.args

#     # construct SQL
#     sql_query = "SELECT Review.review_id, Review.beer_id, beer.beer_name, beer.beer_type, Review.review_text, Review.rating FROM Review INNER JOIN beer ON Review.beer_id = beer.beer_id"

#     # construct filter
#     conditions = []
#     values = []

#     if 'beer_name' in filter_data:
#         conditions.append("beer.beer_name = %s")
#         values.append(filter_data['beer_name'])

#     if 'beer_type' in filter_data:
#         conditions.append("beer.beer_type = %s")
#         values.append(filter_data['beer_type'])

#     if 'rating_min' in filter_data:
#         conditions.append("Review.rating >= %s")
#         values.append(filter_data['rating_min'])

#     if 'rating_max' in filter_data:
#         conditions.append("Review.rating <= %s")
#         values.append(filter_data['rating_max'])

#     if conditions:
#         sql_query += " WHERE " + " AND ".join(conditions)

#     # add limit condition
#     if 'limit' in filter_data:
#         limit = int(filter_data['limit'])
#         sql_query += " LIMIT %s"
#         values.append(limit)

#     # execute
#     cursor1.execute(sql_query, values)
#     results_db1 = cursor1.fetchall()
#     cursor2.execute(sql_query, values)
#     results_db2 = cursor2.fetchall()

#     # 合并两个数据库的结果
#     merged_results = results_db1 + results_db2

#     return jsonify(merged_results)


# @app.route('/')
# def index():
#     return render_template('index.html')



# if __name__ == '__main__':
#     app.run(host="localhost", port='8090')
#     cursor1.close()
#     db1.close()


import pymysql
from flask import Flask, request, jsonify, render_template
import hashlib
import uuid
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
CORS(app)
app.config['DEBUG'] = True

def get_db_connection():
    connection1 = pymysql.connect(host='localhost', user='root', password='hhwswhrO1209', database='ratemybeer1')
    connection2 = pymysql.connect(host='localhost', user='root', password='hhwswhrO1209', database='ratemybeer2')
    return connection1, connection2

def hash_uuid(uuid_str):
    hash_value = hashlib.sha256(uuid_str.encode()).hexdigest()
    return "db1" if int(hash_value[-1], 16) % 2 == 0 else "db2"

@app.route('/add_review', methods=['POST'])
def add_review():
    data = request.json
    if 'beername' not in data or 'beertype' not in data or 'review_text' not in data or 'rating' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    beername, beertype, review_text, rating = data['beername'], data['beertype'], data['review_text'], data['rating']
    conn1, conn2 = get_db_connection()
    cursor1, cursor2 = conn1.cursor(), conn2.cursor()

    try:
        cursor1.execute("SELECT beer_id FROM beer WHERE beer_name = %s AND beer_type = %s", (beername, beertype))
        beer_id = cursor1.fetchone()
        if not beer_id:
            beer_id = str(uuid.uuid4())
            cursor1.execute("INSERT INTO beer (beer_id, beer_name, beer_type) VALUES (%s, %s, %s)", (beer_id, beername, beertype))
            conn1.commit()
            cursor2.execute("INSERT INTO beer (beer_id, beer_name, beer_type) VALUES (%s, %s, %s)", (beer_id, beername, beertype))
            conn2.commit()

        review_id = str(uuid.uuid4())
        db_name = hash_uuid(review_id)
        if db_name == 'db1':
            cursor1.execute("INSERT INTO Review (review_id, beer_id, review_text, rating) VALUES (%s, %s, %s, %s)", (review_id, beer_id, review_text, rating))
            conn1.commit()
        else:
            cursor2.execute("INSERT INTO Review (review_id, beer_id, review_text, rating) VALUES (%s, %s, %s, %s)", (review_id, beer_id, review_text, rating))
            conn2.commit()
    finally:
        cursor1.close()
        cursor2.close()
        conn1.close()
        conn2.close()

    return jsonify({"message": f"Review added into {db_name} successfully"})

@app.route('/delete_review', methods=['DELETE'])
def delete_review():
    data = request.json
    review_id = data.get('review_id')
    if not review_id:
        return jsonify({"error": "review_id is required"}), 400

    conn1, conn2 = get_db_connection()
    cursor1, cursor2 = conn1.cursor(), conn2.cursor()
    assigned_db = hash_uuid(review_id)

    try:
        if assigned_db == "db1":
            cursor1.execute("DELETE FROM Review WHERE review_id = %s", (review_id,))
            conn1.commit()
        else:
            cursor2.execute("DELETE FROM Review WHERE review_id = %s", (review_id,))
            conn2.commit()
    finally:
        cursor1.close()
        cursor2.close()
        conn1.close()
        conn2.close()

    return jsonify({"message": f"Review deleted successfully from {assigned_db}"})

@app.route('/update_review', methods=['POST'])
def update_review():
    data = request.json
    review_id = data.get('review_id')
    if not review_id:
        return jsonify({"error": "review_id is required"}), 400

    review_text = data.get('review_text')
    rating = data.get('rating')
    assigned_db = hash_uuid(review_id)

    conn1, conn2 = get_db_connection()
    cursor = conn1.cursor() if assigned_db == "db1" else conn2.cursor()
    try:
        update_query = "UPDATE Review SET review_text = %s, rating = %s WHERE review_id = %s"
        cursor.execute(update_query, (review_text, rating, review_id))
        conn1.commit() if assigned_db == "db1" else conn2.commit()
    finally:
        cursor.close()
        conn1.close() if assigned_db == "db1" else conn2.close()

    return jsonify({"message": f"Review updated successfully in {assigned_db}"})

@app.route('/select', methods=['GET'])
def select():
    conn1, conn2 = get_db_connection()
    cursor1, cursor2 = conn1.cursor(), conn2.cursor()

    sql_query = "SELECT Review.review_id, Review.beer_id, beer.beer_name, beer.beer_type, Review.review_text, Review.rating FROM Review INNER JOIN beer ON Review.beer_id = beer.beer_id"
    filter_data = request.args
    conditions = []
    values = []

    if 'beer_name' in filter_data:
        conditions.append("beer.beer_name = %s")
        values.append(filter_data['beer_name'])

    if 'beer_type' in filter_data:
        conditions.append("beer.beer_type = %s")
        values.append(filter_data['beer_type'])

    if 'rating_min' in filter_data:
        conditions.append("Review.rating >= %s")
        values.append(filter_data['rating_min'])

    if 'rating_max' in filter_data:
        conditions.append("Review.rating <= %s")
        values.append(filter_data['rating_max'])

    if conditions:
        sql_query += " WHERE " + " AND ".join(conditions)

    if 'limit' in filter_data:
        limit = int(filter_data['limit'])
        sql_query += " LIMIT %s"
        values.append(limit)

    try:
        cursor1.execute(sql_query, values)
        results_db1 = cursor1.fetchall()
        cursor2.execute(sql_query, values)
        results_db2 = cursor2.fetchall()
    finally:
        cursor1.close()
        cursor2.close()
        conn1.close()
        conn2.close()

    merged_results = results_db1 + results_db2
    return jsonify(merged_results)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="localhost", port=8090)
