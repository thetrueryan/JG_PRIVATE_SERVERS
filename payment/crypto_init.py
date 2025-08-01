from aiocryptopay import AioCryptoPay, Networks

from config.settings import CRYPTOBOT_API_TOKEN

crypto = AioCryptoPay(token=CRYPTOBOT_API_TOKEN, network=Networks.MAIN_NET)
