from sqlalchemy import create_engine, Column, Integer, String        # core building blocks
from sqlalchemy.orm import declarative_base, sessionmaker             # ORM tools

engine = create_engine("sqlite:///chatbot.db")          # connects to (or creates) a file called chatbot.db

Base = declarative_base()                                 # base class all our table classes will inherit from

class ChatHistory(Base):                                   # this class = one database table
    __tablename__ = "chat_history"                          # the table's name

    id = Column(Integer, primary_key=True, autoincrement=True)   # unique row ID
    video_id = Column(String)
    video_title = Column(String)
    question = Column(String)
    answer = Column(String)

Base.metadata.create_all(engine)                            # actually creates the table in the .db file (if it doesn't exist yet)

SessionLocal = sessionmaker(bind=engine)                     # factory for creating database "sessions" (connections to talk to the DB)