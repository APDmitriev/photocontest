from fastapi import FastAPI, HTTPException, UploadFile, File, status
from sqlalchemy.future import select
from typing import List
from database import db_dependency
from auth import get_password_hash, verify_password
from schemas import UserResponse, UserCreate, PhotoResponse, ContestResponse, ContestCreate
from model import User, Photo, Contest
import os
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def authenticate_user(username: str, password: str, db: db_dependency):
    result = await db.execute(select(User).filter(User.username == username))
    db_user = result.scalars().first()
    if db_user and verify_password(password, db_user.password):
        return db_user
    return None


@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: db_dependency):
    result = await db.execute(select(User).filter(User.username == user.username))
    db_user = result.scalars().first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@app.post("/login")
async def login(username: str, password: str, db: db_dependency):
    user = await authenticate_user(username, password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return {"message": "Login successful", "user_id": user.id}

@app.post("/create-contest", response_model=ContestResponse)
async def create_contest(contest: ContestCreate, username: str, password: str, db: db_dependency):
    user = await authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    result = await db.execute(select(Contest).filter(Contest.name == contest.name))
    db_contest = result.scalars().first()
    if db_contest:
        raise HTTPException(status_code=400, detail="Contest already exists")

    new_contest = Contest(name=contest.name, description=contest.description)
    db.add(new_contest)
    await db.commit()
    await db.refresh(new_contest)
    return new_contest


@app.get("/contests", response_model=List[ContestResponse])
async def get_contests(db: db_dependency):
    result = await db.execute(select(Contest))
    contests = result.scalars().all()
    return contests


@app.post("/upload-photo", response_model=PhotoResponse)
async def upload_photo(
    username: str,
    password: str,
    db: db_dependency,
    file: UploadFile = File(...),
    name: str = "",
    description: str = "",
    contest_id: int = None
):
    user = await authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    contest = None
    if contest_id:
        result = await db.execute(select(Contest).filter(Contest.id == contest_id))
        contest = result.scalars().first()
        if not contest:
            raise HTTPException(status_code=404, detail="Contest not found")

    os.makedirs('photos', exist_ok=True)

    file_location = f"photos/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    new_photo = Photo(url=f"/{file_location}", name=name, description=description, owner_id=user.id, contest_id=contest.id if contest else None)

    db.add(new_photo)
    await db.commit()
    await db.refresh(new_photo)

    owner = UserResponse(id=user.id, username=user.username)

    return PhotoResponse(id=new_photo.id, url=new_photo.url, name=new_photo.name, description=new_photo.description, likes=new_photo.likes, dislikes=new_photo.dislikes, owner=owner, contest_id=new_photo.contest_id)

@app.post("/rate-photo/{photo_id}")
async def rate_photo(photo_id: int, like: bool, username: str, password: str, db: db_dependency):
    user = await authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    result = await db.execute(select(Photo).filter(Photo.id == photo_id))
    photo = result.scalars().first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    if like:
        photo.likes += 1
    else:
        photo.dislikes += 1

    await db.commit()
    await db.refresh(photo)

    return {"message": "Photo rated successfully", "likes": photo.likes, "dislikes": photo.dislikes}
