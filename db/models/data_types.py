from sqlalchemy.orm import mapped_column
from sqlalchemy import text, BigInteger

import datetime
from typing import Annotated


intpk = Annotated[int, mapped_column(primary_key=True)]
bigint = Annotated[int, mapped_column(BigInteger, nullable=False, unique=True)]
str_256 = Annotated[str, 256]

created_at = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE ('utc', now())"))
]
