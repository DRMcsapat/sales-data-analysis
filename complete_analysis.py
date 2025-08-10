# Sales Data Analysis - Complete Analysis
# ========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
plt.style.use('default')
sns.set_palette("husl")

print("=" * 60)
print("SALES DATA ANALYSIS - E-COMMERCE BUSINESS INTELLIGENCE")
print("=" * 60)

# Load the dataset
print("\n1. LOADING DATA...")
df = pd.read_csv('data/processed/sales_data.csv')

print(f"Dataset shape: {df.shape}")
print(f"Date range: {df['order_date'].min()} to {df['order_date'].max()}")
print("\nFirst 5 rows:")
print(df.head())

# Data preprocessing
print("\n2. DATA PREPROCESSING...")
df['order_date'] = pd.to_datetime(df['order_date'])
df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month
df['quarter'] = df['order_date'].dt.quarter

print("Data types after preprocessing:")
print(df.dtypes)

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

print("\n3. BUSINESS ANALYSIS")
print("=" * 40)

# Question 1: Product Category Performance
print("\n📊 QUESTION 1: What are our top-performing product categories by revenue?")
category_revenue = df.groupby('category')['total_amount'].agg(['sum', 'count', 'mean']).round(2)
category_revenue.columns = ['Total Revenue', 'Number of Orders', 'Average Order Value']
category_revenue = category_revenue.sort_values('Total Revenue', ascending=False)

print("\nRevenue Analysis by Category:")
print(category_revenue)

# Visualization 1: Category Performance
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Product Category Performance Analysis', fontsize=16, fontweight='bold')

# Revenue by category
axes[0,0].bar(category_revenue.index, category_revenue['Total Revenue'], 
              color=sns.color_palette("husl", len(category_revenue)))
axes[0,0].set_title('Total Revenue by Category')
axes[0,0].set_ylabel('Revenue ($)')
axes[0,0].tick_params(axis='x', rotation=45)

# Number of orders by category
axes[0,1].bar(category_revenue.index, category_revenue['Number of Orders'],
              color=sns.color_palette("viridis", len(category_revenue)))
axes[0,1].set_title('Number of Orders by Category')
axes[0,1].set_ylabel('Number of Orders')
axes[0,1].tick_params(axis='x', rotation=45)

# Average order value by category
axes[1,0].bar(category_revenue.index, category_revenue['Average Order Value'],
              color=sns.color_palette("plasma", len(category_revenue)))
axes[1,0].set_title('Average Order Value by Category')
axes[1,0].set_ylabel('Average Order Value ($)')
axes[1,0].tick_params(axis='x', rotation=45)

# Revenue distribution pie chart
axes[1,1].pie(category_revenue['Total Revenue'], labels=category_revenue.index, autopct='%1.1f%%')
axes[1,1].set_title('Revenue Distribution by Category')

plt.tight_layout()
plt.savefig('outputs/figures/category_performance.png', dpi=300, bbox_inches='tight')
plt.show()

# Question 2: Time Trends
print("\n📈 QUESTION 2: How do sales trends vary over time?")

# Monthly sales trends
monthly_sales = df.groupby(['year', 'month'])['total_amount'].sum().reset_index()
monthly_sales['date'] = pd.to_datetime(monthly_sales[['year', 'month']].assign(day=1))

print("\nMonthly Sales Trends:")
print(monthly_sales.tail(12))

# Visualization 2: Time Trends
plt.figure(figsize=(15, 8))

# Monthly revenue trend
plt.subplot(2, 2, 1)
plt.plot(monthly_sales['date'], monthly_sales['total_amount'], marker='o', linewidth=2)
plt.title('Monthly Revenue Trends')
plt.xlabel('Date')
plt.ylabel('Revenue ($)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Seasonal patterns
plt.subplot(2, 2, 2)
monthly_avg = df.groupby('month')['total_amount'].mean()
plt.bar(monthly_avg.index, monthly_avg.values, color=sns.color_palette("coolwarm", 12))
plt.title('Average Revenue by Month (Seasonal Pattern)')
plt.xlabel('Month')
plt.ylabel('Average Revenue ($)')

# Daily sales distribution
plt.subplot(2, 2, 3)
df['day_of_week'] = df['order_date'].dt.day_name()
daily_sales = df.groupby('day_of_week')['total_amount'].sum()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_sales = daily_sales.reindex(day_order)
plt.bar(daily_sales.index, daily_sales.values, color=sns.color_palette("Set2", 7))
plt.title('Revenue by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Revenue ($)')
plt.xticks(rotation=45)

# Quarterly comparison
plt.subplot(2, 2, 4)
quarterly_sales = df.groupby(['year', 'quarter'])['total_amount'].sum().reset_index()
quarterly_pivot = quarterly_sales.pivot(index='quarter', columns='year', values='total_amount')
quarterly_pivot.plot(kind='bar', ax=plt.gca())
plt.title('Quarterly Revenue Comparison')
plt.xlabel('Quarter')
plt.ylabel('Revenue ($)')
plt.legend(title='Year')
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig('outputs/figures/time_trends.png', dpi=300, bbox_inches='tight')
plt.show()

# Question 3: Customer Segmentation
print("\n👥 QUESTION 3: Customer Segmentation Analysis")

segment_analysis = df.groupby('customer_segment').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'quantity': 'mean',
    'discount_applied': 'mean'
}).round(2)

segment_analysis.columns = ['Total Revenue', 'Avg Order Value', 'Order Count', 'Avg Quantity', 'Avg Discount']

print("\nCustomer Segment Analysis:")
print(segment_analysis)

# Visualization 3: Customer Segments
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Customer Segment Analysis', fontsize=16, fontweight='bold')

# Revenue by segment
axes[0,0].bar(segment_analysis.index, segment_analysis['Total Revenue'],
              color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
axes[0,0].set_title('Total Revenue by Customer Segment')
axes[0,0].set_ylabel('Revenue ($)')

# Average order value by segment
axes[0,1].bar(segment_analysis.index, segment_analysis['Avg Order Value'],
              color=['#96CEB4', '#FFEAA7', '#DDA0DD'])
axes[0,1].set_title('Average Order Value by Segment')
axes[0,1].set_ylabel('Average Order Value ($)')

# Customer age distribution by segment
segments = ['Regular', 'Premium', 'VIP']
age_data = [df[df['customer_segment']==seg]['customer_age'].values for seg in segments if seg in df['customer_segment'].values]
axes[1,0].boxplot(age_data, labels=[seg for seg in segments if seg in df['customer_segment'].values])
axes[1,0].set_title('Customer Age Distribution by Segment')
axes[1,0].set_ylabel('Age')

# Orders count by segment
axes[1,1].pie(segment_analysis['Order Count'], labels=segment_analysis.index, 
              autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4', '#45B7D1'])
axes[1,1].set_title('Order Distribution by Segment')

plt.tight_layout()
plt.savefig('outputs/figures/customer_segments.png', dpi=300, bbox_inches='tight')
plt.show()

# Question 4: Sales Channel Performance
print("\n📱 QUESTION 4: Sales Channel Performance")

channel_performance = df.groupby('sales_channel').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_age': 'mean'
}).round(2)

channel_performance.columns = ['Total Revenue', 'Avg Order Value', 'Order Count', 'Avg Customer Age']

print("\nSales Channel Performance:")
print(channel_performance)

# Cross-analysis: Channel vs Category
channel_category = pd.crosstab(df['sales_channel'], df['category'], 
                              values=df['total_amount'], aggfunc='sum').fillna(0)

print("\nRevenue by Channel and Category:")
print(channel_category.round(2))

# Visualization 4: Channel Analysis
plt.figure(figsize=(15, 10))

# Channel revenue
plt.subplot(2, 3, 1)
plt.bar(channel_performance.index, channel_performance['Total Revenue'])
plt.title('Revenue by Sales Channel')
plt.ylabel('Revenue ($)')
plt.xticks(rotation=45)

# Channel vs Category heatmap
plt.subplot(2, 3, 2)
sns.heatmap(channel_category, annot=True, fmt='.0f', cmap='Blues')
plt.title('Revenue Heatmap: Channel vs Category')
plt.ylabel('Sales Channel')
plt.xlabel('Category')

# Average order value by channel
plt.subplot(2, 3, 3)
plt.bar(channel_performance.index, channel_performance['Avg Order Value'], color='lightcoral')
plt.title('Avg Order Value by Channel')
plt.ylabel('Average Order Value ($)')
plt.xticks(rotation=45)

# Regional analysis
plt.subplot(2, 3, 4)
regional_sales = df.groupby('region')['total_amount'].sum().sort_values(ascending=False)
plt.bar(regional_sales.index, regional_sales.values, color='lightgreen')
plt.title('Revenue by Region')
plt.ylabel('Revenue ($)')
plt.xticks(rotation=45)

# Price distribution
plt.subplot(2, 3, 5)
plt.hist(df['total_amount'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
plt.title('Order Value Distribution')
plt.xlabel('Order Value ($)')
plt.ylabel('Frequency')

# Correlation analysis
plt.subplot(2, 3, 6)
numeric_cols = ['unit_price', 'quantity', 'total_amount', 'customer_age', 'discount_applied']
correlation_matrix = df[numeric_cols].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')

plt.tight_layout()
plt.savefig('outputs/figures/channel_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Key Insights and Recommendations
print("\n" + "="*60)
print("KEY BUSINESS INSIGHTS AND RECOMMENDATIONS")
print("="*60)

print("\n1. PRODUCT CATEGORY PERFORMANCE:")
if len(category_revenue) > 0:
    top_category = category_revenue.index[0]
    top_revenue = category_revenue.iloc[0]['Total Revenue']
    print(f"   • {top_category} is our top performer with ${top_revenue:,.2f} in revenue")
print(f"   • Recommendation: Focus marketing budget on top 3 categories")

print("\n2. SEASONAL TRENDS:")
peak_month = monthly_avg.idxmax()
peak_revenue = monthly_avg.max()
print(f"   • Peak sales month: {peak_month} (Avg: ${peak_revenue:,.2f})")
print(f"   • Recommendation: Prepare inventory and marketing campaigns for seasonal peaks")

print("\n3. CUSTOMER SEGMENTS:")
if 'VIP' in segment_analysis.index and 'Regular' in segment_analysis.index:
    vip_aov = segment_analysis.loc['VIP', 'Avg Order Value']
    regular_aov = segment_analysis.loc['Regular', 'Avg Order Value']
    print(f"   • VIP customers have {(vip_aov/regular_aov-1)*100:.1f}% higher average order value")
print(f"   • Recommendation: Develop loyalty programs to convert Regular to Premium/VIP")

print("\n4. SALES CHANNELS:")
best_channel = channel_performance['Total Revenue'].idxmax()
best_channel_revenue = channel_performance.loc[best_channel, 'Total Revenue']
print(f"   • {best_channel} is the highest revenue channel: ${best_channel_revenue:,.2f}")
print(f"   • Recommendation: Optimize user experience on top-performing channels")

print("\n5. REGIONAL OPPORTUNITIES:")
top_region = regional_sales.index[0]
bottom_region = regional_sales.index[-1]
print(f"   • {top_region} region leads sales, {bottom_region} region has growth potential")
print(f"   • Recommendation: Investigate market penetration strategies for underperforming regions")

# Statistical Summary
print("\n" + "="*60)
print("STATISTICAL SUMMARY")
print("="*60)

total_revenue = df['total_amount'].sum()
total_orders = len(df)
avg_order_value = df['total_amount'].mean()

print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Average Order Value: ${avg_order_value:.2f}")
print(f"Date Range: {df['order_date'].min().date()} to {df['order_date'].max().date()}")

print("\n✅ Analysis completed successfully!")
print("📊 Charts saved in outputs/figures/")
print("📄 Check the generated PNG files for visualizations")