import json
from collections import defaultdict

# Читаем исходный JSON
with open('users.json', 'r', encoding='utf-8') as f:
    users = json.load(f)

# Группируем по address.city
cities = defaultdict(list)
for user in users:
    city = user.get('address', {}).get('city', 'Unknown')
    cities[city].append(user['name'])

# Сохраняем результат в cities.json
result = dict(cities)
with open('cities.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print(f" Сгруппировано {len(users)} пользователей по {len(result)} городам.")
print("Результат сохранен в cities.json")
