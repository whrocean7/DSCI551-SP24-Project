from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import hashlib
import uuid
import pymysql
import configparser

app = Flask(__name__, static_url_path='/static')
CORS(app=app)
app.debug = True

# Read database configuration from file
config = configparser.ConfigParser()
config.read('config.txt')

# Connect to databases
try:
    db1 = pymysql.connect(**dict(config.items('ratemybeer1')))
    db1.autocommit(True)
    cursor1 = db1.cursor()
    print("db1 connected successfully")
except pymysql.err.OperationalError as e:
    print(f"Error connecting to db1: {e}")

try:
    db2 = pymysql.connect(**dict(config.items('ratemybeer2')))
    db2.autocommit(True)
    cursor2 = db2.cursor()
    print("db2 connected successfully")
except pymysql.err.OperationalError as e:
    print(f"Error connecting to db2: {e}")

try:
    db1_rep = pymysql.connect(**dict(config.items('ratemybeer1_rep')))
    db1_rep.autocommit(True)
    cursor3 = db1_rep.cursor()
    print("db1_rep connected successfully")
except pymysql.err.OperationalError as e:
    print(f"Error connecting to db1_rep: {e}")

try:
    db2_rep = pymysql.connect(**dict(config.items('ratemybeer2_rep')))
    db2_rep.autocommit(True)
    cursor4 = db2_rep.cursor()
    print("db2_rep connected successfully")
except pymysql.err.OperationalError as e:
    print(f"Error connecting to db2_rep: {e}")

def hash_uuid(uuid_str):
    # use SHA-256 hash function
    hash_value = hashlib.sha256(uuid_str.encode()).hexdigest()
    # int last character
    last_digit = int(hash_value[-1], 16)
    print('hash value:', hash_value[-1])
    print('last_digit int:', last_digit)
    route_table = {'0': 'db1', '1': 'db2'}
    # do hash
    if last_digit % 2 == 0:
        return route_table['0']
    else:
        return route_table['1']

@app.route('/add_review', methods=['POST'])
def add_review():
    # get review
    data = request.json

    # check data
    if 'beername' not in data or 'beertype' not in data or 'review_text' not in data or 'rating' not in data:
        return jsonify({"error": "beername, beertype, review_text, and rating are required"}), 400

    # extract data
    beername = data['beername']
    beertype = data['beertype']
    review_text = data['review_text']
    rating = data['rating']

    # extract beer from either beer table
    cursor1.execute("SELECT beer_id FROM beer WHERE beer_name = %s AND beer_type = %s", (beername, beertype))
    existing_beer = cursor1.fetchone()

    if not existing_beer:
        # if it's a new beer
        beer_id = str(uuid.uuid4())  # use uuid library to generate a unique beer_id
        cursor1.execute("INSERT INTO beer (beer_id, beer_name, beer_type, update_time) VALUES (%s, %s, %s, NOW())",
                       (beer_id, beername, beertype))
        db1.commit()
        cursor2.execute("INSERT INTO beer (beer_id, beer_name, beer_type, update_time) VALUES (%s, %s, %s, NOW())",
                        (beer_id, beername, beertype))
        db2.commit()
        cursor3.execute("INSERT INTO beer (beer_id, beer_name, beer_type, update_time) VALUES (%s, %s, %s, NOW())",
                        (beer_id, beername, beertype))
        db1_rep.commit()
        cursor4.execute("INSERT INTO beer (beer_id, beer_name, beer_type, update_time) VALUES (%s, %s, %s, NOW())",
                        (beer_id, beername, beertype))
        db2_rep.commit()
    else:
        # if it's an existing beer
        beer_id = existing_beer[0]

    # generate uuid for review
    review_id = str(uuid.uuid4())
    db_name = hash_uuid(review_id)

    if db_name == 'db1':
        if 'cursor1' in globals():
            # insert into db1 and db1 replica
            cursor1.execute(
                "INSERT INTO Review (review_id, beer_id, review_text, rating, create_time, update_time) VALUES (%s, %s, %s, %s, NOW(), NOW())",
                (review_id, beer_id, review_text, rating))
            try:
                db1.commit()
                print("db1 insert successful")
                # return jsonify({"message": "Review added into db1 successfully"})
            except pymysql.err.OperationalError as e:
                # Handle the case where db1 is unavailable or dropped
                print(f"Error committing to db1: {e}")
                # return jsonify({"error": "Failed to add review to db1"}), 500
        else:
            print("db1 is not connected, cannot insert data into db1")
        if 'cursor3' in globals():
            cursor3.execute(
                "INSERT INTO Review (review_id, beer_id, review_text, rating, create_time, update_time) VALUES (%s, %s, %s, %s, NOW(), NOW())",
                (review_id, beer_id, review_text, rating))
            try:
                db1_rep.commit()
                # return jsonify({"message": "Review added into db1 replica successfully"})
                print("db1_rep insert successful")
            except pymysql.err.OperationalError as e:
                # Handle the case where db1_rep is unavailable or dropped
                print(f"Error committing to db1_rep: {e}")
                # return jsonify({"error": "Failed to add review to db1 replica"}), 500
        else:
            print("db1_rep is not connected, cannot insert data into db1_rep")
        return jsonify({"message": "Review added into db1 successfully"})
    else:
        if 'cursor2' in globals():
            # insert into db2 and db2 replica
            cursor2.execute(
                "INSERT INTO Review (review_id, beer_id, review_text, rating, create_time, update_time) VALUES (%s, %s, %s, %s, NOW(), NOW())",
                (review_id, beer_id, review_text, rating))
            try:
                db2.commit()
                print("dp2 insert successful")
                # return jsonify({"message": "Review added into db2 replica successfully"})
            except pymysql.err.OperationalError as e:
                # Handle the case where db2_rep is unavailable or dropped
                print(f"Error committing to db2_rep: {e}")
                # return jsonify({"error": "Failed to add review to db2 replica"}), 500
        else:
            print("db2 is not connected, cannot insert data into db2")

        if 'cursor4' in globals():

            cursor4.execute(
                "INSERT INTO Review (review_id, beer_id, review_text, rating, create_time, update_time) VALUES (%s, %s, %s, %s, NOW(), NOW())",
                (review_id, beer_id, review_text, rating))
            try:
                db2_rep.commit()
                print("dp2_rep insert successful")
                # return jsonify({"message": "Review added into db2 successfully"})
            except pymysql.err.OperationalError as e:
                # Handle the case where db2 is unavailable or dropped
                print(f"Error committing to db2: {e}")
                # return jsonify({"error": "Failed to add review to db2"}), 500
        else:
            print("db2_rep is not connected, cannot insert data into db2_rep")
        return jsonify({"message": "Review added into db2 successfully"})


@app.route('/delete_review', methods=['DELETE'])
def delete_review():
    # get data
    data = request.json

    # check review_id
    if 'review_id' not in data:
        return jsonify({"error": "review_id is required"}), 400

    # extract review_id
    review_id = data['review_id']

    # find out which database to operate
    assigned_db = hash_uuid(review_id)

    # Initialize primary and replica database connections and cursors
    if assigned_db == "db1":
        if 'db1' in globals():
            db_connection = db1
            cursor = db_connection.cursor()
            delete_query = "DELETE FROM Review WHERE review_id = %s"
            cursor.execute(delete_query, (review_id,))
            db_connection.commit()
            print("db1 delete successful")
        else:
            print("db1 not connected, cannot delete from it")
        if 'db1_rep' in globals():
            db_connection = db1_rep
            cursor = db_connection.cursor()
            delete_query = "DELETE FROM Review WHERE review_id = %s"
            cursor.execute(delete_query, (review_id,))
            db_connection.commit()
            print("db1_rep delete successful")
        else:
            print("db1_rep not connected, cannot delete from it")

        db_name = "db1"
    else:
        if 'db2' in globals():
            db_connection = db2
            cursor = db_connection.cursor()
            delete_query = "DELETE FROM Review WHERE review_id = %s"
            cursor.execute(delete_query, (review_id,))
            db_connection.commit()
            print("db2 delete successful")
        else:
            print("db2 not connected, cannot delete from it")
        if 'db2_rep' in globals():
            db_connection = db2_rep
            cursor = db_connection.cursor()
            delete_query = "DELETE FROM Review WHERE review_id = %s"
            cursor.execute(delete_query, (review_id,))
            db_connection.commit()
            print("db2_rep delete successful")
        else:
            print("db2_rep not connected, cannot delete from it")
        db_name = "db2"

    return jsonify({"message": f"Review deleted successfully from {db_name} and its replica"})

@app.route('/update_review', methods=['POST'])
def update_review():
    # get data
    data = request.json

    # check review_id
    if 'review_id' not in data:
        return jsonify({"error": "review_id is required"}), 400

    # extract data
    review_id = data['review_id']
    review_text = data.get('review_text')
    rating = data.get('rating')

    # construct SQL
    update_query = "UPDATE Review SET "
    update_values = []

    if review_text:
        update_query += "review_text = %s, "
        update_values.append(review_text)
    if rating:
        update_query += "rating = %s, "
        update_values.append(rating)

    # Add update_time
    update_query += "update_time = NOW(), "

    # delete last ","
    update_query = update_query.rstrip(', ')

    # add filter
    update_query += " WHERE review_id = %s"
    update_values.append(review_id)

    # find out which database to operate
    assigned_db = hash_uuid(review_id)

    # Initialize primary and replica database connections and cursors
    try:
        if assigned_db == "db1":
            if 'db1' in globals():
                db_connection = db1
                cursor = db_connection.cursor()
                cursor.execute(update_query, update_values)
                db_connection.commit()
            else:
                print("db1 not connected, cannot update it")

            if 'db1_rep' in globals():
                db_connection = db1_rep
                cursor = db_connection.cursor()
                cursor.execute(update_query, update_values)
                db_connection.commit()
            else:
                print("db1_rep not connected, cannot update it")
            db_name = "db1"
        else:
            if 'db2' in globals():
                db_connection = db2
                cursor = db_connection.cursor()
                cursor.execute(update_query, update_values)
                db_connection.commit()
            else:
                print("db2 not connected, cannot update it")

            if 'db2_rep' in globals():
                db_connection = db2_rep
                cursor = db_connection.cursor()
                cursor.execute(update_query, update_values)
                db_connection.commit()
            else:
                print("db2_rep not connected, cannot update it")
            db_name = "db2"

    except pymysql.err.OperationalError as e:
        return jsonify({"error": f"Failed to connect to database: {e}"}), 500

    return jsonify({"message": f"Review updated successfully in {db_name} and its replica"})

@app.route('/select', methods=['GET'])
def select():
    try:
        # get filter
        filter_data = request.args

        # Initialize results lists for part 1 and part 2
        part1_results = []
        part2_results = []

        # Maintain a set of unique review IDs
        unique_review_ids = set()

        # Execute queries for db1 if the cursor is defined
        if 'cursor1' in globals():
            cursor = cursor1
            db_name = 'db1'
            try:
                # construct SQL
                sql_query = "SELECT Review.review_id, Review.beer_id, beer.beer_name, beer.beer_type, Review.review_text, Review.rating FROM Review INNER JOIN beer ON Review.beer_id = beer.beer_id"

                # construct filter
                conditions = []
                values = []

                if 'beer_name' in filter_data:
                    conditions.append("beer.beer_name = '{}'".format(filter_data['beer_name']))

                if 'beer_type' in filter_data:
                    conditions.append("beer.beer_type = '{}'".format(filter_data['beer_type']))

                if 'rating' in filter_data:
                    conditions.append("Review.rating = {}".format(filter_data['rating']))

                if conditions:
                    sql_query += " WHERE " + " AND ".join(conditions)

                # add ORDER BY clause to sort by update_time descending
                sql_query += " ORDER BY Review.update_time DESC"

                # add limit condition
                if 'Quantity' in filter_data:
                    limit = int(filter_data['Quantity'])
                    sql_query += " LIMIT {}".format(limit)

                # execute query
                cursor.execute(sql_query, values)
                results = cursor.fetchall()
                # print("db1 res:", results)

                # Filter out redundant results
                filtered_results = [row for row in results if row[0] not in unique_review_ids]

                # Add filtered results to part 1
                part1_results.extend(filtered_results)

                # Update unique review IDs
                unique_review_ids.update(row[0] for row in filtered_results)

            except pymysql.err.OperationalError as e:
                print(f"Failed to execute query on {db_name}: {e}")

        else:
            print("Cursor for db1 is not defined. Skipping queries for db1")

        if 'cursor3' in globals():
            cursor = cursor3
            db_name = 'db3'
            try:
                # construct SQL
                sql_query = "SELECT Review.review_id, Review.beer_id, beer.beer_name, beer.beer_type, Review.review_text, Review.rating FROM Review INNER JOIN beer ON Review.beer_id = beer.beer_id"

                # construct filter
                conditions = []
                values = []

                if 'beer_name' in filter_data:
                    conditions.append("beer.beer_name = '{}'".format(filter_data['beer_name']))

                if 'beer_type' in filter_data:
                    conditions.append("beer.beer_type = '{}'".format(filter_data['beer_type']))

                if 'rating' in filter_data:
                    conditions.append("Review.rating = {}".format(filter_data['rating']))

                if conditions:
                    sql_query += " WHERE " + " AND ".join(conditions)

                # add ORDER BY clause to sort by update_time descending
                sql_query += " ORDER BY Review.update_time DESC"

                # add limit condition
                if 'Quantity' in filter_data:
                    limit = int(filter_data['Quantity'])
                    sql_query += " LIMIT {}".format(limit)

                # execute query
                cursor.execute(sql_query, values)
                results = cursor.fetchall()
                # print("db1_rep res:", results)
                # Filter out redundant results
                filtered_results = [row for row in results if row[0] not in unique_review_ids]

                # Add filtered results to part 1
                part1_results.extend(filtered_results)

                # Update unique review IDs
                unique_review_ids.update(row[0] for row in filtered_results)

            except pymysql.err.OperationalError as e:
                print(f"Failed to execute query on {db_name}: {e}")

        else:
            print("Cursor for db1_rep is not defined. Skipping queries for db1")

        if 'cursor2' in globals():
            cursor = cursor2
            db_name = 'db2'
            try:
                # construct SQL
                sql_query = "SELECT Review.review_id, Review.beer_id, beer.beer_name, beer.beer_type, Review.review_text, Review.rating FROM Review INNER JOIN beer ON Review.beer_id = beer.beer_id"

                # construct filter
                conditions = []
                values = []

                if 'beer_name' in filter_data:
                    conditions.append("beer.beer_name = '{}'".format(filter_data['beer_name']))

                if 'beer_type' in filter_data:
                    conditions.append("beer.beer_type = '{}'".format(filter_data['beer_type']))

                if 'rating' in filter_data:
                    conditions.append("Review.rating = {}".format(filter_data['rating']))

                if conditions:
                    sql_query += " WHERE " + " AND ".join(conditions)

                # add ORDER BY clause to sort by update_time descending
                sql_query += " ORDER BY Review.update_time DESC"

                # add limit condition
                if 'Quantity' in filter_data:
                    limit = int(filter_data['Quantity'])
                    sql_query += " LIMIT {}".format(limit)

                # execute query
                cursor.execute(sql_query, values)
                results = cursor.fetchall()
                # print("db2",results)

                # Filter out redundant results
                filtered_results = [row for row in results if row[0] not in unique_review_ids]

                # Add filtered results to part 1
                part2_results.extend(filtered_results)

                # Update unique review IDs
                unique_review_ids.update(row[0] for row in filtered_results)

            except pymysql.err.OperationalError as e:
                print(f"Failed to execute query on {db_name}: {e}")

        else:
            print("Cursor for db2 is not defined. Skipping queries for db2")

        if 'cursor4' in globals():
            cursor = cursor4
            db_name = 'db4'
            try:
                # construct SQL
                sql_query = "SELECT Review.review_id, Review.beer_id, beer.beer_name, beer.beer_type, Review.review_text, Review.rating FROM Review INNER JOIN beer ON Review.beer_id = beer.beer_id"

                # construct filter
                conditions = []
                values = []

                if 'beer_name' in filter_data:
                    conditions.append("beer.beer_name = '{}'".format(filter_data['beer_name']))

                if 'beer_type' in filter_data:
                    conditions.append("beer.beer_type = '{}'".format(filter_data['beer_type']))

                if 'rating' in filter_data:
                    conditions.append("Review.rating = {}".format(filter_data['rating']))

                if conditions:
                    sql_query += " WHERE " + " AND ".join(conditions)

                # add ORDER BY clause to sort by update_time descending
                sql_query += " ORDER BY Review.update_time DESC"

                # add limit condition
                if 'Quantity' in filter_data:
                    limit = int(filter_data['Quantity'])
                    sql_query += " LIMIT {}".format(limit)

                # execute query
                cursor.execute(sql_query, values)
                results = cursor.fetchall()

                # Filter out redundant results
                filtered_results = [row for row in results if row[0] not in unique_review_ids]

                # Add filtered results to part 1
                part2_results.extend(filtered_results)

                # Update unique review IDs
                unique_review_ids.update(row[0] for row in filtered_results)

            except pymysql.err.OperationalError as e:
                print(f"Failed to execute query on {db_name}: {e}")

        else:
            print("Cursor for db2_rep is not defined. Skipping queries for db2_rep")

        # Combine results from both parts
        # print("part1results", part1_results)
        # print("part2results", part2_results)
        merged_results = part1_results + part2_results
        # print(merged_results)

        # truncate merged results to the limit
        if 'Quantity' in filter_data:
            limit = int(filter_data['Quantity'])
            merged_results = merged_results[:limit]

        # convert results to JSON
        data = [
            {'review_id': row[0], 'beer_id': row[1], 'beer_name': row[2], 'beer_type': row[3], 'review_text': row[4],
             'rating': row[5]} for row in merged_results]
        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)})



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user')
def user():
    return render_template('user.html')


if __name__ == '__main__':
    app.run(host="localhost", port='8091')

    cursor1.close()
    db1.close()
