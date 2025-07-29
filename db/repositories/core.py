from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from typing import Optional
from datetime import datetime, timedelta

from db.models.database import Base
from db.models.models import UsersOrm, ServersOrm, OrdersOrm
from db.session import async_session_factory, async_engine
from decorators.logging_decorator import log_call
from config.logger import logger


class AsyncCore:
    @log_call
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)
            
    @log_call
    @staticmethod
    async def add_user(
        telegram_id: int, 
        first_name: Optional[str]=None, 
        last_name: Optional[str]=None,
        ):
        async with async_session_factory() as session:
            try:
                new_user = UsersOrm(
                    telegram_id=telegram_id, 
                    first_name=first_name, 
                    last_name=last_name,
                    )
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)
            except IntegrityError as e:
                logger.warning(f"IntegrityError: Пользователь с id {telegram_id} уже есть в базе.")

    @log_call
    @staticmethod
    async def add_server(
        country: str, 
        vpn_type: str, 
        traffic: str, 
        price_per_day: int
        ):
        async with async_session_factory() as session:
            new_server = ServersOrm(
                country=country, 
                vpn_type=vpn_type, 
                traffic=traffic, 
                price_per_day=price_per_day
                )
            session.add(new_server)
            await session.commit()
            await session.refresh(new_server)

    @log_call
    @staticmethod
    async def add_order(
        user_id: int, 
        invoice_id: int,
        price: float,
        duration_months: int,
        ):
        async with async_session_factory() as session:
            new_order = OrdersOrm(
                user_id=user_id,
                invoice_id=invoice_id,
                price=price,
                duration_months=duration_months,
                status="active",
            )
            session.add(new_order)
            await session.commit()
            await session.refresh(new_order)
            
    @log_call
    @staticmethod
    async def update_paid_status(
        invoice_id: int, 
        status_name: Optional[str]=None, 
        paid_at: Optional[bool]=False,
        expired_at: Optional[bool]=False,
        ):
        async with async_session_factory() as session:
            stmt = select(OrdersOrm).where(OrdersOrm.invoice_id == invoice_id)
            res = await session.execute(stmt)
            order = res.scalar_one_or_none()
            if order:
                if status_name:
                    order.status = status_name
                if paid_at:
                    duration_days = order.duration_months * 30
                    paid_time = datetime.utcnow()
                    order.paid_at = paid_time
                    if expired_at:
                        order.expires_at = paid_time + timedelta(days=duration_days)
                await session.commit()
            else:
                logger.warning(f"Ордер по invoice_id {invoice_id} не удалось найти и обновить.")
    
    @log_call
    @staticmethod
    async def get_user_by_tg_id(telegram_id: int) -> int | None:
        async with async_session_factory() as session:
            query = (
                select(UsersOrm.id)
                .filter(UsersOrm.telegram_id == telegram_id)
            )
            res = await session.execute(query)
            user_id = res.scalar_one_or_none()
            if user_id:
                return int(user_id)
            
    @log_call
    @staticmethod
    async def get_orders_by_tg_id(telegram_id: int):
        async with async_session_factory() as session:
            query = (
                select(UsersOrm)
                .options(selectinload(UsersOrm.paid_orders))
                .filter(UsersOrm.telegram_id == telegram_id)
            )
            res_raw = await session.execute(query)
            result = res_raw.unique().scalars().all()
            return result
            
    @log_call
    @staticmethod
    async def get_order_by_id(order_id: int):
        async with async_session_factory() as session:
            query = (
                select(OrdersOrm)
                .filter(OrdersOrm.id == order_id)
            )
            res_raw = await session.execute(query)
            result = res_raw.scalar_one_or_none()
            return result