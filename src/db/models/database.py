from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase

from db.models.data_types import str_256


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}
