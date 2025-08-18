from typing import Annotated
from datetime import datetime

from sqlalchemy import String, BigInteger, text, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

intpk = Annotated[int, mapped_column(primary_key=True)]
bigint = Annotated[int, mapped_column(BigInteger, nullable=False, unique=True)]
str_256 = Annotated[str, 256]
created_at = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE ('utc', now())"))
]


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    telegram_id: Mapped[bigint]
    username: Mapped[str_256] = mapped_column(nullable=True)
    first_name: Mapped[str_256] = mapped_column(nullable=True)
    last_name: Mapped[str_256] = mapped_column(nullable=True)
    created_at: Mapped[created_at]

    orders: Mapped[list["OrdersOrm"]] = relationship(back_populates="user")
    servers: Mapped[list["ServersOrm"]] = relationship(back_populates="user")

    paid_orders: Mapped[list["OrdersOrm"]] = relationship(
        back_populates="user",
        lazy="selectin",
        primaryjoin="and_(UsersOrm.id == OrdersOrm.user_id, OrdersOrm.status == 'paid')",
        viewonly=True,
    )


class ServersOrm(Base):
    __tablename__ = "servers"
    id: Mapped[intpk]
    country: Mapped[str_256]
    vpn_type: Mapped[str_256]
    traffic: Mapped[str_256]
    price_per_day: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    user: Mapped["UsersOrm"] = relationship(back_populates="servers")


class OrdersOrm(Base):
    __tablename__ = "orders"

    id: Mapped[intpk]
    invoice_id: Mapped[bigint] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    price: Mapped[int]
    duration_months: Mapped[int]
    status: Mapped[str_256]
    paid_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped["UsersOrm"] = relationship(back_populates="orders")
