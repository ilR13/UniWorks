import uuid

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, func, select, BigInteger, ForeignKey, \
    Float
from sqlalchemy.orm import declarative_base, sessionmaker
import asyncio
# 1. Создаём базовый класс
Base = declarative_base()

# 2. Описываем таблицу как Python-класс
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    accepted_terms = Column(Boolean, default=False)
    registered_at = Column(DateTime, server_default=func.now())

class Works(Base):
    __tablename__ = "works"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    faculty = Column(String)
    speciality = Column(String)
    discipline = Column(String)
    title_work = Column(String)
    task = Column(String)
    mark = Column(String)
    listing_price_uah = Column(Float)
    price_with_fee_uah = Column(Float)
    uuid_watermark = Column(String, default=None)
    ssdeep_hash = Column(String, default=None)
    created_at = Column(DateTime, server_default=func.now())
    status = Column(String)
    file1 = Column(String)
    file2 = Column(String)
    file3 = Column(String)
    file4 = Column(String)
    file5 = Column(String)
    file6 = Column(String)
    file7 = Column(String)
    file8 = Column(String)
    file9 = Column(String)
    file10 = Column(String)


# 3. Создаём движок SQLite (файл создастся в корне)
engine = create_engine('sqlite:///db.db',
                       #echo=True # вывод в консоль всех обращений к бд с помощью алхимии
                       )

async def create_user(tg_id,first_name,last_name):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = select(User).where(User.tg_id==tg_id)
        if len(session.execute(query).all()) == 0:

            new_user = User(tg_id=tg_id, first_name=first_name, last_name=last_name)
            session.add(new_user)
            session.commit()
        #     return "Регистрация пройдена"
        # else:
        #     return "Вы уже зарегистрированы"

async def accept_terms(tg_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = select(User).where((User.tg_id==tg_id) & (User.accepted_terms==True))
        if len(session.execute(query).all()) != 0:
            return True
        else:
            return False

async def accepted_terms(tg_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = select(User).where(User.tg_id==tg_id)
        res = session.execute(query).first()
        if len(res) != 0:

            # user = session.query(User).get(res[0])
            user = session.query(User).filter_by(tg_id=tg_id).first()
            user.accepted_terms = True
            session.commit()

def create_empty_work(user_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:

        new_work = Works(owner_id=user_id)
        session.add(new_work)
        session.commit()

# переписать коннект к бд для автозакрытия сессии
def create_work(user_id, faculty, speciality, discipline, title_work,
                task, mark, listing_price_uah, price_with_fee,
                file1 = None, file2 = None, file3 = None, file4 = None, file5 = None, file6 = None,file7 = None,file8 = None,file9 = None,file10 = None,):

    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = select(Works).where(Works.owner_id==user_id)
        res = session.execute(query).first()


        if len(res) != 0:
            work = session.query(Works).filter_by(owner_id=user_id).all()[-1]
            work.task = task
            work.mark = mark
            work.faculty = faculty
            work.speciality = speciality
            work.discipline = discipline
            work.title_work = title_work
            work.task = task
            work.listing_price_uah = listing_price_uah
            work.price_with_fee_uah = price_with_fee
            work.file1 = file1
            # work.file2 = file2
            # work.file3 = file3
            # work.file4 = file4
            # work.file5 = file5
            # work.file6 = file6
            # work.file7 = file7
            # work.file8 = file8
            # work.file9 = file9
            # work.file10 = file10


            session.commit()

def get_work_id(user_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        work = session.query(Works).filter_by(owner_id=user_id).all()[-1]
        return work.id

# # 4. Создаём таблицы в БД
# Base.metadata.create_all(engine)
#
# print("База данных и таблица созданы!")
