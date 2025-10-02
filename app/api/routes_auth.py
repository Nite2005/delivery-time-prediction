# from fastapi import APIRouter
# from pydantic import BaseModel
# from app.core.security import create_token


# router = APIRouter()


# class AuthInput(BaseModel):
#     username: str
#     password: str

# @router.post('/login')
# def login(auth: AuthInput):
#     if (auth.username == "admin") and (auth.password== "admin"):
#         token = create_token({'sub':auth.username})
#         return {'access_token': token}
#     return {'error': 'Invalid Credentials'}

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from passlib.context import CryptContext
# from jose import jwt
# from datetime import datetime, timedelta
# from app.core.config import settings
# from app.db.session import get_db
# from app.db.models import User

# pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
# router = APIRouter()

# def verify_password(plain, hashed):
#     return pwd_context.verify(plain, hashed)

# def get_password_hash(password):
#     return pwd_context.hash(password)


# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

# @router.post("/register")
# def register(username: str, password: str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == username).first()
#     if user:
#         raise HTTPException(status_code=400, detail="User already exists")
#     hashed = get_password_hash(password)
#     user = User(username=username, password_hash=hashed)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return {"msg": "User created"}

# @router.post("/login")
# def login(username: str, password: str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == username).first()
#     if not user or not verify_password(password, user.password_hash):
#         raise HTTPException(status_code=400, detail="Invalid credentials")
#     token = create_access_token({"sub": user.username})
#     return {"access_token": token, "token_type": "bearer"}


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from app.core.config import settings
from app.db.session import get_db
from app.db.models import User

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# -------- Password utils --------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# -------- JWT utils --------
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM
        )
        return payload
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = verify_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user  # ✅ SQLAlchemy User object

# -------- Routes --------
@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = get_password_hash(password)
    user = User(username=username, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "User created"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
