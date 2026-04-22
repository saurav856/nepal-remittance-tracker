import pandas as pd
from database import engine, Base, SessionLocal
from models import RemittanceFlow
import os

def seed():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    existing = db.query(RemittanceFlow).first()
    if existing:
        print("Database already seeded. Skipping.")
        db.close()
        return

    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "remittance_nrb.csv")
    df = pd.read_csv(csv_path)

    print(f"Loading {len(df)} records into database...")

    for _, row in df.iterrows():
        record = RemittanceFlow(
            fiscal_year=row["fiscal_year"],
            year_ad=int(row["year_ad"]),
            source_country=row["source_country"],
            amount_usd=float(row["amount_usd"]),
            num_workers=int(row["num_workers"]) if pd.notna(row["num_workers"]) else None
        )
        db.add(record)

    db.commit()
    db.close()
    print("Seeding complete.")

if __name__ == "__main__":
    seed()