import os


class Config:
    SECRET_KEY = "your-secret-key-here"
    DATA_FILE = "data/ecommerce_data.csv"
    MODEL_PATH = "models/saved_models/"

    # Recommendation settings
    TOP_N_RECOMMENDATIONS = 10
    SIMILARITY_THRESHOLD = 0.7
