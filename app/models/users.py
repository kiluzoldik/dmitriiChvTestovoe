from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    user_referal_code: Mapped[str] = mapped_column(default=None, nullable=True)
    other_referal_code: Mapped[str] = mapped_column(default=None, nullable=True)
