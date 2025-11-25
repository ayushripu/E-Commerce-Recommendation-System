import pickle
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer


class DataProcessor:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.user_encoder = LabelEncoder()
        self.product_encoder = LabelEncoder()
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words="english")
        self.scaler = MinMaxScaler()

    def load_data(self):
        """Load and preprocess the data"""
        self.df = pd.read_csv(self.data_path)

        # Convert timestamp if it exists
        if "timestamp" in self.df.columns:
            self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])

        # Ensure rating column exists
        if "rating" not in self.df.columns:
            # Create synthetic ratings if they don't exist
            self.df["rating"] = np.random.randint(1, 6, len(self.df))

        print(f"Indian E-commerce Data loaded successfully!")
        print(f"Dataset Shape: {self.df.shape}")
        print(f"Total Users: {self.df['user_id'].nunique():,}")
        print(f"Total Products: {self.df['product_id'].nunique():,}")
        print(f"Total Transactions: {len(self.df):,}")
        print(f"Categories: {self.df['category'].unique().tolist()}")

        return self.df

    def preprocess_data(self):
        """Preprocess the data for recommendation systems"""
        if self.df is None:
            self.load_data()

        # Encode user and product IDs
        self.df["user_id_encoded"] = self.user_encoder.fit_transform(self.df["user_id"])
        self.df["product_id_encoded"] = self.product_encoder.fit_transform(
            self.df["product_id"]
        )

        print("Creating user-item matrix...")

        # Create user-item matrix with error handling
        try:
            self.user_item_matrix = self.df.pivot_table(
                index="user_id_encoded",
                columns="product_id_encoded",
                values="rating",
                fill_value=0,
            )
            print(f"User-item matrix created. Shape: {self.user_item_matrix.shape}")
        except Exception as e:
            print(f"Error creating pivot table: {e}")
            # Create a simple user-item matrix manually
            unique_users = self.df["user_id_encoded"].unique()
            unique_products = self.df["product_id_encoded"].unique()

            self.user_item_matrix = pd.DataFrame(
                0, index=unique_users, columns=unique_products
            )

            # Fill with actual ratings
            for _, row in self.df.iterrows():
                self.user_item_matrix.loc[
                    row["user_id_encoded"], row["product_id_encoded"]
                ] = row["rating"]

        return self.df, self.user_item_matrix

    def get_product_features(self):
        """Extract product features for content-based filtering"""
        product_features = self.df[
            [
                "product_id",
                "product_name",
                "category",
                "brand",
                "description",
                "price",
                "discount",
            ]
        ].drop_duplicates()

        # Create TF-IDF features from product description and category
        product_features["text_features"] = (
            product_features["product_name"].fillna("")
            + " "
            + product_features["category"].fillna("")
            + " "
            + product_features["brand"].fillna("")
            + " "
            + product_features["description"].fillna("")
        )

        tfidf_matrix = self.tfidf_vectorizer.fit_transform(
            product_features["text_features"]
        )

        print(f"Product features extracted. Shape: {tfidf_matrix.shape}")

        return product_features, tfidf_matrix

    def get_user_features(self):
        """Extract user features for collaborative filtering"""
        user_features = (
            self.df.groupby("user_id")
            .agg(
                {
                    "name": "first",
                    "age": "first",
                    "gender": "first",
                    "location": "first",
                    "state": "first",
                    "rating": ["mean", "count"],
                }
            )
            .reset_index()
        )

        user_features.columns = [
            "user_id",
            "name",
            "age",
            "gender",
            "location",
            "state",
            "avg_rating",
            "total_ratings",
        ]

        # Encode gender
        user_features["gender_encoded"] = user_features["gender"].map({"M": 0, "F": 1})

        # Scale numerical features
        numerical_features = ["age", "avg_rating", "total_ratings"]
        user_features[numerical_features] = self.scaler.fit_transform(
            user_features[numerical_features]
        )

        return user_features

    def get_indian_market_insights(self):
        """Get insights specific to Indian market"""
        insights = {}

        # Top categories by sales
        insights["top_categories"] = (
            self.df.groupby("category")
            .agg({"amount": "sum", "product_id": "count"})
            .rename(columns={"amount": "total_revenue", "product_id": "total_sales"})
            .nlargest(5, "total_revenue")
        )

        # Popular payment methods
        insights["payment_methods"] = self.df["payment_method"].value_counts()

        # State-wise sales
        insights["state_sales"] = self.df.groupby("state").size().nlargest(5)

        # Festival season impact
        if "is_festive_season" in self.df.columns:
            festive_sales = self.df.groupby("is_festive_season").agg(
                {"amount": "mean", "product_id": "count"}
            )
            insights["festive_impact"] = festive_sales

        return insights

    def save_encoders(self, path):
        """Save encoders and vectorizers for future use"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(
                {
                    "user_encoder": self.user_encoder,
                    "product_encoder": self.product_encoder,
                    "tfidf_vectorizer": self.tfidf_vectorizer,
                    "scaler": self.scaler,
                },
                f,
            )

    def load_encoders(self, path):
        """Load saved encoders and vectorizers"""
        with open(path, "rb") as f:
            encoders = pickle.load(f)
            self.user_encoder = encoders["user_encoder"]
            self.product_encoder = encoders["product_encoder"]
            self.tfidf_vectorizer = encoders["tfidf_vectorizer"]
            self.scaler = encoders["scaler"]

    def get_indian_market_insights(self):
        """Get market insights for dashboard"""
        insights = {}

        try:
            # Basic price statistics
            insights["avg_price"] = self.df["price"].mean()
            insights["min_price"] = self.df["price"].min()
            insights["max_price"] = self.df["price"].max()

            # Top category
            top_category = self.df["category"].value_counts().index[0]
            insights["top_category"] = top_category

            # User engagement
            products_per_user = self.df.groupby("user_id")["product_id"].nunique()
            insights["avg_products_per_user"] = products_per_user.mean()

            # Rating distribution
            insights["rating_distribution"] = (
                self.df["rating"].value_counts().sort_index().to_dict()
            )

            # Brand popularity
            insights["top_brands"] = self.df["brand"].value_counts().head(5).to_dict()

            # Location insights
            insights["top_locations"] = (
                self.df["location"].value_counts().head(5).to_dict()
            )

        except Exception as e:
            print(f"Error generating insights: {e}")
            # Return default insights
            insights = {
                "avg_price": 0,
                "top_category": "Unknown",
                "avg_products_per_user": 0,
            }

        return insights
