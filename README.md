# GoodFood - Умный Поиск Кафе и Ресторанов 🍽️

Веб-приложение для интеллектуального поиска и анализа кафе/ресторанов с использованием AI для обработки отзывов.

## Возможности 🚀

- Поиск заведений по локации
- AI-анализ отзывов посетителей
- Фильтрация по кухне, рейтингу и ценам
- Интерактивная карта заведений
- Умные рекомендации на основе предпочтений

## Технологии 💻

- **Backend**: FastAPI, SQLAlchemy
- **Frontend**: Streamlit
- **Database**: SQLite/PostgreSQL
- **AI/ML**: OpenAI GPT-3.5, Hugging Face Transformers
- **APIs**: Google Places API
- **DevOps**: Docker, GitHub Actions

## Установка 🔧

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/goodfood.git
cd goodfood
```

2. Установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env файл, добавив свои API ключи
```

## Необходимые API ключи 🔑
- Google Places API ключ
- OpenAI API ключ

## Структура проекта 📁

```markdown
goodfood/
├── backend/     # FastAPI приложение
├── frontend/    # Streamlit интерфейс
├── data/        # Данные и датасеты
├── ml/          # Модели машинного обучения
└── scripts/     # Вспомогательные скрипты
```

## Запуск 🚀

1. Запустите бэкенд:
```bash
uvicorn backend.main:app --reload

2. Запустите фронтенд:
```bash
streamlit run frontend/app.py
```

## API Документация 📚
API документация доступна по адресу: http://localhost:8000/docs

## Тестирование 🧪
Запуск тестов:

```bash
pytest --cov=backend tests/
```

## Вклад в проект 🤝
1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Создайте Pull Request

## Лицензия 📝
MIT License - см. [LICENSE](LICENSE) файл

## Контакты 📧
- Автор: [Ваше Имя]
- Email: [ваш@email.com]
- GitHub: [@username]

## Благодарности 🙏
- OpenAI за GPT API
- Google за Places API

