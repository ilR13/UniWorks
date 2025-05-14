from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Создаём базовый класс
Base = declarative_base()

# 2. Описываем таблицу как Python-класс
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String)
    registered_at = Column(DateTime, server_default=func.now())

# 3. Создаём движок SQLite (файл создастся в корне)
engine = create_engine('sqlite:///db.db')

async def create_user(tg_id,first_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_user = User(tg_id=tg_id, first_name=first_name)
    session.add(new_user)
    session.commit()

#
# # 4. Создаём таблицы в БД
# Base.metadata.create_all(engine)
#
# print("База данных и таблица созданы!")
