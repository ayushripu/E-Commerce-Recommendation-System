# E-Commerce Personalized Recommendation System

## Overview

This is a comprehensive E-commerce Personalized Recommendation System built with Python and Flask. The system implements multiple recommendation algorithms including collaborative filtering, content-based filtering, and hybrid approaches.

## Features

- **Multiple Recommendation Algorithms**: Collaborative, Content-based, and Hybrid
- **Interactive Dashboard**: Real-time analytics and visualization
- **RESTful API**: JSON endpoints for integration
- **Sample Data Generation**: Automatic creation of realistic e-commerce data
- **User-friendly Interface**: Bootstrap-based responsive design

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd ecommerce-recommendation-system
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

4. Open your browser and navigate to:

```text
http://localhost:5000
```

## Project Structure

- `app.py`: Main Flask application

- `models/`: Recommendation algorithms and data processing

- `templates/`: HTML templates for the web interface

- `static/`: CSS, JavaScript, and images

- `data/`: Sample dataset and data generation scripts

## Usage

- Dashboard: View overall statistics and analytics

- Recommendations: Get personalized product recommendations by selecting a user ID and recommendation method

- Product Details: View product information and similar products

- API Endpoints: Use /api/recommend/<user_id> for programmatic access

## Recommendation Methods

- Collaborative Filtering: Based on user similarity

- Content-Based Filtering: Based on product features and descriptions

- Hybrid Approach: Combines both methods for optimal results

## Technologies Used

1. Python 3.x
2. Flask
3. Scikit-learn
4. Pandas & NumPy
5. Bootstrap 5
6. Chart.js
