from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os

from models import Task, get_db
from openai_service import extract_task_info
from scheduler import start_scheduler

app = FastAPI(title="Simple Todo API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Task schemas
class TaskBase(BaseModel):
    content: str
    due_time: datetime

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    completed: bool
    
    class Config:
        orm_mode = True

class TaskInput(BaseModel):
    user_input: str

# Start the scheduler when the app starts
@app.on_event("startup")
def startup_event():
    start_scheduler()

# API endpoints
@app.post("/tasks/", response_model=TaskResponse)
async def create_task(task_input: TaskInput, db: Session = Depends(get_db)):
    # Extract task info from user input
    task_info = await extract_task_info(task_input.user_input)
    
    if not task_info:
        raise HTTPException(status_code=400, detail="Could not extract task information")
    
    # Create new task
    db_task = Task(
        content=task_info["content"],
        due_time=task_info["due_time"]
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task

@app.get("/tasks/", response_model=List[TaskResponse])
def get_tasks(completed: Optional[bool] = None, db: Session = Depends(get_db)):
    query = db.query(Task)
    
    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    return query.order_by(Task.due_time).all()

@app.put("/tasks/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = True
    db.commit()
    
    return {"message": "Task marked as completed"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    
    return {"message": "Task deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)