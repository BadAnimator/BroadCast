import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import schedule
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
TELEGRAM_BOT_TOKEN = "8650040948:AAHbVAM9BIuETrnWcDFI66cfj1cWhajJd6M"            # Токен твоего бота
MISTRAL_API_KEY = "6bHT7e3TE0TPnfdsNsols5JkkgfSB8VC"         # Ключ от Mistral AI
ADMINS = [6036761167, 6419615188]                   # ID администраторов (можно несколько)

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
            "https://www.securitylab.ru/export/rss/",
            "https://xakep.ru/feed/",
            "https://habr.com/ru/rss/hubs/infosec/articles/"
        ],
        "posts_per_day": 2
    },
    -1002515949890: {
        "title": "Stalin-OSINT",
        "description": "OSINT-расследования, методы поиска информации, утечки данных.",
        "link": "https://t.me/osint_stalin",
        "topics": ["OSINT", "расследования", "поиск информации", "данные"],
        "rss_sources": [
            "https://www.osintme.com/index.php/feed/",
            "https://medium.com/feed/tag/osint"
        ],
        "posts_per_day": 2
    },
    -1002758779598: {
        "title": "True-Killer",
        "description": "Криминальные новости, истории, расследования.",
        "link": "https://t.me/true_killer",
        "topics": ["криминал", "новости", "расследования", "происшествия"],
        "rss_sources": [
            "https://lenta.ru/rss/topics/criminal/",
            "https://www.kommersant.ru/RSS/news.xml"
        ],
        "posts_per_day": 2
    },
    -1002914714454: {
        "title": "ARECTOBAH_3A_PKH",
        "description": "Юмор, мемы, приколы, забавные истории.",
        "link": "https://t.me/APECTOBAH_3A_PKH",
        "topics": ["юмор", "мемы", "приколы", "развлечения"],
        "rss_sources": [
            "https://pikabu.ru/feed/feed.rss",
            "https://www.anekdot.ru/rss/export_joke_new.xml"
        ],
        "posts_per_day": 2
    },
    -1003021980862: {
        "title": "DARK-IntenretS",
        "description": "Тёмная сторона интернета, технологии, уязвимости.",
        "link": "https://t.me/dark_internets",
        "topics": ["интернет", "технологии", "безопасность", "уязвимости"],
        "rss_sources": [
            "https://habr.com/ru/rss/hubs/infosec/articles/",
            "https://www.securitylab.ru/export/rss/"
        ],
        "posts_per_day": 2
    },
    -1002468234153: {
        "title": "Attack-APATIA",
        "description": "Кибератаки, уязвимости, защита.",
        "link": "https://t.me/attack_apatia",
        "topics": ["кибератаки", "уязвимости", "защита", "инциденты"],
        "rss_sources": [
            "https://xakep.ru/feed/",
            "https://www.securitylab.ru/export/rss/"
        ],
        "posts_per_day": 2
    },
    -1003391258799: {
        "title": "Поиск людей бот",
        "description": "Методы поиска людей, OSINT, советы.",
        "link": "https://t.me/People_Searchrobot",
        "topics": ["поиск людей", "OSINT", "инструменты", "советы"],
        "rss_sources": [
            "https://medium.com/feed/tag/osint"
        ],
        "posts_per_day": 2
    },
    -1003395961959: {
        "title": "Пробивчик?",
        "description": "Пробив информации, базы данных, утечки.",
        "link": "https://t.me/Probitb_cheloveka",
        "topics": ["пробив", "базы данных", "утечки", "информация"],
        "rss_sources": [
            "https://www.opennet.ru/opennews/opennews_all.rss"
        ],
        "posts_per_day": 2
    },
    -1003381982796: {
        "title": "YandexRU",
        "description": "Новости Яндекса, технологий, интернета.",
        "link": "https://t.me/https_yandex_ru",
        "topics": ["яндекс", "технологии", "новости", "поиск"],
        "rss_sources": [
            "https://yandex.ru/news/export/rss2.xml"
        ],
        "posts_per_day": 2
    },
    -1003546469611: {
        "title": "T",
        "description": "Технологии, робототехника, искусственный интеллект.",
        "link": "https://t.me/transformer16",
        "topics": ["робототехника", "искусственный интеллект", "нейросети", "технологии"],
        "rss_sources": [
            "https://habr.com/ru/rss/hubs/ai/articles/",
            "https://techcrunch.com/feed/"
        ],
        "posts_per_day": 2
    },
    -1003220451594: {
        "title": "M",
        "description": "Личный блог, мысли, новости, IT.",
        "link": "https://t.me/Maksimkaq1",
        "topics": ["личное", "новости", "IT", "жизнь"],
        "rss_sources": [
            "https://habr.com/ru/rss/news/",
            "https://lenta.ru/rss/latest/"
        ],
        "posts_per_day": 2
    },
    -1003252915826: {
        "title": "Reklama",
        "description": "Свежие рекламные предложения, маркетинг.",
        "link": "https://t.me/ReklamaADX1",
        "topics": ["реклама", "маркетинг", "продвижение", "бизнес"],
        "rss_sources": [
            "https://vc.ru/rss",
            "https://www.cossa.ru/events/rss/"
        ],
        "posts_per_day": 2
    },
    -1003497443207: {
        "title": "Durov",
        "description": "Новости о Дурове, Telegram, технологиях.",
        "link": "https://t.me/DUROV_NOT_FAKE",
        "topics": ["дуров", "telegram", "технологии", "новости"],
        "rss_sources": [
            "https://lenta.ru/rss/latest/",
            "https://habr.com/ru/rss/news/"
        ],
        "posts_per_day": 2
    },
    -1003863551288: {
        "title": "Дедушка",
        "description": "Мудрые мысли, истории, советы.",
        "link": "https://t.me/DEDUIIIKA",
        "topics": ["мысли", "истории", "советы", "жизнь"],
        "rss_sources": [
            "https://www.adme.ru/feed/",
            "https://www.anekdot.ru/rss/export_joke_new.xml"
        ],
        "posts_per_day": 2
    },
    -1003888741797: {
        "title": "Дуров",
        "description": "Всё о Дурове и Telegram.",
        "link": "https://t.me/DurovTelegramMessanger",
        "topics": ["дуров", "telegram", "новости", "технологии"],
        "rss_sources": [
            "https://habr.com/ru/rss/news/"
        ],
        "posts_per_day": 2
    },
    -1003867449619: {
        "title": "Убийца мира",
        "description": "Криминал, происшествия, загадочные события.",
        "link": "https://t.me/KILLER_WORLD_1",
        "topics": ["криминал", "происшествия", "загадки", "новости"],
        "rss_sources": [
            "https://lenta.ru/rss/topics/criminal/",
            "https://www.kommersant.ru/RSS/news.xml"
        ],
        "posts_per_day": 2
    },
    -1003539952195: {
        "title": "🕵️‍♂️ OSINT (NEW)",
        "description": "OSINT-инструменты, методы, новости.",
        "link": "https://t.me/ProbivChelovekar0bot",
        "topics": ["OSINT", "инструменты", "методы", "расследования"],
        "rss_sources": [
            "https://medium.com/feed/tag/osint",
            "https://www.osintme.com/index.php/feed/"
        ],
        "posts_per_day": 2
    },
    -1003740108157: {
        "title": "GitHub",
        "description": "Интересные репозитории, новости GitHub, разработка.",
        "link": "https://t.me/GitHub_Commit",
        "topics": ["github", "разработка", "open source", "программирование"],
        "rss_sources": [
            "https://github.blog/feed/",
            "https://habr.com/ru/rss/hubs/programming/articles/"
        ],
        "posts_per_day": 2
    },
    -1003825497899: {
        "title": "Handle",
        "description": "Обработка информации, анализ данных, инструменты.",
        "link": "https://t.me/Handle_message",
        "topics": ["анализ данных", "инструменты", "обработка", "информация"],
        "rss_sources": [
            "https://habr.com/ru/rss/hubs/data_engineering/articles/"
        ],
        "posts_per_day": 2
    },
    -1003715932763: {
        "title": "It's ILON!",
        "description": "Илон Маск, SpaceX, Tesla, инновации.",
        "link": "https://t.me/EilonMaks",
        "topics": ["илон маск", "spacex", "tesla", "инновации"],
        "rss_sources": [
            "https://www.space.com/feeds/all",
            "https://techcrunch.com/feed/"
        ],
        "posts_per_day": 2
    },
    -1003895644764: {
        "title": "Вечеринка Эпштейна!",
        "description": "Скандалы, интриги, расследования.",
        "link": "https://t.me/Epstein_Party2",
        "topics": ["скандалы", "расследования", "новости", "интриги"],
        "rss_sources": [
            "https://lenta.ru/rss/latest/",
            "https://www.kommersant.ru/RSS/news.xml"
        ],
        "posts_per_day": 2
    },
    -1003754883430: {
        "title": "SherlockBot",
        "description": "Поиск информации, OSINT-инструменты.",
        "link": "https://t.me/SherlockRobot1",
        "topics": ["OSINT", "поиск", "инструменты", "информация"],
        "rss_sources": [
            "https://medium.com/feed/tag/osint"
        ],
        "posts_per_day": 2
    },
    -1003836056023: {
        "title": "Vektor",
        "description": "Вектор атаки, кибербезопасность, защита.",
        "link": "https://t.me/VektorRobot1",
        "topics": ["кибербезопасность", "атаки", "защита", "уязвимости"],
        "rss_sources": [
            "https://xakep.ru/feed/",
            "https://www.securitylab.ru/export/rss/"
        ],
        "posts_per_day": 2
    },
    -1003896483277: {
        "title": "Супер-человек",
        "description": "Всё о человеке: здоровье, психология, саморазвитие.",
        "link": "https://t.me/SuperPuperChell",
        "topics": ["здоровье", "психология", "саморазвитие", "человек"],
        "rss_sources": [
            "https://takzdorovo.ru/rss/",
            "https://www.psychologies.ru/feed/"
        ],
        "posts_per_day": 2
    },
    -1003814514563: {
        "title": "MAXXX",
        "description": "Блог Макса, мысли, новости, IT.",
        "link": "https://t.me/MessengerMaksik",
        "topics": ["личное", "новости", "IT", "жизнь"],
        "rss_sources": [
            "https://habr.com/ru/rss/news/",
            "https://lenta.ru/rss/latest/"
        ],
        "posts_per_day": 2
    },
    -1003727058869: {
        "title": "Помидор",
        "description": "Огородничество, растения, дача, полезные советы.",
        "link": "https://t.me/P0m1d0r_0gorod",
        "topics": ["огород", "растения", "дача", "советы"],
        "rss_sources": [
            "https://www.supersadovnik.ru/export/rss.xml",
            "https://7dach.ru/feed"
        ],
        "posts_per_day": 2
    },
    -1003802909728: {
        "title": "Девушка",
        "description": "Женский журнал: мода, красота, отношения, психология.",
        "link": "https://t.me/DevuIIIka",
        "topics": ["мода", "красота", "отношения", "психология"],
        "rss_sources": [
            "https://www.cosmo.ru/feed/",
            "https://www.psychologies.ru/feed/"
        ],
        "posts_per_day": 2
    },
    -1003784125451: {
        "title": "ass",
        "description": "Юмор, мемы, приколы без цензуры.",
        "link": "https://t.me/ItsSuperUsername",
        "topics": ["юмор", "мемы", "приколы", "развлечения"],
        "rss_sources": [
            "https://pikabu.ru/feed/feed.rss",
            "https://www.anekdot.ru/rss/export_joke_new.xml"
        ],
        "posts_per_day": 2
    },
    -1003809459289: {
        "title": "Uss",
        "description": "Новости, технологии, интересные факты.",
        "link": "https://t.me/tgsosallol",
        "topics": ["новости", "технологии", "факты", "интересно"],
        "rss_sources": [
            "https://lenta.ru/rss/latest/",
            "https://habr.com/ru/rss/news/"
        ],
        "posts_per_day": 2
    }
}

# ========================
#    ОЧЕРЕДЬ МОДЕРАЦИИ
# ========================
class ModerationItem:
    def __init__(self, channel_id: int, text: str, admin_messages: Dict[int, int]):
        self.channel_id = channel_id
        self.text = text
        self.admin_messages = admin_messages  # {admin_id: message_id}
        self.status = 'pending'  # pending, approved, rejected, regenerating

moderation_queue: Dict[int, ModerationItem] = {}
next_id = 0

# ========================
#    ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ========================
def clean_html_for_telegram(text: str) -> str:
    """
    Оставляет только разрешённые теги: b, i, a, code, pre.
    Заменяет <br> на \n.
    Преобразует списки в читаемый вид.
    """
    # Замена <br>
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)

    # Удаление тегов списков
    text = re.sub(r'</?(ol|ul|li)[^>]*>', '', text, flags=re.IGNORECASE)

    # Замена <li> на маркер (если вдруг остались)
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'• \1\n', text, flags=re.IGNORECASE | re.DOTALL)

    # Разрешённые теги
    allowed_tags = ['b', 'strong', 'i', 'em', 'a', 'code', 'pre']
    # Но strong и em дублируют b и i, оставим для совместимости
    # Можно расширить список, но в промпте мы просим использовать только b, i, a, code, pre

    def replace_tag(match):
        tag = match.group(0)
        tag_name_match = re.match(r'</?(\w+)', tag, re.IGNORECASE)
        if tag_name_match:
            tag_name = tag_name_match.group(1).lower()
            if tag_name in allowed_tags:
                return tag
        return ''

    text = re.sub(r'</?[\w][^>]*>', replace_tag, text)
    text = re.sub(r'\n\s*\n', '\n\n', text)  # нормализация пустых строк
    return text.strip()

def is_valid_html(text: str, max_attempts: int = 3) -> bool:
    """
    Простейшая проверка валидности HTML: баланс открывающих/закрывающих тегов.
    Для production лучше использовать более строгую проверку.
    """
    # Убираем всё, что не в тегах, и проверяем баланс
    tags = re.findall(r'<[^>]*>', text)
    stack = []
    for tag in tags:
        if tag.startswith('</'):
            # закрывающий тег
            if not stack:
                return False
            # убираем слэш и возможные пробелы
            tag_name = re.match(r'</\s*([^\s>]+)', tag).group(1)
            if stack[-1] != tag_name:
                return False
            stack.pop()
        elif tag.endswith('/>') or tag in ['<br>', '<hr>', '<img>']:
            # одиночный тег - пропускаем
            continue
        else:
            # открывающий тег
            tag_name = re.match(r'<\s*([^\s>/]+)', tag).group(1)
            stack.append(tag_name)
    return len(stack) == 0

def fetch_news(channel_id: int) -> str:
    """Собирает последние новости из RSS-источников канала."""
    config = CHANNELS[channel_id]
    sources = config.get('rss_sources', [])
    news_text = ""
    for url in sources[:3]:  # не более 3 источников
        try:
            feed = feedparser.parse(url)
            entries = feed.entries[:2]  # последние 2 новости
            for entry in entries:
                title = entry.get('title', '')
                summary = entry.get('summary', '') or entry.get('description', '')
                news_text += f"{title}\n{summary}\n\n"
        except Exception as e:
            logging.warning(f"RSS error for {url}: {e}")
            continue
    if not news_text.strip():
        news_text = "Новости на сегодня: интересные события в мире технологий."
    return news_text[:2000]  # ограничим длину

def generate_post(channel_id: int, topics: List[str], news_text: str, attempt: int = 0) -> Optional[str]:
    """
    Генерирует пост через Mistral, проверяет HTML-валидность.
    При неудаче делает до 3 попыток.
    """
    if not news_text.strip():
        news_text = f"Напиши интересный пост на тему {', '.join(topics)} без опоры на конкретные новости."
    if attempt >= 3:
        logging.error(f"Failed to generate valid HTML for channel {channel_id} after 3 attempts")
        return None

    prompt = f"""Ты — профессиональный копирайтер для Telegram-канала "{CHANNELS[channel_id]['title']}" на тему {', '.join(topics)}.
Напиши информативный и интересный пост на основе следующего материала. Пост должен быть уникальным, не копируй материал дословно.

### Технические требования (строго соблюдать):
1. **Только HTML-разметка** — Markdown запрещён категорически.
2. **Разрешённые теги**: <b>, <i>, <a href="...">, <code>, <pre>.
3. **Запрещены**: <u>, <ins>, <s>, <strike>, <del>, <ol>, <ul>, <li>, <br>, <p>, <div> и любые другие теги.
4. **Перенос строки**: между абзацами — одна пустая строка (два перевода строки). Внутри абзаца переносы не нужны.
5. **Списки**: если нужен список, используй символ • (U+2022) или цифры с точкой в начале строки, но не HTML-теги.
6. **Длина поста**: 400–700 символов (без учёта тегов).
7. **Не злоупотребляй эмодзи** — максимум 2–3 на пост, если они уместны.

Материал для поста:
{news_text}"""
    try:
        response = mistral_client.chat.complete(
            model="labs-mistral-small-creative",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.4,
            max_tokens=4096
        )
        text = response.choices[0].message.content.strip().replace("<br>", "\n")
        text = clean_html_for_telegram(text)
        text = text + "\n⭐️ Лучший бот с ИИ: @WortexAI_ChatBot"
        if is_valid_html(text):
            return text
        else:
            logging.warning(f"Invalid HTML (attempt {attempt+1}), regenerating...")
            return generate_post(channel_id, topics, news_text, attempt+1)
    except Exception as e:
        logging.error(f"Generation error: {e}")
        return None

def send_to_moderation(channel_id: int, text: str):
    """Отправляет пост на модерацию всем админам."""
    print(text)
    global next_id
    item_id = next_id
    next_id += 1
    admin_messages = {}
    markup = InlineKeyboardMarkup(row_width=3)
    #logging.info(f"📤 Отправка кнопок: approve_{item_id}, reject_{item_id}, regenerate_{item_id}")
    #print(f"📤 Отправка кнопок: approve_{item_id}, reject_{item_id}, regenerate_{item_id}")
    markup.add(
        InlineKeyboardButton("✅ Подтвердить", callback_data=f"approve_{item_id}"),
        InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{item_id}"),
        InlineKeyboardButton("🔄 Перегенерировать", callback_data=f"regenerate_{item_id}")
    )
    for admin_id in ADMINS:
        try:
            logging.info(f"📤 Отправка кнопок: approve_{item_id}, reject_{item_id}, regenerate_{item_id}")
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
        moderation_queue[item_id] = ModerationItem(channel_id, text, admin_messages)

def create_post_for_channel(channel_id: int):
    """Основная функция: собирает новости, генерирует пост и отправляет на модерацию."""
    logging.info(f"Generating post for channel {channel_id}")
    config = CHANNELS[channel_id]
    topics = config.get('topics', ['новости'])
    news = fetch_news(channel_id)
    post_text = generate_post(channel_id, topics, news)
    if post_text:
        send_to_moderation(channel_id, post_text)
    else:
        logging.error(f"Failed to generate post for channel {channel_id}")

def initial_generation():
    """Генерирует первые посты для всех каналов."""
    logging.info("🚀 Запуск первичной генерации постов...")
    for channel_id in CHANNELS.keys():
        try:
            create_post_for_channel(channel_id)
            time.sleep(2)  # небольшая пауза между запросами
        except Exception as e:
            logging.error(f"Ошибка при первичной генерации для канала {channel_id}: {e}")
    logging.info("✅ Первичная генерация завершена.")

# ========================
#    ОБРАБОТЧИКИ КОМАНД
# ========================
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in ADMINS:
        bot.reply_to(message, "Привет, админ! Я буду присылать посты на модерацию.")
    else:
        bot.reply_to(message, "Я бот для автоматического постинга. Доступ только администраторам.")

# ========================
#    ОБРАБОТЧИК КОЛБЭКОВ
# ========================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call: CallbackQuery):
    print(f"🔥 Колбэк получен: {call.data}")  # для отладки
    data = call.data
    parts = data.split('_')
    if len(parts) != 2:
        bot.answer_callback_query(call.id, "Неверный формат данных")
        return
    action, item_id_str = parts
    try:
        item_id = int(item_id_str)
    except ValueError:
        bot.answer_callback_query(call.id, "Ошибка ID")
        return

    # Получаем элемент из очереди
    item = moderation_queue.get(item_id)
    if not item:
        bot.answer_callback_query(call.id, "Пост уже обработан")
        # Попробуем удалить сообщение, если оно ещё висит
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        return

    # Проверяем, что пост ещё ожидает модерации
    if item.status != 'pending':
        bot.answer_callback_query(call.id, "Пост уже обработан")
        return

    # Проверяем, что админ имеет право
    if call.from_user.id not in ADMINS:
        bot.answer_callback_query(call.id, "Вы не админ")
        return

    # Устанавливаем статус "в обработке", чтобы другие админы не могли нажать
    item.status = 'processing'

    # Отвечаем на callback, чтобы убрать "часики" на кнопке
    bot.answer_callback_query(call.id)

    # Обработка действий
    if action == 'approve':
        try:
            # Очищаем текст от неподдерживаемых тегов
            clean_text = clean_html_for_telegram(item.text)
            bot.send_message(item.channel_id, clean_text, parse_mode='HTML')
            logging.info(f"Пост опубликован в канал {item.channel_id}")
        except Exception as e:
            logging.error(f"Ошибка публикации: {e}")
            bot.send_message(call.from_user.id, f"❌ Ошибка публикации: {e}")
            item.status = 'pending'  # возвращаем в очередь
            return

        # Удаляем сообщения у всех админов
        for admin_id, msg_id in item.admin_messages.items():
            try:
                bot.delete_message(admin_id, msg_id)
            except Exception as e:
                logging.warning(f"Не удалось удалить сообщение у админа {admin_id}: {e}")

        # Удаляем из очереди
        del moderation_queue[item_id]

    elif action == 'reject':
        logging.info(f"Пост {item_id} отклонён админом {call.from_user.id}")

        # Удаляем сообщения у всех админов
        for admin_id, msg_id in item.admin_messages.items():
            try:
                bot.delete_message(admin_id, msg_id)
            except Exception as e:
                logging.warning(f"Не удалось удалить сообщение у админа {admin_id}: {e}")

        # Удаляем из очереди
        del moderation_queue[item_id]

    elif action == 'regenerate':
        logging.info(f"Запрошена перегенерация поста {item_id}")

        # Удаляем старые сообщения
        for admin_id, msg_id in item.admin_messages.items():
            try:
                bot.delete_message(admin_id, msg_id)
            except Exception as e:
                logging.warning(f"Не удалось удалить сообщение у админа {admin_id}: {e}")

        # Удаляем старый элемент
        del moderation_queue[item_id]

        # Генерируем новый пост
        config = CHANNELS[item.channel_id]
        topics = config.get('topics', ['новости'])
        news = fetch_news(item.channel_id)
        new_text = generate_post(item.channel_id, topics, news)

        if new_text:
            send_to_moderation(item.channel_id, new_text)
            bot.send_message(call.from_user.id, "🔄 Новый вариант отправлен на модерацию")
        else:
            bot.send_message(call.from_user.id, "❌ Не удалось сгенерировать новый пост")
# ========================
#    ПЛАНИРОВЩИК
# ========================
def schedule_jobs():
    """Настраивает расписание для всех каналов."""
    for channel_id, config in CHANNELS.items():
        interval = 24 / config.get('posts_per_day', 2)  # часы
        schedule.every(interval).hours.do(create_post_for_channel, channel_id)
        logging.info(f"Scheduled {config['title']} every {interval} hours")

def run_schedule():
    """Запускает планировщик в фоновом потоке."""
    while True:
        schedule.run_pending()
        time.sleep(60)

# ========================
#    ЗАПУСК
# ========================
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Настраиваем расписание
    schedule_jobs()
    gen_thread = threading.Thread(target=initial_generation, daemon=True)
    gen_thread.start()

    # Запускаем планировщик в отдельном потоке
    threading.Thread(target=run_schedule, daemon=True).start()

    # Запускаем бота
    logging.info("Bot started")
    bot.infinity_polling()