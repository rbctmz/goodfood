from openai import OpenAI

client = OpenAI()
from typing import Optional

async def analyze_sentiment(text: str) -> Optional[float]:
    """Анализ тональности отзыва через OpenAI"""
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Оцени тональность отзыва по шкале от 0 до 1, где 0 - негативная, 1 - позитивная. Верни только число."},
            {"role": "user", "content": text}
        ])
        return float(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return None