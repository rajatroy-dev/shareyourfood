import azure.functions as func
import logging

from shareyourfood.bot.start import Start


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    bot = Start(req)
    bot.chat()

    # location_keyboard = KeyboardButton(
    #     text="send_location", request_location=True)
    # contact_keyboard = KeyboardButton(
    #     text="send_contact", request_contact=True)
    # custom_keyboard = [[location_keyboard, contact_keyboard]]
    # reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    # bot.send_message(chat_id=update.message.chat.id,
    #                  text="Would you mind sharing your location and contact with me?",
    #                  reply_markup=reply_markup)

    # bot.send_message(chat_id=update.message.chat.id,
    #                  text=f"Echo: {update.message.text}",
    #                  reply_markup=ReplyKeyboardRemove())

    return func.HttpResponse(
        "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
        status_code=200
    )
