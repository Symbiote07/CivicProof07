from sqlalchemy.orm import Session
from models import engine, Booth, Voter, Task, SessionLocal, Base

# 1. Reset the Database (Clear everything to avoid duplicates)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed_data():
    print("🌱 Seeding Data...")

    # 2. Create Booths
    booth1 = Booth(name="Sector 14, Gali 3", location_lat="26.8467", location_long="80.9462")
    booth2 = Booth(name="Hazratganj Main Market", location_lat="26.8500", location_long="80.9400")
    
    db.add(booth1)
    db.add(booth2)
    db.commit() # Save to get IDs
    
    print(f"✅ Created Booth 1: {booth1.name} (ID: {booth1.id})")

    # 3. Create Voters (Linked explicitly to Booth 1)
    voters = [
        Voter(name="Aryan", phone="9999999999", segment="Youth", booth_id=booth1.id),
        Voter(name="Priya", phone="7777777777", segment="Women", booth_id=booth1.id),
        Voter(name="Rahul", phone="8888888888", segment="Trader", booth_id=booth2.id), # Different booth
    ]
    
    db.add_all(voters)
    db.commit()
    print(f"✅ Registered {len(voters)} Voters.")

    # 4. Create Tasks (Linked explicitly to Booth 1)
    task1 = Task(title="Fix Streetlight Pole #4", status="Pending", booth_id=booth1.id)
    task2 = Task(title="Repair Pothole near Shop 10", status="Pending", booth_id=booth2.id)

    db.add(task1)
    db.add(task2)
    db.commit()
    
    print(f"✅ Created Task 1: {task1.title} -> Linked to Booth {task1.booth_id}")
    print("🚀 Database is ready! Task 1 and Aryan are both in Booth 1.")

if __name__ == "__main__":
    seed_data()