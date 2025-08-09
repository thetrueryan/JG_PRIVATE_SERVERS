import asyncio

from aiocryptopay.models.invoice import Invoice  # type: ignore[import-untyped]

from loggers.logger import logger
from payment.crypto_init import crypto


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
