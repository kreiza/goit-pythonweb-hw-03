# GoIT Python Web HW-03

Веб-додаток з маршрутизацією та обробкою форм.

## Функціональність

- **Головна сторінка** (`/`) - index.html
- **Сторінка повідомлень** (`/message`) - message.html з формою
- **Перегляд повідомлень** (`/read`) - відображення всіх збережених повідомлень
- **Статичні ресурси** - style.css, logo.png
- **Обробка помилок** - error.html для 404

## Запуск

### Локально
```bash
pip install -r requirements.txt
python main.py
```

### Docker
```bash
# Збірка та запуск
docker build -t web-app .
docker run -p 3000:3000 -v $(pwd)/storage:/app/storage web-app

# Або через docker-compose
docker-compose up --build
```

Додаток буде доступний на http://localhost:3000

## Структура даних

Повідомлення зберігаються у `storage/data.json`:
```json
{
  "2022-10-29 20:20:58.020261": {
    "username": "krabaton",
    "message": "First message"
  }
}
```