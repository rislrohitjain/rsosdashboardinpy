import polars as pl
import os
import urllib.parse
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

_engine = None

def get_db_engine():
    global _engine
    if _engine is None:
        user = os.getenv("DB_USER")
        password = urllib.parse.quote_plus(os.getenv("DB_PASS", ""))
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT", "3306")
        db = os.getenv("DB_NAME")
        
        uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
        _engine = create_engine(uri, pool_pre_ping=True)
    return _engine

def get_student_data(limit=10000):
    engine = get_db_engine()
    # Using text() for SQLAlchemy compatibility
    query = text("CALL GetStudentDetailsFastForVisual(:limit, :offset)")
    
    try:
        with engine.connect() as conn:
            print(f"--- 🛰️  Connecting to {os.getenv('DB_HOST')} ---")
            result = conn.execute(query, {"limit": limit, "offset": 0})
            
            # Extract rows
            rows = [dict(row._mapping) for row in result]
            print(f"--- 📥 Rows found in DB: {len(rows)} ---")

            if not rows:
                return []

            # Process with Polars
            df = pl.DataFrame(rows)
            print(f"--- ⚡ Polars processing {df.height} records ---")

            # Auto-export for verification
            df.write_excel("debug_rsos_report.xlsx")
            
            return df.to_dicts()

    except Exception as e:
        print(f"--- ❌ SYSTEM ERROR: {str(e)} ---")
        return []
        
def get_student_data_excel(limit=10000):
    # Target the static folder explicitly
    file_name = "sample_for_dashboard.xlsx"
    file_path = os.path.join("static", file_name)
    
    print(f"--- 📍 Current Working Directory: {os.getcwd()} ---")
    
    
    print(f"--- 🛰️  Looking for local file at: {file_path} ---")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"--- ❌ SYSTEM ERROR: File not found at {file_path} ---")
        return []
        
    try:
        # 1. Force the 'calamine' engine which is highly compatible with diverse .xlsx styles
        # 2. Explicitly read the first sheet (read_excel reads sheet 1 by default, but this is safer)
        # df = pl.read_excel(file_path, engine="calamine")
        df = pl.read_excel(file_path, engine="openpyxl")
        
        print(f"--- 📥 Total rows loaded from Excel: {df.height} ---")

        if df.height == 0:
            print("--- ⚠️  WARNING: Excel file was read, but it contains 0 rows of data. ---")
            return []

        # Respect the limit parameter if data exceeds it
        if limit and df.height > limit:
            df = df.head(limit)
            print(f"--- ✂️  Sliced dataset to first {limit} rows ---")

        print(f"--- ⚡ Polars processing {df.height} records ---")
        
        return df.to_dicts()

    except Exception as e:
        # This will now print the EXACT error traceback/message instead of a generic failure
        import traceback
        print(f"--- ❌ SYSTEM ERROR: {str(e)} ---")
        traceback.print_exc()
        return []