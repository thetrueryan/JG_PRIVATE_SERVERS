import asyncio
from aiocryptopay.models.invoice import Invoice

from db.repositories.core import AsyncCore
from payment.crypto_init import crypto
from config.logger import logger

async def check_invoice_status_loop(invoice: Invoice) -> bool:
    invoice_id = invoice.invoice_id
    logger.info(f"Начало проверки статуса у invoice {invoice_id}")
    while invoice.status == "active":
        await asyncio.sleep(10)
        invoices = await crypto.get_invoices(invoice_ids=[invoice_id])
        if isinstance(invoices, list):
                invoice = invoices[0]
                
    if invoice.status == "paid":
        await AsyncCore.update_paid_status(invoice_id, status_name="paid", paid_at=True, expired_at=True)
        return True
    
    if invoice.status == "expired":
         await AsyncCore.update_paid_status(invoice_id, status_name="expired")

    return False