import pandas as pd
from faker import Faker
import random


def generate_sample_data(num_users=1000, num_products=200, num_transactions=5000):
    # Initialize Faker with Indian locale
    fake = Faker("en_IN")

    # Generate users with Indian names and locations
    users = []
    for i in range(num_users):
        users.append(
            {
                "user_id": i + 1,
                "name": fake.name(),
                "age": random.randint(18, 65),
                "gender": random.choice(["M", "F"]),
                "location": fake.city(),
                "state": fake.state(),
                "email": fake.email(),
                "phone_number": fake.phone_number(),
            }
        )

    # Generate products with Indian context
    categories = [
        "Electronics",
        "Clothing",
        "Books",
        "Home & Kitchen",
        "Sports",
        "Beauty",
        "Groceries",
        "Furniture",
        "Mobile Phones",
        "Fashion Accessories",
    ]

    # Indian brands by category
    indian_brands = {
        "Electronics": [
            "Samsung",
            "Micromax",
            "Lava",
            "Intex",
            "iBall",
            "Onida",
            "Videocon",
            "BPL",
        ],
        "Clothing": [
            "FabIndia",
            "Biba",
            "Manyavar",
            "W",
            "Allen Solly",
            "Peter England",
            "Raymond",
            "Levis",
        ],
        "Books": [
            "Arihant",
            "S. Chand",
            "NCERT",
            "MBD",
            "Oswaal",
            "Upkar",
            "GK Publications",
        ],
        "Home & Kitchen": [
            "Prestige",
            "Bajaj",
            "Havells",
            "Usha",
            "Philips",
            "Butterfly",
            "Morphy Richards",
        ],
        "Sports": [
            "Nike",
            "Adidas",
            "Puma",
            "Reebok",
            "Decathlon",
            "Slazenger",
            "Yonex",
        ],
        "Beauty": [
            "Lakme",
            "Maybelline",
            "L'Oreal",
            "Hindustan Unilever",
            "Nivea",
            "Ponds",
            "Garnier",
        ],
        "Groceries": [
            "Amul",
            "Britannia",
            "Parle",
            "Dabur",
            "Nestle",
            "Cadbury",
            "Haldiram",
            "MTR",
        ],
        "Furniture": [
            "Godrej",
            "Nilkamal",
            "Durian",
            "Pepperfry",
            "Urban Ladder",
            "HomeTown",
            "Ikea",
        ],
        "Mobile Phones": [
            "Samsung",
            "Xiaomi",
            "Realme",
            "Oppo",
            "Vivo",
            "OnePlus",
            "Motorola",
        ],
        "Fashion Accessories": [
            "Tanishq",
            "PC Jeweller",
            "Fastrack",
            "Titan",
            "Sonata",
            "Maxima",
        ],
    }

    # Indian product names by category
    indian_product_names = {
        "Electronics": [
            "Smart TV",
            "Washing Machine",
            "Refrigerator",
            "Air Conditioner",
            "Laptop",
            "Tablet",
            "Smartphone",
            "Headphones",
        ],
        "Clothing": [
            "Kurta",
            "Saree",
            "Sherwani",
            "Jeans",
            "Shirt",
            "Dress",
            "T-shirt",
            "Traditional Wear",
        ],
        "Books": [
            "Competitive Exam Guide",
            "Academic Textbook",
            "Novel",
            "Cookbook",
            "Children's Book",
            "Self-help Book",
        ],
        "Home & Kitchen": [
            "Mixer Grinder",
            "Pressure Cooker",
            "Cookware Set",
            "Dinner Set",
            "Water Purifier",
            "Iron",
        ],
        "Sports": [
            "Cricket Bat",
            "Football",
            "Badminton Racket",
            "Sports Shoes",
            "Yoga Mat",
            "Fitness Equipment",
        ],
        "Beauty": [
            "Face Cream",
            "Lipstick",
            "Kajal",
            "Shampoo",
            "Perfume",
            "Makeup Kit",
            "Skin Care",
        ],
        "Groceries": [
            "Biscuits",
            "Chocolates",
            "Snacks",
            "Spices",
            "Tea",
            "Coffee",
            "Ready-to-eat",
        ],
        "Furniture": [
            "Sofa Set",
            "Dining Table",
            "Wardrobe",
            "Bed",
            "Office Chair",
            "Bookshelf",
        ],
        "Mobile Phones": [
            "Smartphone",
            "Feature Phone",
            "Tablet",
            "Smart Watch",
            "Earphones",
        ],
        "Fashion Accessories": [
            "Necklace",
            "Earrings",
            "Watch",
            "Bracelet",
            "Sunglasses",
            "Handbag",
        ],
    }

    products = []
    for i in range(num_products):
        category = random.choice(categories)
        brand = random.choice(indian_brands.get(category, ["Generic"]))
        product_name_base = random.choice(
            indian_product_names.get(category, ["Product"])
        )

        products.append(
            {
                "product_id": i + 1,
                "product_name": f"{brand} {product_name_base} {i + 1}",
                "category": category,
                "price": round(random.uniform(199, 99999), 2),
                "brand": brand,
                "rating": round(random.uniform(3.0, 5.0), 1),
                "description": fake.text(max_nb_chars=100),
                "discount": random.randint(0, 70),
                "in_stock": random.choice([True, True, True, False]),
            }
        )

    # Generate transactions with Indian context
    transactions = []
    for i in range(num_transactions):
        user_id = random.randint(1, num_users)
        product_id = random.randint(1, num_products)

        # Add rating to transactions (Indians tend to rate higher)
        rating = random.choices([3, 4, 5, 2, 1], weights=[3, 4, 2, 1, 1])[0]

        transactions.append(
            {
                "transaction_id": i + 1,
                "user_id": user_id,
                "product_id": product_id,
                "rating": rating,
                "timestamp": fake.date_time_between(start_date="-1y", end_date="now"),
                "purchase_count": random.randint(1, 3),
                "amount": round(
                    random.uniform(199, 19999), 2
                ),  # Transaction amount in INR
                "payment_method": random.choice(
                    [
                        "Credit Card",
                        "Debit Card",
                        "UPI",
                        "Net Banking",
                        "Cash on Delivery",
                    ]
                ),
                "delivery_status": random.choice(
                    ["Delivered", "Shipped", "Processing", "Cancelled"]
                ),
            }
        )

    # Create DataFrames
    transactions_df = pd.DataFrame(transactions)
    products_df = pd.DataFrame(products)
    users_df = pd.DataFrame(users)

    # Merge data
    df = transactions_df.merge(products_df, on="product_id")
    df = df.merge(users_df, on="user_id")

    # Add some Indian festival season spikes
    festival_months = [
        1,
        4,
        8,
        10,
        11,
    ]  # Jan, Apr, Aug, Oct, Nov - major Indian festivals
    df["is_festive_season"] = df["timestamp"].dt.month.isin(festival_months)

    return df


def display_sample_data(df):
    """Display sample data for verification"""
    print("\n" + "=" * 50)
    print("SAMPLE DATA PREVIEW")
    print("=" * 50)

    print(f"\nTotal Records: {len(df):,}")
    print(f"Columns: {df.columns.tolist()}")

    print("\nFirst 3 Users:")
    users_sample = (
        df[["user_id", "name", "age", "gender", "location", "state"]]
        .drop_duplicates()
        .head(3)
    )
    print(users_sample.to_string(index=False))

    print("\nFirst 5 Products:")
    products_sample = (
        df[["product_id", "product_name", "category", "brand", "price"]]
        .drop_duplicates()
        .head(5)
    )
    print(products_sample.to_string(index=False))

    print("\nFirst 5 Transactions:")
    transactions_sample = df[
        [
            "transaction_id",
            "user_id",
            "product_id",
            "rating",
            "amount",
            "payment_method",
        ]
    ].head(5)
    print(transactions_sample.to_string(index=False))

    print("\nData Summary:")
    print(f"Unique Users: {df['user_id'].nunique():,}")
    print(f"Unique Products: {df['product_id'].nunique():,}")
    print(f"Unique Categories: {df['category'].nunique()}")
    print(f"Date Range: {df['timestamp'].min()} to {df['timestamp'].max()}")

    print("\nPrice Range (INR):")
    print(f"Min: ₹{df['price'].min():.2f}")
    print(f"Max: ₹{df['price'].max():.2f}")
    print(f"Avg: ₹{df['price'].mean():.2f}")

    print("\nRating Distribution:")
    print(df["rating"].value_counts().sort_index())

    print("\nMissing Values:")
    print(df.isnull().sum())


if __name__ == "__main__":
    print("Generating Indian E-commerce Sample Data...")
    df = generate_sample_data()

    # Save to CSV
    df.to_csv("data/ecommerce_data.csv", index=False)

    # Display sample data
    display_sample_data(df)

    print(f"\nData successfully saved to 'data/ecommerce_data.csv'")
