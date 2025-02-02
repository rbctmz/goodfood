# MVP (Minimum Viable Product) — набор функций, которые должны быть выполнены, чтобы продукт был готов к продаже.

Вот пошаговый план:

---

### **1. Определите MVP (ключевые функции)**
Сфокусируйтесь на самом необходимом:

- **Поиск кафе** по локации (например, город или район).
- **Анализ отзывов** через LLM (например, суммаризация и оценка тональности).
- **Фильтры** по типу кухни, рейтингу, цене.
- **Простой интерфейс** с картой и списком заведений.

---

### **2. Соберите данные**

Начните с небольшого набора данных для тестирования:
- **Ручной сбор**: Возьмите 10–20 кафе из открытых источников (Google Maps, Яндекс.Карты) и сохраните их отзывы и меню в CSV/JSON.
- **Используйте API**: Например, [Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview) или [Yelp Fusion API](https://www.yelp.com/developers/documentation/v3) для получения данных (если не хотите заниматься скрапингом).
- **Важно**: Проверьте условия использования данных, чтобы не нарушать правила платформ.

---

### **3. Настройте LLM для анализа**
- **Выберите модель**: 
  - **OpenAI API** (GPT-3.5/4) — самый простой вариант для начала (пример: анализ тональности отзывов).
  - Бесплатные альтернативы: [Hugging Face Transformers](https://huggingface.co/) (например, модель `bert-base-multilingual-uncased-sentiment` для оценки настроения).
- **Пример запроса к GPT**:
  ```python
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "Проанализируй отзыв и выдели основные темы (еда, обслуживание, атмосфера) и общий тон (позитивный/негативный)."},
      {"role": "user", "content": "Отзыв: 'Кофе отличный, но обслуживали медленно.'"}
    ]
  )
  print(response.choices[0].message['content'])
  # Вывод: Темы: еда (позитивно), обслуживание (негативно). Общий тон: нейтральный.
  ```

---

### **4. Создайте бэкенд**
Используйте простые инструменты для быстрого старта:
- **Язык**: Python (наиболее удобен для работы с LLM и прототипирования).
- **Фреймворки**:
  - **FastAPI** для создания API.
  - **SQLite** или **PostgreSQL** для хранения данных кафе.
- **Пример структуры API**:
  - `GET /search?location=Москва&cuisine=кофейня` → возвращает список кафе.
  - `POST /analyze` → принимает отзыв и возвращает анализ от LLM.

---

### **5. Сделайте фронтенд**
Используйте инструменты для быстрого прототипирования:
- **Streamlit** (Python-библиотека) — можно создать интерфейс за несколько часов.
- **Пример кода на Streamlit**:
  ```python
  import streamlit as st

  st.title("Поиск кафе")
  location = st.text_input("Введите город:")
  if location:
      # Запрос к вашему API для получения данных
      cafes = get_cafes_from_backend(location)
      for cafe in cafes:
          st.write(f"**{cafe['name']}** (Рейтинг: {cafe['rating']}/5)")
          st.write(f"Отзывы: {cafe['summary']}")
  ```

---

### **6. Соберите всё вместе**
1. Запустите бэкенд (например, на локальном сервере с помощью `uvicorn main:app --reload` для FastAPI).
2. Запустите фронтенд (для Streamlit: `streamlit run app.py`).
3. Протестируйте сценарии:
   - Поиск кафе по локации.
   - Просмотр анализа отзывов.
   - Фильтрация по параметрам.

---

### **7. Проверьте гипотезы**
- Покажите прототип друзьям или тестовой аудитории.
- Соберите фидбек: 
  - Удобен ли интерфейс?
  - Понятны ли рекомендации?
  - Какие функции не хватает?

---

### **8. Что дальше?**
- Добавьте больше данных (автоматизируйте сбор через скрапинг или API).
- Улучшите анализ (например, сравнение меню или выявление уникальных блюд).
- Интегрируйте карты (например, через [Leaflet.js](https://leafletjs.com/) или [Google Maps API](https://developers.google.com/maps/documentation)).

---

### **Пример стека для прототипа**
| Компонент       | Инструменты                         |
|-----------------|-------------------------------------|
| **Данные**      | Google Maps API                     |
| **Бэкенд**      | FastAPI + SQLite                    |
| **LLM**         | OpenAI API                          |
| **Фронтенд**    | Streamlit                           |
| **Деплой**      | Heroku / PythonAnywhere (для MVP)   |

---

### **Пример структуры проекта**
```markdown
goodfood/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── cafes.py
│   │   │   │   └── reviews.py
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   └── session.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── cafe_service.py
│   │       └── review_service.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_api.py
│   └── main.py
├── frontend/
│   ├── __init__.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── home.py
│   │   └── analysis.py
│   └── app.py
├── data/
│   ├── raw/
│   │   └── cafes.json
│   └── processed/
│       └── analyzed_reviews.json
├── ml/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── sentiment.py
│   └── utils/
│       ├── __init__.py
│       └── text_preprocessing.py
├── scripts/
│   ├── data_collection/
│   │   ├── google_places.py
│   │   └── yelp_api.py
│   └── setup_db.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```
### Описание основных компонентов:
- backend/ - FastAPI приложение
- frontend/ - Streamlit интерфейс
- data/ - JSON файлы с данными
- ml/ - Модули для работы с LLM
- scripts/ - Вспомогательные скрипты

### **requirements.txt**
```markdown
fastapi
uvicorn
sqlalchemy
streamlit
openai
python-dotenv
requests
```
