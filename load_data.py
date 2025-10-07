# load_data.py
import pandas as pd
from sqlalchemy.exc import IntegrityError
from database import SessionLocal, engine
from models import Base, Provider, Receiver, FoodListing, Claim

def create_tables():
    """Create all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

def load_csv_data(filepath, parse_dates=None):
    """Load CSV safely with optional date parsing."""
    try:
        df = pd.read_csv(filepath, parse_dates=parse_dates)
        print(f"📥 Loaded {filepath} ({len(df)} rows)")
        return df
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return pd.DataFrame()

def insert_providers(session, df):
    for _, row in df.iterrows():
        provider = Provider(
            Provider_ID=int(row["Provider_ID"]),
            Name=row["Name"],
            Type=row["Type"],
            Address=row["Address"],
            City=row["City"],
            Contact=row["Contact"]
        )
        session.merge(provider)  # merge avoids duplicate insertions
    print(f"✅ Inserted {len(df)} providers")

def insert_receivers(session, df):
    for _, row in df.iterrows():
        receiver = Receiver(
            Receiver_ID=int(row["Receiver_ID"]),
            Name=row["Name"],
            Type=row["Type"],
            City=row["City"],
            Contact=row["Contact"]
        )
        session.merge(receiver)
    print(f"✅ Inserted {len(df)} receivers")

def insert_food_listings(session, df):
    for _, row in df.iterrows():
        food = FoodListing(
            Food_ID=int(row["Food_ID"]),
            Food_Name=row["Food_Name"],
            Quantity=int(row["Quantity"]),
            Expiry_Date=pd.to_datetime(row["Expiry_Date"]).date() if not pd.isna(row["Expiry_Date"]) else None,
            Provider_ID=int(row["Provider_ID"]),
            Provider_Type=row["Provider_Type"],
            Location=row["Location"],
            Food_Type=row["Food_Type"],
            Meal_Type=row["Meal_Type"]
        )
        session.merge(food)
    print(f"✅ Inserted {len(df)} food listings")

def insert_claims(session, df):
    for _, row in df.iterrows():
        claim = Claim(
            Claim_ID=int(row["Claim_ID"]),
            Food_ID=int(row["Food_ID"]),
            Receiver_ID=int(row["Receiver_ID"]),
            Status=row["Status"],
            Timestamp=pd.to_datetime(row["Timestamp"])
        )
        session.merge(claim)
    print(f"✅ Inserted {len(df)} claims")

def load_all_data():
    """Main loader function."""
    create_tables()
    session = SessionLocal()

    try:
        # Load CSVs
        providers_df = load_csv_data("providers_data.csv")
        receivers_df = load_csv_data("receivers_data.csv")
        food_df = load_csv_data("food_listings_data.csv", parse_dates=["Expiry_Date"])
        claims_df = load_csv_data("claims_data.csv", parse_dates=["Timestamp"])

        # Load into DB (order matters)
        if not providers_df.empty:
            insert_providers(session, providers_df)

        if not receivers_df.empty:
            insert_receivers(session, receivers_df)

        if not food_df.empty:
            insert_food_listings(session, food_df)

        if not claims_df.empty:
            insert_claims(session, claims_df)

        session.commit()
        print("🎉 All data loaded successfully into PostgreSQL!")

    except IntegrityError as e:
        session.rollback()
        print(f"⚠️ Integrity Error: {e}")
    except Exception as e:
        session.rollback()
        print(f"❌ Unexpected Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    load_all_data()
