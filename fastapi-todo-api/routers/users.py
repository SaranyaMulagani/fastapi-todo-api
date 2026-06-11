from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import auth

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.

    - **name**: Your full name
    - **email**: Must be unique
    - **password**: Minimum 6 characters
    """
    # Check if email already exists
    existing_user = db.query(models.User).filter(
        models.User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user with hashed password
    new_user = models.User(
        name=user_data.name,
        email=user_data.email,
        password=auth.hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/login",
    response_model=schemas.Token,
    summary="Login and get access token"
)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password to receive a JWT access token.

    Use this token in the Authorization header:
    `Bearer <your_token>`
    """
    # Find user by email
    user = db.query(models.User).filter(
        models.User.email == credentials.email
    ).first()

    # Check user exists and password is correct
    if not user or not auth.verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = auth.create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get(
    "/me",
    response_model=schemas.UserResponse,
    summary="Get my profile"
)
def get_my_profile(current_user: models.User = Depends(auth.get_current_user)):
    """
    Get the profile of the currently logged in user.
    Requires authentication.
    """
    return current_user


@router.delete(
    "/me",
    response_model=schemas.MessageResponse,
    summary="Delete my account"
)
def delete_my_account(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Permanently delete your account and all your todos.
    """
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted successfully"}
