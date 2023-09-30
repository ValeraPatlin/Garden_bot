import bot


import logging


logging.basicConfig(level = logging.DEBUG , filename = "logger.log")   # , filename = "logger.log"

logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("aiogram").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)



def main() -> None:
    bot.bot_start()



if __name__ == "__main__":
    main()
    

