from payment.crypto_init import crypto
from aiocryptopay.models.invoice import Invoice
from decorators.logging_decorator import log_call


@log_call
async def get_crypto_invoice(total_price: float) -> Invoice:
    invoice = await crypto.create_invoice(
        currency_type="fiat",
        fiat="RUB",
        amount=total_price,
        expires_in=900,
    )
    return invoice
