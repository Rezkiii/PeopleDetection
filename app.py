from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Konfigurasi koneksi database
db_config = {
    'host': 'localhost',
    'database': 'data_sensor',
    'user': 'user',
    'password': 'pass'
}

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        print("Koneksi ke MySQL berhasil")
    except Error as e:
        print(f"Error: '{e}'")

    return connection

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    timestamp = data.get('timestamp')
    detected_people = data.get('detected_people')

    if not timestamp or not isinstance(detected_people, int):
        return jsonify({'error': 'Invalid data'}), 400

    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO detected_data (timestamp, detected_people) VALUES (%s, %s)"
    values = (timestamp, detected_people)

    try:
        cursor.execute(query, values)
        connection.commit()
        return jsonify({'message': 'Data received and stored successfully'}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/data', methods=['GET'])
def get_data():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM detected_data")
    results = cursor.fetchall()

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
