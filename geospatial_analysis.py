
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

# Step 1: Create sample location-based sales data

data = {
    "City": [
        "Chennai", "Coimbatore", "Bangalore",
        "Hyderabad", "Mumbai", "Pune",
        "Kochi", "Madurai", "Vijayawada", "Mysore"
    ],
    "Latitude": [
        13.0827, 11.0168, 12.9716,
        17.3850, 19.0760, 18.5204,
        9.9312, 9.9252, 16.5062, 12.2958
    ],
    "Longitude": [
        80.2707, 76.9558, 77.5946,
        78.4867, 72.8777, 73.8567,
        76.2673, 78.1198, 80.6480, 76.6394
    ],
    "Sales": [
        85000, 65000, 95000, 90000, 98000,
        70000, 45000, 30000, 25000, 40000
    ],
    "Customer_Demand": [
        900, 750, 950, 850, 980,
        800, 700, 850, 900, 650
    ],
    "Existing_Stores": [
        8, 5, 10, 9, 12, 4, 2, 1, 1, 2
    ]
}

df = pd.DataFrame(data)

# Step 2: Save raw dataset
df.to_csv("sales_location_data.csv", index=False)

print("Original Geospatial Dataset:")
print(df)

# Step 3: Check missing values and duplicates
print("\nMissing Values:")
print(df.isnull().sum())

df = df.drop_duplicates()

# Step 4: Calculate demand per existing store
df["Demand_Per_Store"] = (
    df["Customer_Demand"] / df["Existing_Stores"]
)

# Step 5: Identify expansion opportunities
# High demand and fewer existing stores

df["Expansion_Opportunity"] = np.where(
    (df["Customer_Demand"] >= 800) &
    (df["Existing_Stores"] <= 2),
    "High Opportunity",
    "Normal"
)

print("\nExpansion Opportunities:")
print(df[[
    "City", "Customer_Demand",
    "Existing_Stores", "Expansion_Opportunity"
]])

# Step 6: Sort locations by demand per store
df = df.sort_values(
    by="Demand_Per_Store",
    ascending=False
)

# Step 7: Create geographical map
m = folium.Map(
    location=[15.0, 78.0],
    zoom_start=5
)

for _, row in df.iterrows():

    if row["Expansion_Opportunity"] == "High Opportunity":
        color = "red"
    else:
        color = "blue"

    popup_text = (
        f"City: {row['City']}<br>"
        f"Sales: Rs. {row['Sales']}<br>"
        f"Customer Demand: {row['Customer_Demand']}<br>"
        f"Existing Stores: {row['Existing_Stores']}<br>"
        f"Opportunity: {row['Expansion_Opportunity']}"
    )

    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=8,
        popup=popup_text,
        color=color,
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

# Save geographical map
m.save("sales_geographical_map.html")

# Step 8: Visualize sales by city
plt.figure(figsize=(10, 5))

plt.bar(df["City"], df["Sales"])

plt.title("Sales Analysis by City")
plt.xlabel("City")
plt.ylabel("Sales Amount")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("sales_by_city.png")
plt.show()

# Step 9: Visualize customer demand
plt.figure(figsize=(10, 5))

plt.bar(df["City"], df["Customer_Demand"])

plt.title("Customer Demand by City")
plt.xlabel("City")
plt.ylabel("Customer Demand")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("customer_demand.png")
plt.show()

# Step 10: Save cleaned analysis
df.to_csv("geospatial_analysis_results.csv", index=False)

print("\nBest Locations for Business Expansion:")

print(
    df[df["Expansion_Opportunity"] == "High Opportunity"]
    [["City", "Customer_Demand", "Existing_Stores"]]
)

print("\nGeospatial Data Analysis Completed Successfully!")
