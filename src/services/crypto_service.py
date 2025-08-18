import asyncio

from aiocryptopay.models.invoice import Invoice  # type: ignore[import-untyped]

from core.decorators import log_call
from core.logger import logger
from core.crypto_init import crypto


@log_call
async def get_crypto_invoice(total_price: float) -> Invoice:
    invoice = await crypto.create_invoice(
        currency_type="fiat",
        fiat="RUB",
        amount=total_price,
        expires_in=900,
    )
    return invoice


async def check_invoice_status_loop(invoice: Invoice) -> str | None:
    invoice_id = invoice.invoice_id
    logger.info(f"Начало проверки статуса у invoice {invoice_id}")
    while invoice.status == "active":
        await asyncio.sleep(10)
        invoices = await crypto.get_invoices(invoice_ids=[invoice_id])
        if isinstance(invoices, list):
            invoice = invoices[0]

    if invoice.status == "paid":
        return "paid"

    if invoice.status == "expired":
        return "expired"

    return None
