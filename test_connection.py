from sqlalchemy import create_engine

# Replace with your actual connection URL
DATABASE_URL = 'sqlite:///./travel_planner.db'

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
