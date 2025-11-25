import os
from flask import Flask, render_template, request, jsonify
from models.data_processor import DataProcessor
from models.recommendation_engine import RecommendationEngine
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Global variables
dp = None
re = None


def initialize_system():
    """Initialize the recommendation system"""
    global dp, re

    try:
        # Check if sample data exists, if not create it
        if not os.path.exists(app.config["DATA_FILE"]):
            print("Generating sample data...")
            from data.create_sample_data import generate_sample_data

            df = generate_sample_data()
            df.to_csv(app.config["DATA_FILE"], index=False)
            print("Sample data generated successfully!")

        # Initialize data processor and recommendation engine
        dp = DataProcessor(app.config["DATA_FILE"])
        dp.load_data()

        re = RecommendationEngine(dp)
        re.build_models()

        print("Recommendation system initialized successfully!")

    except Exception as e:
        print(f"Error initializing system: {e}")
        # Create a fallback system
        dp = DataProcessor(app.config["DATA_FILE"])
        dp.load_data()
        re = RecommendationEngine(dp)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    """Main dashboard with analytics"""
    try:
        # Basic statistics
        total_users = dp.df["user_id"].nunique()
        total_products = dp.df["product_id"].nunique()
        total_transactions = len(dp.df)
        avg_rating = dp.df["rating"].mean()

        # Top products - ensure we have the right columns
        top_products_data = (
            dp.df.groupby("product_id")
            .agg(
                {
                    "product_name": "first",
                    "category": "first",
                    "rating": "mean",
                    "purchase_count": "sum",
                    "price": "first",
                }
            )
            .nlargest(5, "purchase_count")
            .reset_index()
        )

        # Convert to dictionary with proper handling
        top_products_dict = []
        for _, row in top_products_data.iterrows():
            top_products_dict.append(
                {
                    "product_id": int(row["product_id"]),
                    "product_name": str(row["product_name"]),
                    "category": str(row["category"]),
                    "rating": float(row["rating"]),
                    "purchase_count": int(row["purchase_count"]),
                    "price": float(row["price"]),
                    "brand": str(row["brand"]) if "brand" in row else "Generic",
                }
            )

        # Category distribution - ensure proper data format
        category_dist_data = dp.df.groupby("category").size().reset_index(name="count")
        category_dist_dict = []
        for _, row in category_dist_data.iterrows():
            category_dist_dict.append(
                {"category": str(row["category"]), "count": int(row["count"])}
            )

        # Get market insights
        insights = {
            "avg_price": float(dp.df["price"].mean()),
            "top_category": str(category_dist_data.iloc[0]["category"]),
            "avg_products_per_user": float(
                dp.df.groupby("user_id")["product_id"].nunique().mean()
            ),
        }

        return render_template(
            "dashboard.html",
            total_users=total_users,
            total_products=total_products,
            total_transactions=total_transactions,
            avg_rating=round(avg_rating, 2),
            top_products=top_products_dict,
            category_dist=category_dist_dict,
            insights=insights,
        )

    except Exception as e:
        print(f"Dashboard error: {e}")
        import traceback

        traceback.print_exc()
        return f"Error loading dashboard: {str(e)}"


@app.route("/recommendations", methods=["GET", "POST"])
def recommendations():
    """Get personalized recommendations"""
    if request.method == "POST":
        user_id = int(request.form["user_id"])
        method = request.form.get("method", "hybrid")
        n_recommendations = int(request.form.get("n_recommendations", 10))

        # Get recommendations
        recommended_product_ids = re.get_user_recommendations(
            user_id, method, n_recommendations
        )

        # Get product details
        recommended_products = []
        for product_id in recommended_product_ids:
            product_info = dp.df[dp.df["product_id"] == product_id].iloc[0]
            recommended_products.append(
                {
                    "product_id": product_id,
                    "product_name": product_info["product_name"],
                    "category": product_info["category"],
                    "price": product_info["price"],
                    "brand": product_info["brand"],
                    "rating": product_info["rating"],
                }
            )

        # Get user history
        user_history = dp.df[dp.df["user_id"] == user_id].nlargest(5, "timestamp")

        return render_template(
            "recommendations.html",
            user_id=user_id,
            method=method,
            recommendations=recommended_products,
            user_history=user_history.to_dict("records"),
        )

    return render_template("recommendations.html")


@app.route("/api/recommend/<int:user_id>")
def api_recommend(user_id):
    """API endpoint for recommendations"""
    method = request.args.get("method", "hybrid")
    n_recommendations = int(request.args.get("n", 10))

    try:
        recommended_product_ids = re.get_user_recommendations(
            user_id, method, n_recommendations
        )

        recommended_products = []
        for product_id in recommended_product_ids:
            product_info = dp.df[dp.df["product_id"] == product_id].iloc[0]
            recommended_products.append(
                {
                    "product_id": product_id,
                    "product_name": product_info["product_name"],
                    "category": product_info["category"],
                    "price": product_info["price"],
                    "brand": product_info["brand"],
                    "rating": product_info["rating"],
                }
            )

        return jsonify(
            {
                "success": True,
                "user_id": user_id,
                "method": method,
                "recommendations": recommended_products,
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/stats")
def api_stats():
    """API endpoint for statistics"""
    total_users = dp.df["user_id"].nunique()
    total_products = dp.df["product_id"].nunique()
    total_transactions = len(dp.df)
    avg_rating = dp.df["rating"].mean()

    return jsonify(
        {
            "total_users": total_users,
            "total_products": total_products,
            "total_transactions": total_transactions,
            "average_rating": round(avg_rating, 2),
        }
    )


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    """Product detail page with similar products"""
    product_info = dp.df[dp.df["product_id"] == product_id].iloc[0]

    # Get similar products
    similar_products_ids = re.content_based_filtering(product_id, 5)
    similar_products = []

    for sim_product_id in similar_products_ids:
        sim_product_info = dp.df[dp.df["product_id"] == sim_product_id].iloc[0]
        similar_products.append(
            {
                "product_id": sim_product_id,
                "product_name": sim_product_info["product_name"],
                "category": sim_product_info["category"],
                "price": sim_product_info["price"],
                "rating": sim_product_info["rating"],
            }
        )

    return render_template(
        "product_detail.html", product=product_info, similar_products=similar_products
    )


if __name__ == "__main__":
    initialize_system()
    app.run(debug=True, host="0.0.0.0", port=5000)
