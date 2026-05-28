import os
os.system("pip install pyTelegramBotAPI schedule feedparser requests beautifulsoup4 mistralai==1.12.4")

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import schedule
import json
import time
import threading
import logging
import random
import re
from datetime import datetime
import feedparser
import requests
from bs4 import BeautifulSoup
from mistralai import Mistral
from typing import Dict, List, Optional

# ========================
#       НАСТРОЙКИ
# ========================
TELEGRAM_BOT_TOKEN = "8650040948:AAHeUQCyKC_ml6q0sKPj54nkI2lqz4L6gZY"
MISTRAL_API_KEY = "6bHT7e3TE0TPnfdsNsols5JkkgfSB8VC"
ADMINS = [6036761167, 6419615188]
GITHUB_URL = "https://github.com/BadAnimator/BroadCast/raw/refs/heads/main/Config.json"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

# ========================
#       КАНАЛЫ
# ========================
CHANNELS = {
    -1002839720955: {
        "title": "DarkNet-Magazine",
        "description": "Новости и статьи о даркнете, кибербезопасности, анонимности.",
        "link": "https://t.me/darknet_magazine",
        "topics": ["кибербезопасность", "даркнет", "хакеры", "анонимность"],
        "rss_sources": [
            "https://www.interfax.ru/rss.asp",
            "http://www.securitylab.ru/_services/export/rss/news.php",
            "https://xakep.ru/feed/",
            "https://habr.com/ru/rss/all/all/?fl=ru",
            "https://nplus1.ru/rss"
        ],
        "posts_per_day": 6
    },
    -1002515949890: {
        "title": "Stalin-OSINT",
        "description": "OSINT-расследования, методы поиска информации, утечки данных.",
        "link": "https://t.me/osint_stalin",
        "topics": ["OSINT", "расследования", "поиск информации", "данные"],
        "rss_sources": [
            "https://tass.ru/rss/v2.xml",
            "https://www.interfax.ru/rss.asp",
            "https://www.osintme.com/index.php/feed/",
            "https://nplus1.ru/rss"
        ],
        "posts_per_day": 6
    },
    -1002758779598: {
        "title": "True-Killer",
        "description": "Криминальные новости, истории, расследования.",
        "link": "https://t.me/true_killer",
        "topics": ["криминал", "новости", "расследования", "происшествия"],
        "rss_sources": [
            "https://tass.ru/rss/v2.xml",
            "https://www.interfax.ru/rss.asp",
            "https://lenta.ru/rss/news",
            "https://iz.ru/xml/rss/all.xml"
        ],
        "posts_per_day": 6
    },
    -1002914714454: {
        "title": "ARECTOBAH_3A_PKH",
        "description": "Юмор, мемы, приколы, забавные истории, новости.",
        "link": "https://t.me/APECTOBAH_3A_PKH",
        "topics": ["юмор", "мемы", "приколы", "развлечения", "новости"],
        "rss_sources": [
            "https://tass.ru/rss/v2.xml",
            "https://www.interfax.ru/rss.asp",
            "https://www.anekdot.ru/rss/export_j.xml",
            "https://iz.ru/xml/rss/all.xml"
        ],
        "posts_per_day": 6
    },
    -1003021980862: {
        "title": "DARK-IntenretS",
        "description": "Тёмная сторона интернета, технологии, уязвимости.",
        "link": "https://t.me/dark_internets",
        "topics": ["интернет", "технологии", "безопасность", "уязвимости"],
        "rss_sources": [
            "https://habr.com/ru/rss/all/all/?fl=ru",
            "http://www.securitylab.ru/_services/export/rss/news.php",
            "https://tass.ru/rss/v2.xml",
            "https://nplus1.ru/rss"
        ],
        "posts_per_day": 6
    },
    -1002468234153: {
        "title": "Attack-APATIA",
        "description": "Кибератаки, уязвимости, защита.",
        "link": "https://t.me/attack_apatia",
        "topics": ["кибератаки", "уязвимости", "защита", "инциденты"],
        "rss_sources": [
            "https://xakep.ru/feed/",
            "http://www.securitylab.ru/_services/export/rss/news.php",
            "https://tass.ru/rss/v2.xml",
            "https://nplus1.ru/rss"
        ],
        "posts_per_day": 6
    },
    -1003391258799: {
        "title": "Поиск людей бот",
        "description": "Методы поиска людей, OSINT, советы, новости",
        "link": "https://t.me/People_Searchrobot",
        "topics": ["поиск людей", "OSINT", "инструменты", "советы", "новости"],
        "rss_sources": [
            "https://tass.ru/rss/v2.xml",
            "https://russian.rt.com/rss/",
            "https://iz.ru/xml/rss/all.xml"
        ],
        "posts_per_day": 6
    },
    -1003395961959: {
        "title": "Пробивчик?",
        "description": "Пробив информации, базы данных, утечки.",
        "link": "https://t.me/Probitb_cheloveka",
        "topics": ["пробив", "базы данных", "утечки", "информация"],
        "rss_sources": [
            "https://www.opennet.ru/opennews/opennews_all.rss",
            "https://russian.rt.com/rss/",
            "https://iz.ru/xml/rss/all.xml",
            "https://nplus1.ru/rss"
        ],
        "posts_per_day": 8
    },
    -1003381982796: {
        "title": "YandexRU",
        "description": "Новости Яндекса, технологий, интернета.",
        "link": "https://t.me/https_yandex_ru",
        "topics": ["яндекс", "технологии", "новости", "поиск"],
        "rss_sources": [
            "https://russian.rt.com/rss/",
            "https://iz.ru/xml/rss/all.xml",
            "https://nplus1.ru/rss"
        ],
        "posts_per_day": 6
    },
    -1003220451594: {
        "title": "M",
        "description": "Новости, IT, инструменты",
        "link": "https://t.me/Maksimkaq1",
        "topics": ["новости", "IT", "инструменты"],
        "rss_sources": [
            "https://russian.rt.com/rss/",
            "https://lenta.ru/rss/news",
            "https://iz.ru/xml/rss/all.xml"
        ],
        "posts_per_day": 6
    },
    -1003252915826: {
        "title": "Reklama",
        "description": "Свежие рекламные предложения, маркетинг.",
        "link": "https://t.me/ReklamaADX1",
        "topics": ["реклама", "маркетинг", "продвижение", "бизнес"],
        "rss_sources": [
            "https://vc.ru/rss",
            "https://www.cossa.ru/events/rss/",
            "https://russian.rt.com/rss/"
        ],
        "posts_per_day": 6
    },
    -1003497443207: {
        "title": "Durov",
        "description": "Новости о Дурове, Telegram, технологиях.",
        "link": "https://t.me/DUROV_NOT_FAKE",
        "topics": ["дуров", "telegram", "технологии", "новости"],
        "rss_sources": [
            "https://lenta.ru/rss/news",
            "https://habr.com/ru/rss/all/all/?fl=ru",
            "https://russian.rt.com/rss/"
        ],
        "posts_per_day": 6
    },
    -1003863551288: {
        "title": "Дедушка",
        "description": "Мудрые мысли, истории, советы.",
        "link": "https://t.me/DEDUIIIKA",
        "topics": ["мысли", "истории", "советы", "жизнь"],
        "rss_sources": [
            "https://www.adme.ru/feed/",
            "https://www.anekdot.ru/rss/export_j.xml",
            "https://iz.ru/xml/rss/all.xml"
        ],
        "posts_per_day": 6
    },
    -1003888741797: {
        "title": "Дуров",
        "description": "Всё о Дурове, Telegram и технологиях",
        "link": "https://t.me/DurovTelegramMessanger",
        "topics": ["дуров", "telegram", "новости", "технологии", "иновации"],
        "rss_sources": [
            "https://habr.com/ru/rss/all/all/?fl=ru",
            "https://russian.rt.com/rss/",
            "https://iz.ru/xml/rss/all.xml"
        ],
        "posts_per_day": 6
    },
    -1003867449619: {
        "title": "Убийца мира",
        "description": "Криминал, происшествия, загадочные события.",
        "link": "https://t.me/KILLER_WORLD_1",
        "topics": ["криминал", "происшествия", "загадки", "новости"],
        "rss_sources": [
            "https://www.interfax.ru/rss.asp",
            "https://lenta.ru/rss/news",
            "https://russian.rt.com/rss/"
        ],
        "posts_per_day": 6
    },
    -1003539952195: {
        "title": "🕵️‍♂️ OSINT (NEW)",
        "description": "OSINT-инструменты, методы, новости.",
        "link": "https://t.me/ProbivChelovekar0bot",
        "topics": ["OSINT", "инструменты", "методы", "расследования", "поиск", "новости"],
        "rss_sources": [
            "https://www.interfax.ru/rss.asp",
            "https://www.osintme.com/index.php/feed/",
            "https://iz.ru/xml/rss/all.xml",
            "https://postnauka.ru/feed"
        ],
        "posts_per_day": 6
    },
    -1003740108157: {
        "title": "GitHub",
        "description": "Интересные репозитории, новости GitHub, разработка.",
        "link": "https://t.me/GitHub_Commit",
        "topics": ["github", "разработка", "open source", "программирование"],
        "rss_sources": [
            "https://www.interfax.ru/rss.asp",
            "https://github.blog/feed/",
            "https://habr.com/ru/rss/hubs/programming/articles/",
            "https://iz.ru/xml/rss/all.xml"
        ],
        "posts_per_day": 6
    },
    -1003825497899: {
        "title": "Handle",
        "description": "Обработка информации, анализ данных, инструменты.",
        "link": "https://t.me/Handle_message",
        "topics": ["анализ данных", "инструменты", "обработка", "информация"],
        "rss_sources": [
            "https://habr.com/ru/rss/hubs/data_engineering/articles/",
            "https://iz.ru/xml/rss/all.xml",
            "https://nplus1.ru/rss"
        ],
        "posts_per_day": 6
    },
    -1003715932763: {
        "title": "It's ILON!",
        "description": "Илон Маск, SpaceX, Tesla, инновации.",
        "link": "https://t.me/EilonMaks",
        "topics": ["илон маск", "spacex", "tesla", "инновации"],
        "rss_sources": [
            "https://www.space.com/feeds/all",
            "https://techcrunch.com/feed/",
            "https://iz.ru/xml/rss/all.xml"
        ],
        "posts_per_day": 6
    },
    -1003895644764: {
        "title": "Вечеринка Эпштейна!",
        "description": "Скандалы, интриги, расследования.",
        "link": "https://t.me/Epstein_Party2",
        "topics": ["скандалы", "расследования", "новости"],
        "rss_sources": [
            "https://www.interfax.ru/rss.asp",
            "https://lenta.ru/rss/news",
            "https://iz.ru/xml/rss/all.xml"
        ],
        "posts_per_day": 6
    },
    -1003754883430: {
        "title": "SherlockBot",
        "description": "Поиск информации, OSINT-инструменты.",
        "link": "https://t.me/SherlockRobot1",
        "topics": ["OSINT", "поиск", "инструменты", "информация"],
        "rss_sources": [
            "https://www.interfax.ru/rss.asp",
            "https://russian.rt.com/rss/",
            "https://nplus1.ru/rss"
        ],
        "posts_per_day": 6
    },
    -1003836056023: {
        "title": "Vektor",
        "description": "Вектор атаки, кибербезопасность, защита.",
        "link": "https://t.me/VektorRobot1",
        "topics": ["кибербезопасность", "атаки", "защита", "уязвимости"],
        "rss_sources": [
            "https://www.interfax.ru/rss.asp",
            "https://xakep.ru/feed/",
            "http://www.securitylab.ru/_services/export/rss/news.php",
            "https://naked-science.ru/feed"
        ],
        "posts_per_day": 6
    },
    -1003896483277: {
        "title": "Супер-человек",
        "description": "Всё о человеке: здоровье, психология, саморазвитие.",
        "link": "https://t.me/SuperPuperChell",
        "topics": ["здоровье", "психология", "саморазвитие", "человек"],
        "rss_sources": [
            "https://takzdorovo.ru/rss/",
            "https://russian.rt.com/rss/",
            "https://iz.ru/xml/rss/all.xml"
        ],
        "posts_per_day": 6
    },
    -1003814514563: {
        "title": "MAXXX",
        "description": "Новости, IT, инструменты",
        "link": "https://t.me/MessengerMaksik",
        "topics": ["новости", "IT", "инструменты", "инновации"],
        "rss_sources": [
            "https://www.interfax.ru/rss.asp",
            "https://habr.com/ru/rss/all/all/?fl=ru",
            "https://lenta.ru/rss/news",
            "https://naked-science.ru/feed"
        ],
        "posts_per_day": 6
    },
    -1003727058869: {
        "title": "Помидор",
        "description": "Огородничество, новости, химикаты.",
        "link": "https://t.me/P0m1d0r_0gorod",
        "topics": ["огород", "новости", "растения", "ЗОЖ"],
        "rss_sources": [
            "https://russian.rt.com/rss/",
            "https://iz.ru/xml/rss/all.xml",
            "https://nplus1.ru/rss"
        ],
        "posts_per_day": 6
    },
    -1003802909728: {
        "title": "Девушка",
        "description": "Женский журнал: мода, красота, отношения, психология.",
        "link": "https://t.me/DevuIIIka",
        "topics": ["мода", "красота", "отношения", "психология"],
        "rss_sources": [
            "https://russian.rt.com/rss/",
            "https://iz.ru/xml/rss/all.xml",
            "https://nplus1.ru/rss"
        ],
        "posts_per_day": 6
    },
    -1003784125451: {
        "title": "ass",
        "description": "Юмор, мемы, приколы без цензуры.",
        "link": "https://t.me/ItsSuperUsername",
        "topics": ["юмор", "мемы", "приколы", "развлечения"],
        "rss_sources": [
            "https://www.anekdot.ru/rss/export_j.xml",
            "https://www.interfax.ru/rss.asp",
            "https://nplus1.ru/rss"
        ],
        "posts_per_day": 6
    },
    -1003809459289: {
        "title": "Uss",
        "description": "Новости, технологии, интересные факты.",
        "link": "https://t.me/tgsosallol",
        "topics": ["новости", "технологии", "факты", "интересно"],
        "rss_sources": [
            "https://lenta.ru/rss/news",
            "https://habr.com/ru/rss/all/all/?fl=ru",
            "https://nplus1.ru/rss",
            "https://naked-science.ru/feed"
        ],
        "posts_per_day": 6
    }
}

def update_channels():
    global CHANNELS

    try:
        response = requests.get(GITHUB_URL, timeout=15)
        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict):
            return False, "Config is not dict"

        CHANNELS = data
        return True, None

    except Exception as e:
        return False, str(e)

# ========================
#    ОЧЕРЕДЬ МОДЕРАЦИИ
# ========================
class ModerationItem:
    def __init__(self, channel_id: int, text: str, admin_messages: Dict[int, int]):
        self.channel_id = channel_id
        self.text = text
        self.admin_messages = admin_messages
        self.status = 'pending'

moderation_queue: Dict[int, ModerationItem] = {}
next_id = 0

# ========================
#    АВТО-ПРОВЕРКА ПОСТОВ
# ========================
def needs_moderation(text: str) -> bool:
    """
    True  -> отправить админам
    False -> опубликовать сразу
    """
    if "комментарии" in text.lower():
        return True
    if "личку" in text.lower():
        return True
    if "---" in text.lower():
        return True
    if "```" in text.lower():
        return True

    return False

# ========================
#    ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ========================
def clean_html_for_telegram(text: str) -> str:
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)

    text = re.sub(r'</?(ol|ul|li)[^>]*>', '', text, flags=re.IGNORECASE)

    text = re.sub(
        r'<li[^>]*>(.*?)</li>',
        r'• \1\n',
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    allowed_tags = ['b', 'strong', 'i', 'em', 'a', 'code', 'pre']

    def replace_tag(match):
        tag = match.group(0)

        tag_name_match = re.match(r'</?(\w+)', tag, re.IGNORECASE)

        if tag_name_match:
            tag_name = tag_name_match.group(1).lower()

            if tag_name in allowed_tags:
                return tag

        return ''

    text = re.sub(r'</?[\w][^>]*>', replace_tag, text)
    text = re.sub(r'\n\s*\n', '\n\n', text)

    return text.strip()

def is_valid_html(text: str) -> bool:
    tags = re.findall(r'<[^>]*>', text)

    stack = []

    for tag in tags:
        if tag.startswith('</'):
            if not stack:
                return False

            tag_name_match = re.match(r'</\s*([^\s>]+)', tag)

            if not tag_name_match:
                return False

            tag_name = tag_name_match.group(1)

            if stack[-1] != tag_name:
                return False

            stack.pop()

        elif tag.endswith('/>') or tag.lower() in ['<br>', '<hr>', '<img>']:
            continue

        else:
            tag_name_match = re.match(r'<\s*([^\s>/]+)', tag)

            if not tag_name_match:
                return False

            tag_name = tag_name_match.group(1)
            stack.append(tag_name)

    return len(stack) == 0

def fetch_news(channel_id: int) -> str:
    config = CHANNELS[channel_id]

    sources = config.get('rss_sources', [])

    news_text = ""

    for url in sources[:5]:
        try:
            feed = feedparser.parse(url)

            entries = feed.entries[:2]

            for entry in entries:
                title = entry.get('title', '')
                summary = entry.get('summary', '') or entry.get('description', '')

                news_text += f"{title}\n{summary}\n\n"

        except Exception as e:
            logging.warning(f"RSS error for {url}: {e}")
            continue

    if not news_text.strip():
        news_text = "Не удалось получить новости. Импровизируй."

    return news_text[:2000]

def generate_post(channel_id: int, topics: List[str], news_text: str, attempt: int = 0) -> Optional[str]:
    if not news_text.strip():
        news_text = f"Напиши интересный пост на тему {', '.join(topics)} без опоры на конкретные новости."

    if attempt >= 3:
        logging.error(f"Failed to generate valid HTML for channel {channel_id}")
        return None

    prompt = f"""Ты — профессиональный копирайтер для Telegram-канала "{CHANNELS[channel_id]['title']}" на темы {', '.join(topics)}.
Напиши информативный и интересный пост на основе следующего материала.
Пост должен быть уникальным, но иногда копируй материал дословно для большей точности.

### Технические требования (строго соблюдать):
1. **Только HTML-разметка** — Markdown запрещён категорически. Вместо двойных звёздочек используй тег <b>.
2. **Разрешённые теги**: <b>, <i>, <a href="...">, <code>, <pre>.
3. **Запрещены**: <u>, <ins>, <s>, <strike>, <del>, <ol>, <ul>, <li>, <br>, <p>, <div> и любые другие теги.
4. **Перенос строки**: между абзацами — одна пустая строка (два перевода строки). Внутри абзаца переносы не нужны.
5. **Списки**: если нужен список, используй символ • (U+2022) или цифры с точкой в начале строки, но не HTML-теги.
6. **Длина поста**: 500–700 символов (без учёта тегов).
7. **Не злоупотребляй эмодзи** — максимум 2–3 на пост, если они уместны.
8. **Не используй заглушки** — никаких example.com, и подобного. Не знаешь точной ссылки на ресурс - не вставляй.
9. **Никаких "пишите в комментариях** — канал не имеет чата, или комментариев. Не упоминай комментарии вообще.
10. **Максимально человечно** — старайся писать максимально человечно, не роботизированно.
11. **Ничего не делать админам** - Не пиши в начале "Вот ваш пост в указанном формате...", пиши сразу текст без лишней воды.
12. **Ничего про "смотрите в шапке канала..."** - Сам по себе канал ничего подобного не имеет. Не добавляй таким образом работы модерам.
13. **Никаких полосок** - В телеграме не работает "---". Не вставляй такого "перехода" нигде. Ставь просто перевод строки.

Материал для поста: {news_text}"""

    try:
        response = mistral_client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1.2,
            max_tokens=8192
        )

        text = response.choices[0].message.content.strip()

        text = text.replace("<br>", "\n")

        text = clean_html_for_telegram(text)

        text += "\n\n⭐️ Лучший бот с ИИ: @WortexAI_ChatBot"

        if is_valid_html(text):
            return text

        logging.warning(f"Invalid HTML attempt {attempt + 1}")

        return generate_post(
            channel_id,
            topics,
            news_text,
            attempt + 1
        )

    except Exception as e:
        if "429" in str(e):
            logging.error("429 received. Sleeping 5 minutes.")
            time.sleep(300)

        logging.error(f"Generation error: {e}")

        return None

def publish_post(channel_id: int, text: str) -> bool:
    try:
        clean_text = clean_html_for_telegram(text)

        bot.send_message(
            channel_id,
            clean_text,
            parse_mode='HTML'
        )

        logging.info(f"Post published to {channel_id}")

        return True

    except Exception as e:
        logging.error(f"Publish error: {e}")

        return False

def send_to_moderation(channel_id: int, text: str):
    global next_id

    item_id = next_id
    next_id += 1

    admin_messages = {}

    markup = InlineKeyboardMarkup(row_width=3)

    markup.add(
        InlineKeyboardButton(
            "✅ Подтвердить",
            callback_data=f"approve_{item_id}"
        ),
        InlineKeyboardButton(
            "❌ Отклонить",
            callback_data=f"reject_{item_id}"
        ),
        InlineKeyboardButton(
            "🔄 Перегенерировать",
            callback_data=f"regenerate_{item_id}"
        )
    )

    for admin_id in ADMINS:
        try:
            msg = bot.send_message(
                admin_id,
                f"<b>Новый пост для канала {CHANNELS[channel_id]['title']}</b>\n\n{text}",
                parse_mode='HTML',
                reply_markup=markup
            )

            admin_messages[admin_id] = msg.message_id

        except Exception as e:
            logging.error(f"Failed to send to admin {admin_id}: {e}")

    if admin_messages:
        moderation_queue[item_id] = ModerationItem(
            channel_id,
            text,
            admin_messages
        )

def create_post_for_channel(channel_id: int):
    logging.info(f"Generating post for channel {channel_id}")

    try:
        config = CHANNELS[channel_id]

    except KeyError:
        logging.error(f"Channel config not found: {channel_id}")
        return

    topics = config.get('topics', ['новости'])

    try:
        news = fetch_news(channel_id)

    except Exception as e:
        logging.error(f"News fetch error: {e}")
        news = ""

    post_text = generate_post(
        channel_id,
        topics,
        news
    )

    if not post_text:
        logging.error(f"Failed to generate post for channel {channel_id}")
        return

    try:
        moderation_required = needs_moderation(post_text)

    except Exception as e:
        logging.error(f"Moderation check failed: {e}")

        moderation_required = True

    if moderation_required:
        logging.info(f"Sent to moderation: {channel_id}")

        send_to_moderation(
            channel_id,
            post_text
        )

    else:
        logging.info(f"Auto approved: {channel_id}")

        success = publish_post(
            channel_id,
            post_text
        )

        if not success:
            logging.warning("Auto publish failed. Sending to moderation.")

            send_to_moderation(
                channel_id,
                post_text
            )

def initial_generation():
    logging.info("🚀 Initial generation started")

    for channel_id in CHANNELS.keys():
        try:
            create_post_for_channel(channel_id)

            time.sleep(30)

        except Exception as e:
            logging.error(f"Initial generation error: {e}")

    logging.info("✅ Initial generation completed")

# ========================
#    ОБРАБОТЧИКИ КОМАНД
# ========================
@bot.message_handler(content_types=['text'])
def handle_message(message):
    cid = message.chat.id
    txt = message.text.lower()
    if not cid in ADMINS:
        bot.reply_to(
            message,
            "Вы не админ."
        )
        return

    if txt == "/start":
        if message.from_user.id in ADMINS:
            bot.reply_to(
                message,
                "Привет, админ!"
            )

        else:
            bot.reply_to(
                message,
                "Доступ запрещён."
            )

    elif txt == "/update":
        if cid in ADMINS:
            status, error = update_channels()

            if status:
                bot.reply_to(
                    message,
                    f"Обновлено.\nКаналов: {len(CHANNELS)}"
                )

            else:
                bot.reply_to(
                    message,
                    f"Ошибка:\n{error}"
                )

        else:
            bot.reply_to(
                message,
                "Вы не админ."
            )
    elif txt.startswith("/broadcast"):
        if txt == "/broadcast":
            bot.reply_to(
                message,
                "Использование: /broadcast <текст>"
            )
            return
        text = message.text[len("/broadcast "):].strip()
        bot.send_message(cid, "Рассылка началась...")
        success, errors = 0, 0
        for channel in CHANNELS:
            try:
                bot.send_message(channel, text, parse_mode="HTML")
                success+=1
            except Exception as e:
                errors+=1
            time.sleep(0.5)
        bot.send_message(cid, f"Успешно: {success}\nОшибок: {errors}")

    else:
        bot.reply_to(
            message,
            "Неизвестная команда."
        )

# ========================
#    ОБРАБОТЧИК КОЛБЭКОВ
# ========================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call: CallbackQuery):
    data = call.data

    parts = data.split('_')

    if len(parts) != 2:
        bot.answer_callback_query(call.id, "Ошибка")
        return

    action, item_id_str = parts

    try:
        item_id = int(item_id_str)

    except ValueError:
        bot.answer_callback_query(call.id, "Ошибка ID")
        return

    item = moderation_queue.get(item_id)

    if not item:
        bot.answer_callback_query(call.id, "Уже обработано")

        try:
            bot.delete_message(
                call.message.chat.id,
                call.message.message_id
            )

        except:
            pass

        return

    if item.status != 'pending':
        bot.answer_callback_query(call.id, "Уже обработано")
        return

    if call.from_user.id not in ADMINS:
        bot.answer_callback_query(call.id, "Нет доступа")
        return

    item.status = 'processing'

    bot.answer_callback_query(call.id)

    if action == 'approve':
        try:
            success = publish_post(
                item.channel_id,
                item.text
            )

            if not success:
                raise Exception("Publish failed")

        except Exception as e:
            logging.error(f"Publish error: {e}")

            bot.send_message(
                call.from_user.id,
                f"❌ Ошибка публикации:\n{e}"
            )

            item.status = 'pending'
            return

        for admin_id, msg_id in item.admin_messages.items():
            try:
                bot.delete_message(admin_id, msg_id)

            except Exception as e:
                logging.warning(f"Delete error: {e}")

        del moderation_queue[item_id]

    elif action == 'reject':
        logging.info(f"Rejected: {item_id}")

        for admin_id, msg_id in item.admin_messages.items():
            try:
                bot.delete_message(admin_id, msg_id)

            except Exception as e:
                logging.warning(f"Delete error: {e}")

        del moderation_queue[item_id]

    elif action == 'regenerate':
        logging.info(f"Regenerating: {item_id}")

        for admin_id, msg_id in item.admin_messages.items():
            try:
                bot.delete_message(admin_id, msg_id)

            except Exception as e:
                logging.warning(f"Delete error: {e}")

        del moderation_queue[item_id]

        config = CHANNELS[item.channel_id]

        topics = config.get('topics', ['новости'])

        news = fetch_news(item.channel_id)

        new_text = generate_post(
            item.channel_id,
            topics,
            news
        )

        if new_text:
            send_to_moderation(
                item.channel_id,
                new_text
            )

            bot.send_message(
                call.from_user.id,
                "🔄 Новый вариант отправлен"
            )

        else:
            bot.send_message(
                call.from_user.id,
                "❌ Ошибка генерации"
            )

# ========================
#    ПЛАНИРОВЩИК
# ========================
def schedule_jobs():
    for channel_id, config in CHANNELS.items():
        minutes = int(
            (24 * 60) /
            config.get('posts_per_day', 2)
        )

        schedule.every(minutes).minutes.do(
            create_post_for_channel,
            channel_id
        )

        logging.info(
            f"Scheduled {config['title']} every {minutes} minutes"
        )

def run_schedule():
    while True:
        try:
            schedule.run_pending()

        except Exception as e:
            logging.error(f"Scheduler error: {e}")

        time.sleep(30)

# ========================
#    ЗАПУСК
# ========================
if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    schedule_jobs()

    gen_thread = threading.Thread(
        target=initial_generation,
        daemon=True
    )

    gen_thread.start()

    threading.Thread(
        target=run_schedule,
        daemon=True
    ).start()

    logging.info("Bot started")

    while True:
        try:
            bot.infinity_polling(
                timeout=60,
                long_polling_timeout=60
            )

        except Exception as e:
            logging.error(f"Polling error: {e}")

            time.sleep(15)
