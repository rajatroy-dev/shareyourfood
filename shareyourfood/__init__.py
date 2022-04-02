import azure.functions as func
import logging

from shareyourfood.bot.start import Start


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    bot = Start(req)
    bot.chat()

    return func.HttpResponse(
        'This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.',
        status_code=200
    )
