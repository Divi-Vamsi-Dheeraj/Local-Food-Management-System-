# queries.py
import pandas as pd
from sqlalchemy import func
from database import SessionLocal
from models import Provider, Receiver, FoodListing, Claim

def run_queries():
    session = SessionLocal()
    results = {}

    # 1️⃣ Providers per city
    q1 = session.query(Provider.City, func.count().label("Providers")).group_by(Provider.City).all()
    results["Providers per City"] = pd.DataFrame(q1, columns=["City", "Providers"])

    # 2️⃣ Receivers per city
    q2 = session.query(Receiver.City, func.count().label("Receivers")).group_by(Receiver.City).all()
    results["Receivers per City"] = pd.DataFrame(q2, columns=["City", "Receivers"])

    # 3️⃣ Provider Type with most food
    q3 = session.query(FoodListing.Provider_Type, func.sum(FoodListing.Quantity)).group_by(FoodListing.Provider_Type).all()
    results["Top Provider Type"] = pd.DataFrame(q3, columns=["Provider_Type", "Total_Quantity"])

    # 4️⃣ Receivers with most claims
    q4 = session.query(Receiver.Name, func.count(Claim.Claim_ID)).join(Claim).group_by(Receiver.Name).all()
    results["Top Receivers by Claims"] = pd.DataFrame(q4, columns=["Receiver_Name", "Claim_Count"])

    # 5️⃣ Total food quantity
    total_qty = session.query(func.sum(FoodListing.Quantity)).scalar()
    results["Total Food Quantity"] = pd.DataFrame({"Total_Quantity": [total_qty]})

    # 6️⃣ City with highest listings
    q6 = session.query(FoodListing.Location, func.count()).group_by(FoodListing.Location).all()
    results["Listings per City"] = pd.DataFrame(q6, columns=["City", "Listings"])

    # 7️⃣ Most common food types
    q7 = session.query(FoodListing.Food_Type, func.count()).group_by(FoodListing.Food_Type).all()
    results["Food Type Count"] = pd.DataFrame(q7, columns=["Food_Type", "Count"])

    # 8️⃣ Claims per food item
    q8 = session.query(FoodListing.Food_Name, func.count(Claim.Claim_ID)).join(Claim).group_by(FoodListing.Food_Name).all()
    results["Claims per Food Item"] = pd.DataFrame(q8, columns=["Food_Name", "Claim_Count"])

    # 9️⃣ Provider with highest successful claims
    q9 = (
        session.query(Provider.Name, func.count(Claim.Claim_ID))
        .join(FoodListing, FoodListing.Provider_ID == Provider.Provider_ID)
        .join(Claim, Claim.Food_ID == FoodListing.Food_ID)
        .filter(Claim.Status == "Completed")
        .group_by(Provider.Name)
        .all()
    )
    results["Top Providers (Completed Claims)"] = pd.DataFrame(q9, columns=["Provider_Name", "Completed_Claims"])

    # 🔟 Claim status breakdown
    q10 = session.query(Claim.Status, func.count()).group_by(Claim.Status).all()
    df10 = pd.DataFrame(q10, columns=["Status", "Count"])
    df10["Percentage"] = (df10["Count"] / df10["Count"].sum()) * 100
    results["Claim Status Breakdown"] = df10

    # 11️⃣ Avg food claimed per receiver
    q11 = (
        session.query(Receiver.Name, func.avg(FoodListing.Quantity))
        .join(Claim, Claim.Receiver_ID == Receiver.Receiver_ID)
        .join(FoodListing, Claim.Food_ID == FoodListing.Food_ID)
        .group_by(Receiver.Name)
        .all()
    )
    results["Average Food per Receiver"] = pd.DataFrame(q11, columns=["Receiver_Name", "Avg_Quantity"])

    # 12️⃣ Most claimed meal type
    q12 = session.query(FoodListing.Meal_Type, func.count(Claim.Claim_ID)).join(Claim).group_by(FoodListing.Meal_Type).all()
    results["Most Claimed Meal Type"] = pd.DataFrame(q12, columns=["Meal_Type", "Claim_Count"])

    # 13️⃣ Total food donated by provider
    q13 = session.query(Provider.Name, func.sum(FoodListing.Quantity)).join(FoodListing).group_by(Provider.Name).all()
    results["Total Food Donated per Provider"] = pd.DataFrame(q13, columns=["Provider_Name", "Total_Quantity"])

    session.close()
    return results
