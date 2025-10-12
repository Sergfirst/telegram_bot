import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== КОНФИГУРАЦИЯ =====
TOKEN = os.getenv("RAILWAY_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
SUPPORT_NICKNAME = "@zuzihelp"  # Замените на никнейм техподдержки
PDF_INSTRUCTION = "instruction.pdf"  # Путь к файлу инструкции
PDF_BOOK = "book.pdf"  # Путь к файлу книги

# ===== ОБРАБОТЧИКИ КОМАНД =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    welcome_text = """
👋 Добро пожаловать! Я ваш помощник.

📚 Вот доступные команды:

/instruction - Отправляет инструкцию по использованию бота (PDF файл)

/book - Отправляет справочную книгу (PDF файл)

/support - Показывает контакт техподдержки

Для использования команды просто напишите её в чат.
    """
    await update.message.reply_text(welcome_text)


async def instruction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /instruction"""
    try:
        with open(PDF_INSTRUCTION, 'rb') as f:
            await update.message.reply_document(
                document=f,
                caption="📄 Вот ваша инструкция"
            )
    except FileNotFoundError:
        await update.message.reply_text(
            "❌ Файл инструкции не найден. Обратитесь в поддержку."
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке инструкции: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка. Попробуйте позже."
        )


async def book(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /book"""
    try:
        with open(PDF_BOOK, 'rb') as f:
            await update.message.reply_document(
                document=f,
                caption="📖 Вот ваша книга"
            )
    except FileNotFoundError:
        await update.message.reply_text(
            "❌ Файл книги не найден. Обратитесь в поддержку."
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке книги: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка. Попробуйте позже."
        )


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /support"""
    message = f"""
📞 Свяжитесь с технической поддержкой:

👤 Никнейм: {SUPPORT_NICKNAME}

Напишите сообщение поддержке для решения проблем.
    """
    await update.message.reply_text(message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
📚 Доступные команды:

/start - Показать приветствие и инструкцию
/instruction - Отправить PDF инструкцию
/book - Отправить PDF книгу
/support - Показать контакт поддержки
/help - Показать эту справку
    """
    await update.message.reply_text(help_text)


# ===== ОСНОВНАЯ ФУНКЦИЯ =====

def main() -> None:
    """Запуск бота"""
    # Создаём приложение
    app = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("instruction", instruction))
    app.add_handler(CommandHandler("book", book))
    app.add_handler(CommandHandler("support", support))
    app.add_handler(CommandHandler("help", help_command))

    # Запускаем бота
    print("✅ Бот запущен...")
    app.run_polling()


if __name__ == '__main__':
    main()
