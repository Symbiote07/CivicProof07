from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

# Import our modules
# CHECK THIS LINE: Did you add 'Voter'?
# CHECK THIS LINE: Did you add 'Voter'?
from models import Base, engine, SessionLocal, Task, Booth, Voter
from ai_engine import analyze_streetlight
# 1. Initialize the App
app = FastAPI(title="CivicProof API", description="AI-Powered Micro-Accountability Engine")

# Allow mobile apps to talk to this server (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 2. The "Hello World" Endpoint
@app.get("/")
def read_root():
    return {"message": "CivicProof API is Online 🟢"}

# 3. Get All Tasks (So the App can show a list)
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# 4. The CORE Feature: Upload Proof & Verify
@app.post("/verify-task/{task_id}")
async def verify_task(task_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # A. Find the task in the database
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # B. Save the uploaded file locally
    file_location = f"images/{file.filename}"
    os.makedirs("images", exist_ok=True) # Create folder if not exists
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # C. Run the AI Engine on this file!
    ai_result = analyze_streetlight(file_location)
    
    # D. Update Database based on AI Result
    if ai_result["success"]:
        task.status = "Verified ✅"
        task.image_url = file_location
        # In a real app, here is where we would trigger the SMS notification to voters!
    else:
        task.status = "Rejected ❌"
    
    db.commit()
    
    return {
        "task_id": task_id,
        "ai_verdict": ai_result,
        "new_status": task.status
    }