from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Load and process data
def process_data():
    df = pd.read_csv('train.csv')

    # Fix here: tell pandas to parse dates with day first (dd/mm/yyyy)
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

    df['Month'] = df['Order Date'].dt.to_period('M')

    # rest of your code...


    # Example revenue column (you can adjust if you have Quantity and UnitPrice instead)
    df['Revenue'] = df['Sales']  # Using 'Sales' as Revenue

    # Top 5 products by total revenue
    top_products = df.groupby('Product Name')['Revenue'].sum().sort_values(ascending=False).head(5)

    # Monthly revenue
    monthly_revenue = df.groupby('Month')['Revenue'].sum()

    # Save visualizations
    os.makedirs('static', exist_ok=True)

    plt.figure(figsize=(10, 5))
    top_products.plot(kind='bar')
    plt.title('Top 5 Best-Selling Products')
    plt.ylabel('Revenue')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/top_products.png')
    plt.close()

    plt.figure(figsize=(10, 5))
    monthly_revenue.plot(kind='line', marker='o')
    plt.title('Monthly Revenue Trend')
    plt.ylabel('Revenue')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/monthly_revenue.png')
    plt.close()

@app.route('/')
def index():
    process_data()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
