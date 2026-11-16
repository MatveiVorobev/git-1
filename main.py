import requests
import json
import os

def get_biometrics(name):
    """Этап 1: Разведка"""
    try:
        age_resp = requests.get(f"https://api.agify.io?name={name}", timeout=5)
        
        if age_resp.status_code == 429:
            print("Внимание: Лимит API возраста исчерпан.")
            age = "лимит исчерпан"
        else:
            age_resp.raise_for_status()
            age_data = age_resp.json()
            age = age_data.get("age", "неизвестно")
            
        gender_resp = requests.get(f"https://api.genderize.io?name={name}", timeout=5)
        
        if gender_resp.status_code == 429:
            print("Внимание: Лимит API пола исчерпан.")
            gender_pct = 0
            gender_text = "unknown"
        else:
            gender_resp.raise_for_status()
            gender_data = gender_resp.json()
            probability = gender_data.get("probability", 0)
            gender_pct = int(probability * 100) if probability else 0
            gender_text = gender_data.get("gender", "unknown")
        
        print(f"Цель: {name.capitalize()}. Вероятный возраст: {age}. Пол: {gender_text} ({gender_pct}%).")
        
        return {
            "name": name,
            "age": age,
            "gender_probability": gender_pct
        }
    except Exception as e:
        print(f"Ошибка разведки: {e}")
        return None

def get_digital_activity(user_id=1):
    """Этап 2: Маскировка"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SecretAgentBot/1.0",
        "Accept-Language": "ru-RU,ru;q=0.9"
    }
    
    try:
        response = requests.get(
            "https://jsonplaceholder.typicode.com/posts",
            params={"userId": user_id},
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
        posts = response.json()
        
        count = len(posts)
        first_post_title = posts[0]["title"] if posts else "Нет постов"
        
        print(f"Постов: {count}. Первый: {first_post_title}")
        return {"posts_count": count}
    except Exception as e:
        print(f"Ошибка маскировки: {e}")
        return {"posts_count": 0}

def send_report(data):
    """Этап 3: Передача данных"""
    try:
        response = requests.post("https://httpbin.org/post", json=data, timeout=5)
        response.raise_for_status()
        server_response = response.json()
        print("Отчет принят сервером:")
        print(json.dumps(server_response.get("json"), indent=2))
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def download_evidence():
    """Этап 4: Загрузка улик (упрощенная)"""
    try:
        url = "https://via.placeholder.com/400x300.png"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        # Скачиваем content целиком, а не потоком
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        filename = "evidence.jpg"
        with open(filename, 'wb') as f:
            f.write(response.content)
                
        file_size = os.path.getsize(filename)
        print(f"Улика скачана: {filename}. Размер: {file_size} байт.")
    except Exception as e:
        print(f"Ошибка скачивания: {e}")

def test_error_handling():
    """Этап 5: Обработка сбоев"""
    print("\n--- Тест ошибок ---")
    
    try:
        resp = requests.get("https://httpbin.org/status/404", timeout=5)
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Перехвачено: 404 Not Found.")
        
    try:
        resp = requests.get("https://httpbin.org/delay/6", timeout=3)
    except requests.exceptions.Timeout:
        print("Перехвачено: Timeout (база молчит).")

def main():
    print("=== ЗАПУСК ПРОТОКОЛА ===\n")
    
    name = input("Имя цели: ").strip()
    bio_data = get_biometrics(name)
    
    if not bio_data:
        print("Сбой биометрии.")
        return

    activity_data = get_digital_activity(user_id=1)
    
    report = {
        "target_name": bio_data["name"],
        "estimated_age": bio_data["age"],"female_probability_pct": bio_data["gender_probability"],
        "digital_footprint_posts": activity_data["posts_count"]
    }
    
    send_report(report)
    download_evidence()
    test_error_handling()
    
    print("\n=== ГОТОВО ===")

if __name__ == "__main__":
    main()
