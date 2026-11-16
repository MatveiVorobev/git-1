import requests
import sys

# Демонстрационные данные на случай проблем с сетью
MOCK_DATA = {
    "current_condition": [{
        "temp_C": "15",
        "humidity": "65",
        "windspeedKmph": "12",
        "weatherDesc": [{"value": "Partly cloudy"}]
    }]
}

def main():
    city = input("Введите город (например, London): ").strip()
    if not city:
        print("Ошибка: пустой ввод.")
        sys.exit(1)

    print(f"Запрос данных для {city}...")
    
    try:
        url = f"http://wttr.in/{city}?format=j1"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        c = data["current_condition"][0]
        is_mock = False
    except Exception as e:
        print(f"⚠️ Сеть недоступна или таймаут. Используются демонстрационные данные.")
        data = MOCK_DATA
        c = data["current_condition"][0]
        is_mock = True

    temp = c["temp_C"]
    humidity = c["humidity"]
    wind = c["windspeedKmph"]
    desc = c["weatherDesc"][0]["value"]

    print("\n" + "="*40)
    if is_mock:
        print(f"Погода в городе: {city} (ДЕМО-РЕЖИМ)")
    else:
        print(f"Погода в городе: {city}")
    print("-"*40)
    print(f"Температура:  {int(temp):+d}°C")
    print(f"Влажность:    {humidity}%")
    print(f"Ветер:        {wind} км/ч")
    print(f"Состояние:    {desc}")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()
