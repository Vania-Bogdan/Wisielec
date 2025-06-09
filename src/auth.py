from sqlalchemy import Column, Integer, String
from database import Base, Session, engine
import hashlib


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)

    def __repr__(self):
        return f"<Player(username='{self.username}', wins={self.wins}, losses={self.losses})>"


# Функція для хешування
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Створення таблиці
def create_tables():
     # Base.metadata.drop_all(bind=engine)  # повністю видалити
     Base.metadata.create_all(bind=engine)  # створити з новими полями


# Реєстрація нового користувача
def register(username, password):
    session = Session()
    if not username or not password:
        return False, "Nie można zostawić pustych pól"
    if len(password) < 6:
        return False, "Hasło musi mieć min. 6 znaków"
    if session.query(Player).filter_by(username=username).first():
        session.close()
        return False, "Użytkownik już istnieje"
    user = Player(username=username, password_hash=hash_password(password))
    session.add(user)
    session.commit()
    session.close()
    return True, "Zarejestrowano poprawnie"


# Логін користувача
def login(username, password):
    if not username or not password:
        return False, "Nie można zostawić pustych pól"
    session = Session()
    user = session.query(Player).filter_by(username=username).first()
    if user and user.password_hash == hash_password(password):
        session.close()
        return True, "Zalogowano"
    session.close()
    return False, "Nieprawidłowe dane"
