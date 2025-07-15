from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, func, select
from sqlalchemy.orm import declarative_base, sessionmaker
import asyncio
# 1. Создаём базовый класс
Base = declarative_base()

# 2. Описываем таблицу как Python-класс
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    accepted_terms = Column(Boolean, default=False)
    registered_at = Column(DateTime, server_default=func.now())

# 3. Создаём движок SQLite (файл создастся в корне)
engine = create_engine('sqlite:///db.db',
                       #echo=True # вывод в консоль всех обращений к бд с помощью алхимии
                       )

async def create_user(tg_id,first_name,last_name):
    with engine.connect() as conn:
        query = select(User).where(User.tg_id==tg_id)
        if len(conn.execute(query).all()) == 0:
            Session = sessionmaker(bind=engine)
            session = Session()
            new_user = User(tg_id=tg_id, first_name=first_name, last_name=last_name)
            session.add(new_user)
            session.commit()
        #     return "Регистрация пройдена"
        # else:
        #     return "Вы уже зарегистрированы"

async def accept_terms(tg_id):
    with engine.connect() as conn:
        query = select(User).where((User.tg_id==tg_id) & (User.accepted_terms==True))
        if len(conn.execute(query).all()) != 0:
            return True
        else:
            return False

async def accepted_terms(tg_id):
    with engine.connect() as conn:
        query = select(User).where(User.tg_id==tg_id)
        res = conn.execute(query).first()
        if len(res) != 0:
            Session = sessionmaker(bind=engine)
            session = Session()
            user = session.query(User).get(res[0])
            user.accepted_terms = True
            session.commit()

# # 4. Создаём таблицы в БД
# Base.metadata.create_all(engine)
#
# print("База данных и таблица созданы!")
