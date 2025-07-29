from payment.crypto_init import crypto
from aiocryptopay.models.invoice import Invoice

async def get_crypto_invoice(total_price: float) -> Invoice:
    invoice = await crypto.create_invoice(
                    currency_type="fiat", 
                    fiat="RUB", 
                    amount=total_price, 
                    expires_in=30,
                )
    return invoice