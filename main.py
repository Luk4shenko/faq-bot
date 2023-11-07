import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Начальное состояние
START, FAQ = range(2)

# FAQ-сообщения (здесь вы можете добавить свои вопросы и ответы)
faq_messages = {
    "Привет": "Привет! Чем я могу вам помочь?",
    "Как я могу узнать свой ID?": "Ваш ID: {}",
    "Какой смысл жизни?": "Смысл жизни - это вечный вопрос. Что для вас важно в жизни?",
    "Спасибо": "Пожалуйста! Если у вас есть еще вопросы, не стесняйтесь спрашивать.",
}

# Функция обработки команды /start
def start(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    context.user_data['user_id'] = user_id
    update.message.reply_text("Добро пожаловать! Я готов помочь вам. Ваш ID: {}".format(user_id))
    return FAQ

# Функция обработки вопросов
def faq(update: Update, context: CallbackContext) -> int:
    user_id = context.user_data.get('user_id')
    text = update.message.text
    if text in faq_messages:
        response = faq_messages[text].format(user_id)
        update.message.reply_text(response)
    else:
        update.message.reply_text("Извините, я не понимаю ваш вопрос. Попробуйте еще раз или используйте команду /start.")
    return FAQ

# Функция для остановки бота
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("До свидания! Если у вас возникнут еще вопросы, вы всегда можете вернуться.")
    return ConversationHandler.END

def main():
    updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FAQ: [MessageHandler(Filters.text & ~Filters.command, faq)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
