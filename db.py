import uuid
import ssdeep
import imagehash

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
    price_with_free_uah = Column(Float)
    uuid_watermark = Column(String, default=None)
    # ssdeep_hash = Column(String, default=None)
    created_at = Column(DateTime, server_default=func.now())
    status = Column(String)
    # file1 = Column(String)
    # file1_hash = Column(String)
    # file2 = Column(String)
    # file2_hash = Column(String)
    # file3 = Column(String)
    # file3_hash = Column(String)
    # file4 = Column(String)
    # file4_hash = Column(String)
    # file5 = Column(String)
    # file5_hash = Column(String)
    # file6 = Column(String)
    # file6_hash = Column(String)
    # file7 = Column(String)
    # file7_hash = Column(String)
    # file8 = Column(String)
    # file8_hash = Column(String)
    # file9 = Column(String)
    # file9_hash = Column(String)
    # file10 = Column(String)
    # file10_hash = Column(String)

class Files(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    work_id = Column(Integer, ForeignKey("works.id"))
    created_at = Column(DateTime, server_default=func.now())
    file_type = Column(String)
    status = Column(String)
    file = Column(String)
    file_hash = Column(String)
    

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


def create_work(user_id, faculty, speciality, discipline, title_work,
                task, mark, listing_price_uah, price_with_fee ):

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
            work.price_with_free_uah = price_with_fee
            # work.file1 = file1
            # work.uuid_watermark = file1_hash

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
    

def check_hash_file(hash1):
    Session = sessionmaker(bind=engine)
    res = True
    with Session() as session:
        file = session.query(Files.file_hash).filter_by(file_type="document")
        
        for hash2 in file:
            if hash2[0] != None:
                if ssdeep.compare(hash1, hash2[0]) < 10:
                    res = True
                else:
                    return False
    return res


def check_image_hash(hash1):
    hash1 = imagehash.hex_to_hash(hash1)
    Session = sessionmaker(bind = engine)
    res = True
    with Session() as session:
        file = session.query(Files.file_hash).filter_by(file_type="image")
        
        for hash2 in file:

            if hash2[0] != None:
    
               
                if hash1 - imagehash.hex_to_hash(hash2[0]) > 5:
                    res = True
                else:
                    return False
    return res
    

def delete_work(user_id):
    work_id = get_work_id(user_id)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        work = session.query(Works).filter_by(owner_id=user_id).all()[-1]
        session.delete(work)
        files =  session.query(Files).filter_by(work_id=work_id).all()
        for file in files:
            session.delete(file)
        #print(files)
        session.commit()

def test():
    return(Works)



def add_file(user_id, file, file_type, hash):
    work_id = get_work_id(user_id)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        new_file = Files( work_id= work_id, file= file, file_type= file_type, file_hash = hash)
        session.add(new_file)
        
        session.commit()

# def add_ssdeep_hash(user_id, num_file, hash):
#     Session = sessionmaker(bind=engine)
#     with Session() as session:
#         work = session.query(Works).filter_by(owner_id=user_id).all()[-1]
#         work.num_file = hash

# # 4. Создаём таблицы в БД
# Base.metadata.create_all(engine)

# print("База данных и таблица созданы!")
