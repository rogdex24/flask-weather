import requests

# RUN TESTS
# pytest test_weather_api.py

BASE_URL = "http://localhost:5000"

def test_add_weather():
    city = "New York"
    temp = 25
    humidity = 50
    response = requests.post(
        f"{BASE_URL}/weather",
        json={"city": city, "temperature": temp, "humidity": humidity}
    )
    assert response.status_code == 201

def test_get_weather_by_city():
    city = "New York"
    response = requests.get(f"{BASE_URL}/weather/{city}")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == city

def test_update_weather():
    city = "New York"
    new_temp = 30
    new_humidity = 60
    response = requests.put(
        f"{BASE_URL}/weather/{city}",
        json={"temperature": new_temp, "humidity": new_humidity}
    )
    assert response.status_code == 200

def test_delete_weather():
    city = "New York"
    response = requests.delete(f"{BASE_URL}/weather/{city}")
    assert response.status_code == 200
