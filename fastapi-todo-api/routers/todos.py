from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
import schemas
import auth

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)


@router.get(
    "/",
    response_model=List[schemas.TodoResponse],
    summary="Get all my todos"
)
def get_all_todos(
    completed: Optional[bool] = Query(None, description="Filter by completed status"),
    priority: Optional[str] = Query(None, description="Filter by priority: low, medium, high"),
    skip: int = Query(0, description="Number of todos to skip"),
    limit: int = Query(10, description="Max todos to return"),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all todos for the logged in user.

    Optional filters:
    - **completed**: true or false
    - **priority**: low, medium, high
    - **skip** and **limit** for pagination
    """
    query = db.query(models.Todo).filter(
        models.Todo.owner_id == current_user.id
    )

    # Apply filters if provided
    if completed is not None:
        query = query.filter(models.Todo.completed == completed)

    if priority:
        query = query.filter(models.Todo.priority == priority)

    todos = query.offset(skip).limit(limit).all()
    return todos


@router.post(
    "/",
    response_model=schemas.TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new todo"
)
def create_todo(
    todo_data: schemas.TodoCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new todo item.

    - **title**: Required
    - **description**: Optional
    - **priority**: low, medium, high (default: medium)
    """
    new_todo = models.Todo(
        **todo_data.model_dump(),
        owner_id=current_user.id
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo


@router.get(
    "/{todo_id}",
    response_model=schemas.TodoResponse,
    summary="Get a single todo"
)
def get_todo(
    todo_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific todo by ID. Only the owner can access it."""
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.owner_id == current_user.id
    ).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

    return todo


@router.put(
    "/{todo_id}",
    response_model=schemas.TodoResponse,
    summary="Update a todo"
)
def update_todo(
    todo_id: int,
    todo_data: schemas.TodoUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a todo. Only provided fields will be updated.

    You can update:
    - **title**
    - **description**
    - **completed** (true/false)
    - **priority** (low/medium/high)
    """
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.owner_id == current_user.id
    ).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

    # Only update fields that were actually provided
    update_data = todo_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)

    db.commit()
    db.refresh(todo)

    return todo


@router.patch(
    "/{todo_id}/complete",
    response_model=schemas.TodoResponse,
    summary="Mark todo as complete"
)
def mark_complete(
    todo_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Quickly mark a todo as completed."""
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.owner_id == current_user.id
    ).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

    todo.completed = True
    db.commit()
    db.refresh(todo)

    return todo


@router.delete(
    "/{todo_id}",
    response_model=schemas.MessageResponse,
    summary="Delete a todo"
)
def delete_todo(
    todo_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Permanently delete a todo."""
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.owner_id == current_user.id
    ).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

    db.delete(todo)
    db.commit()

    return {"message": f"Todo '{todo.title}' deleted successfully"}


@router.delete(
    "/",
    response_model=schemas.MessageResponse,
    summary="Delete all my todos"
)
def delete_all_todos(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Delete all todos for the logged in user."""
    deleted = db.query(models.Todo).filter(
        models.Todo.owner_id == current_user.id
    ).delete()

    db.commit()

    return {"message": f"Deleted {deleted} todos successfully"}
