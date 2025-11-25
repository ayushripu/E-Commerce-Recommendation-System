import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import pickle
import os


class RecommendationEngine:
    def __init__(self, data_processor):
        self.dp = data_processor
        self.user_item_matrix = None
        self.product_features = None
        self.tfidf_matrix = None
        self.user_features = None

    def build_models(self):
        """Build all recommendation models"""
        print("Building recommendation models...")

        # Preprocess data
        self.dp.preprocess_data()

        # Get matrices
        self.user_item_matrix = self.dp.user_item_matrix
        self.product_features, self.tfidf_matrix = self.dp.get_product_features()
        self.user_features = self.dp.get_user_features()

        print("Building collaborative filtering model...")
        # Build collaborative filtering model
        try:
            self.collab_similarity = cosine_similarity(self.user_item_matrix)
            print("Collaborative filtering model built successfully")
        except Exception as e:
            print(f"Error building collaborative model: {e}")
            # Create a dummy similarity matrix
            n_users = self.user_item_matrix.shape[0]
            self.collab_similarity = np.eye(n_users)

        print("Building content-based model...")
        # Build content-based model
        try:
            self.content_similarity = cosine_similarity(self.tfidf_matrix)
            print("Content-based model built successfully")
        except Exception as e:
            print(f"Error building content-based model: {e}")
            n_products = self.tfidf_matrix.shape[0]
            self.content_similarity = np.eye(n_products)

        print("Building KNN model...")
        # Build KNN model for hybrid approach
        try:
            self.knn_model = NearestNeighbors(n_neighbors=10, metric="cosine")
            self.knn_model.fit(self.user_item_matrix)
            print("KNN model built successfully")
        except Exception as e:
            print(f"Error building KNN model: {e}")
            self.knn_model = None

        print("All recommendation models built successfully!")

    def collaborative_filtering(self, user_id, n_recommendations=10):
        """Collaborative filtering based recommendations"""
        try:
            user_idx = self.dp.user_encoder.transform([user_id])[0]

            # Get similar users
            user_similarity = self.collab_similarity[user_idx]
            similar_users = np.argsort(user_similarity)[::-1][
                1:6
            ]  # Top 5 similar users

            # Get products rated by similar users
            similar_users_ratings = self.user_item_matrix.iloc[similar_users]
            recommended_products = similar_users_ratings.mean(axis=0).sort_values(
                ascending=False
            )

            # Filter out already rated products
            user_ratings = self.user_item_matrix.iloc[user_idx]
            unrated_products = recommended_products[user_ratings == 0]

            # Get top recommendations
            top_product_indices = unrated_products.head(n_recommendations).index
            product_ids = self.dp.product_encoder.inverse_transform(top_product_indices)

            return product_ids.tolist()
        except Exception as e:
            print(f"Error in collaborative filtering: {e}")
            return []

    def content_based_filtering(self, product_id, n_recommendations=10):
        """Content-based recommendations"""
        try:
            product_idx = self.product_features[
                self.product_features["product_id"] == product_id
            ].index[0]

            # Get similar products
            product_similarity = self.content_similarity[product_idx]
            similar_products = np.argsort(product_similarity)[::-1][
                1 : n_recommendations + 1
            ]

            recommended_product_ids = self.product_features.iloc[similar_products][
                "product_id"
            ].tolist()
            return recommended_product_ids
        except Exception as e:
            print(f"Error in content-based filtering: {e}")
            return []

    def hybrid_recommendation(self, user_id, n_recommendations=10):
        """Hybrid recommendation combining collaborative and content-based filtering"""
        print(f"Generating hybrid recommendations for user {user_id}")

        collab_recs = self.collaborative_filtering(user_id, n_recommendations)

        # If user has no history, use popular products
        if not collab_recs:
            print("No collaborative recommendations, using popular products")
            return self.get_popular_products(n_recommendations)

        # Enhance with content-based recommendations
        enhanced_recs = []
        for product_id in collab_recs[:3]:  # Use top 3 from collaborative
            content_recs = self.content_based_filtering(product_id, 2)
            enhanced_recs.extend(content_recs)

        # Combine and remove duplicates
        all_recs = list(set(collab_recs + enhanced_recs))
        return all_recs[:n_recommendations]

    def get_popular_products(self, n_recommendations=10):
        """Get most popular products based on ratings and purchase count"""
        try:
            popularity = (
                self.dp.df.groupby("product_id")
                .agg({"rating": "mean", "purchase_count": "sum"})
                .reset_index()
            )

            popularity["score"] = popularity["rating"] * popularity["purchase_count"]
            popular_products = popularity.nlargest(n_recommendations, "score")[
                "product_id"
            ].tolist()

            return popular_products
        except Exception as e:
            print(f"Error getting popular products: {e}")
            # Return random products as fallback
            return self.dp.df["product_id"].sample(n_recommendations).tolist()

    def get_user_recommendations(self, user_id, method="hybrid", n_recommendations=10):
        """Get recommendations for a user based on specified method"""
        print(f"Getting {method} recommendations for user {user_id}")

        if method == "collaborative":
            return self.collaborative_filtering(user_id, n_recommendations)
        elif method == "content":
            # For content-based, we need a product ID, so we'll use user's last viewed product
            user_history = self.dp.df[self.dp.df["user_id"] == user_id]
            if len(user_history) > 0:
                last_product = user_history.iloc[-1]["product_id"]
                return self.content_based_filtering(last_product, n_recommendations)
            else:
                return self.get_popular_products(n_recommendations)
        else:  # hybrid
            return self.hybrid_recommendation(user_id, n_recommendations)

    def save_model(self, path):
        """Save the recommendation model"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load_model(cls, path, data_processor):
        """Load a saved recommendation model"""
        with open(path, "rb") as f:
            model = pickle.load(f)
            model.dp = data_processor
            return model
