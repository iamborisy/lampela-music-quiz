# Music Quiz Application

## 📚 Приложение 1: Quiz (Квиз)

### Запуск
```bash
cd /Users/user/Documents/music-exam
source .venv/bin/activate
python app.py
```

Откройте браузер: `http://127.0.0.1:5000`

### Функциональность
1. **Главная страница** (`/`) - инициализирует новый квиз
2. **Страница вопроса** (`/quiz`) - показывает:
   - Номер текущего вопроса
   - Ссылку на трек в YouTube Music
   - Выпадающие меню для выбора жанра, поджанра и декады

3. **Страница результата** (`/check_answer`) - показывает:
   - Название трека (🎵)
   - Статус: ✓ Correct или ✗ Incorrect
   - Для каждого поля (жанр, поджанр, декада):
     - Зелёное поле, если правильно
     - Красное поле с правильным ответом, если неправильно

4. **Финальная страница** (`/result`) - итоговый результат со всеми ответами

### Структура Данных
- `tracks.json` - база данных треков (автоматически обновляется через `update_db.py`)
- `stats.json` - статистика визитов и результатов
- Шаблоны в `templates/`:
  - `index.html` - форма с выпадающими меню
  - `check.html` - результат после submit
  - `result.html` - финальный итог

---

## 🔄 Приложение 2: Update Database (Обновление БД)

### Запуск
```bash
cd /Users/user/Documents/music-exam
.venv/bin/python update_db.py
```

### Процесс обновления
1. Скрипт читает файл `list.txt`
2. Парсит блоки в формате:
   ```
   Genre
   Decade
   Subgenre
   Track Title
   Full YouTube Music URL
   Track Title
   Full YouTube Music URL
   ...
   ```
3. Автоматически извлекает YouTube ID из полного URL
4. Проверяет каждый трек на дубликаты (по названию и URL)
5. Добавляет только новые треки в `tracks.json`
6. Выводит подробный отчет

### Формат `list.txt`

**Пример:**
```
Blues
1920-1940
Countryblues
Charley Patton: Down the Dirt Road Blues
https://music.youtube.com/watch?v=fzcCQJ3F_eQ&si=RMjYVOlHkLclHmTo
Tommy Johnson: Canned Heat Blues
https://music.youtube.com/watch?v=RHw1ugBLS5g&si=test123

Jazz
1950-1960
Bebop
Charlie Parker: Koko
https://music.youtube.com/watch?v=test001&si=bebop1
```

### Ключевые функции
- ✓ Парсит множество жанров в одном файле
- ✓ Извлекает YouTube ID из полного URL
- ✓ Проверяет на дубликаты по названию и URL
- ✓ Добавляет только новые треки
- ✓ Выводит подробный лог процесса

### Вывод скрипта
```
🎵 Music Quiz Database Updater
==================================================

📖 Parsing list.txt...
  ✓ Parsed: Track Name
  ⊘ Duplicate: Another Track

💾 Updating database...
✓ Saved 14 tracks to tracks.json

==================================================
📊 Summary:
  • New tracks added: 5
  • Duplicates skipped: 2
  • Total tracks in database: 14
==================================================
```

---

## 🔧 Технические детали

### Структура проекта
```
/Users/user/Documents/music-exam/
├── app.py              # Главное Flask приложение
├── update_db.py        # Скрипт обновления БД
├── list.txt            # Исходный файл для обновления
├── tracks.json         # База данных треков
├── stats.json          # Статистика
├── templates/
│   ├── index.html      # Форма квиза
│   ├── check.html      # Результат ответа
│   └── result.html     # Финальный итог
└── .venv/              # Виртуальное окружение
```

### Зависимости
- Flask - веб-фреймворк
- Jinja2 - шаблонизация (встроена в Flask)

---

## 💡 Советы

1. **Добавление новых треков** - просто отредактируйте `list.txt` и запустите `update_db.py`
2. **Сброс статистики** - удалите `stats.json`, он пересоздастся при следующем запуске
3. **Подозрение на дубликаты?** - просмотрите вывод скрипта, он их все покажет
4. **Ошибка парсинга?** - проверьте, что URL начинается с `https://music.youtube.com/`

