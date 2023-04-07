from flask import Flask, jsonify, request
from db import Database

app = Flask(__name__)


@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    
    if not (city and isinstance(city, str)):
        return jsonify({'error': 'City name is required as str'}), 400
    
    try:
        with Database() as db:
            query = "SELECT temperature, humidity FROM weather_data WHERE city = %s"
            db.cursor.execute(query, (city,))
            result = db.cursor.fetchone()

            if not result:
                return jsonify({'error': 'Weather data not found for the city'}), 404

            data = {'city': city, 'temperature': result[0], 'humidity': result[1]}
            return jsonify(data), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'Unable to fetch weather data'}), 500
    
    
@app.route('/weather', methods=['POST'])
def add_weather():
    data = request.get_json()
    city = data.get('city')
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    
    if not all([
        isinstance(city, str),
        isinstance(temperature, (int,float)),
        isinstance(humidity, (int,float))
    ]):
        return jsonify({'error': 'City must be a provided as a string and temperature and humidity must be integers'}), 400


    try:
        with Database() as db:
            query = "INSERT INTO weather_data (city, temperature, humidity) VALUES (%s, %s, %s)"
            db.cursor.execute(query, (city, temperature, humidity))
            db.connection.commit()
            return jsonify({'message': 'Weather added successfully'}), 201
    except Exception as e:
        print(e)
        return jsonify({'error': 'Unable to add weather or City already exists'}), 500



@app.route('/weather/<city>', methods=['PUT'])
def update_weather(city):
    temperature = request.json.get('temperature')
    humidity = request.json.get('humidity')

    if not all(isinstance(val, (int, float)) for val in [temperature, humidity]):
        return jsonify({'error': 'Temperature and humidity must be provided as integers or floats'}), 400


    try:
        with Database() as db:
            query = "UPDATE weather_data SET"
            values = []

            if temperature:
                query += " temperature = %s,"
                values.append(temperature)

            if humidity:
                query += " humidity = %s,"
                values.append(humidity)

            query = query.rstrip(',')
            query += " WHERE city = %s"
            values.append(city)

            db.cursor.execute(query, tuple(values))
            db.connection.commit()

            return jsonify({'message': 'Weather data updated successfully'}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'Unable to update weather data'}), 500


@app.route('/weather/<city>', methods=['DELETE'])
def delete_weather(city):
    try:
        with Database() as db:
            query = "DELETE FROM weather_data WHERE city = %s"
            db.cursor.execute(query, (city,))
            db.connection.commit()

            return jsonify({'message': 'Weather data deleted successfully'}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'Unable to delete weather data'}), 500


if __name__ == '__main__':
    app.run()
