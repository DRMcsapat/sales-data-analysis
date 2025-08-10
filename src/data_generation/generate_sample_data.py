import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate sample e-commerce sales data
def generate_sales_data(n_records=2000):
    # Product categories and their typical price ranges
    categories = {
        'Electronics': (50, 2000),
        'Clothing': (20, 200),
        'Home & Garden': (15, 500),
        'Books': (10, 50),
        'Sports': (25, 300),
        'Beauty': (15, 150)
    }
    
    # Customer segments
    customer_segments = ['Regular', 'Premium', 'VIP']
    
    # Sales channels
    channels = ['Online', 'Store', 'Mobile App']
    
    # Generate date range (last 2 years)
    start_date = datetime.now() - timedelta(days=730)
    
    data = []
    
    for i in range(n_records):
        # Random date within the range
        random_days = random.randint(0, 730)
        order_date = start_date + timedelta(days=random_days)
        
        # Random category
        category = random.choice(list(categories.keys()))
        price_range = categories[category]
        
        # Generate price based on category
        base_price = random.uniform(price_range[0], price_range[1])
        
        # Random quantity (most orders are 1-3 items)
        quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.15, 0.07, 0.03])
        
        # Calculate total with some discount probability
        discount = random.choice([0, 0.05, 0.10, 0.15, 0.20]) if random.random() < 0.3 else 0
        unit_price = base_price * (1 - discount)
        total_amount = unit_price * quantity
        
        # Customer info
        customer_segment = np.random.choice(customer_segments, p=[0.6, 0.3, 0.1])
        customer_age = random.randint(18, 75)
        
        # Sales channel
        channel = np.random.choice(channels, p=[0.45, 0.35, 0.20])
        
        # Region
        region = random.choice(['North', 'South', 'East', 'West', 'Central'])
        
        # Add seasonal effects
        month = order_date.month
        if month in [11, 12]:  # Holiday season
            total_amount *= random.uniform(1.1, 1.3)
        elif month in [6, 7, 8]:  # Summer
            if category in ['Sports', 'Clothing']:
                total_amount *= random.uniform(1.05, 1.2)
        
        data.append({
            'order_id': f'ORD_{i+1:06d}',
            'order_date': order_date.strftime('%Y-%m-%d'),
            'category': category,
            'unit_price': round(unit_price, 2),
            'quantity': quantity,
            'total_amount': round(total_amount, 2),
            'customer_segment': customer_segment,
            'customer_age': customer_age,
            'sales_channel': channel,
            'region': region,
            'discount_applied': discount
        })
    
    return pd.DataFrame(data)

# Generate the dataset
df = generate_sales_data(2000)

# Save to CSV in the correct location
df.to_csv('data/processed/sales_data.csv', index=False)

print("Sample data generated successfully!")
print(f"Dataset shape: {df.shape}")
print("\nFirst few rows:")
print(df.head())
print("\nDataset info:")
print(df.info())