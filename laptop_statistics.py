import pandas as pd
import numpy as np
from scipy import stats

# Create realistic laptop dataset
np.random.seed(42)  # For reproducible results

# 10 laptops with 10 specifications
laptops_data = {
    'Brand': ['Dell', 'HP', 'Lenovo', 'Apple', 'ASUS', 'Acer', 'MSI', 'Razer', 'Microsoft', 'LG'],
    'Model': ['XPS 15', 'Spectre x360', 'ThinkPad X1', 'MacBook Pro', 'ROG Strix', 'Swift 3', 'GS66', 'Blade 15', 'Surface Pro', 'Gram 17'],
    'Price ($)': [1499, 1299, 1599, 1999, 1799, 899, 1699, 2499, 1199, 1399],
    'Screen_Size (inch)': [15.6, 14.0, 14.0, 14.0, 15.6, 14.0, 15.6, 15.6, 13.0, 17.0],
    'RAM (GB)': [16, 16, 16, 16, 32, 8, 32, 16, 16, 16],
    'Storage (GB)': [512, 512, 1024, 512, 1024, 256, 1024, 1024, 256, 512],
    'CPU_Speed (GHz)': [2.6, 2.8, 2.4, 2.4, 2.3, 3.2, 2.4, 2.6, 2.4, 2.8],
    'Battery_Life (hours)': [8.5, 10.0, 12.0, 10.5, 6.0, 11.0, 7.5, 5.5, 10.5, 14.0],
    'Weight (kg)': [1.8, 1.3, 1.4, 1.6, 2.3, 1.2, 2.1, 2.0, 0.8, 1.4],
    'Performance_Score': [85, 80, 88, 92, 95, 75, 90, 93, 78, 82]
}

# Create DataFrame
df = pd.DataFrame(laptops_data)

print("=== LAPTOP DATASET (10 rows × 10 columns) ===")
print(df.to_string(index=False))
print("\n" + "="*80)

# Calculate statistics for numerical columns
numerical_columns = ['Price ($)', 'Screen_Size (inch)', 'RAM (GB)', 'Storage (GB)', 
                    'CPU_Speed (GHz)', 'Battery_Life (hours)', 'Weight (kg)', 'Performance_Score']

print("\n=== STATISTICAL ANALYSIS ===")
for col in numerical_columns:
    data = df[col]
    
    print(f"\n--- {col} ---")
    print(f"Count: {len(data)}")
    print(f"Mean: {data.mean():.2f}")
    print(f"Median: {data.median():.2f}")
    print(f"Mode: {data.mode().iloc[0] if not data.mode().empty else 'No mode'}")
    print(f"Standard Deviation: {data.std():.2f}")
    print(f"Variance: {data.var():.2f}")
    print(f"Minimum: {data.min():.2f}")
    print(f"Maximum: {data.max():.2f}")
    print(f"Range: {data.max() - data.min():.2f}")
    print(f"25th Percentile (Q1): {data.quantile(0.25):.2f}")
    print(f"75th Percentile (Q3): {data.quantile(0.75):.2f}")
    print(f"IQR: {data.quantile(0.75) - data.quantile(0.25):.2f}")
    print(f"Skewness: {stats.skew(data):.3f}")
    print(f"Kurtosis: {stats.kurtosis(data):.3f}")

print("\n" + "="*80)
print("=== CORRELATION MATRIX ===")
correlation_matrix = df[numerical_columns].corr()
print(correlation_matrix.round(3))

print("\n" + "="*80)
print("=== STATISTICAL FORMULAS USED ===")
print("""
1. Mean (Average): μ = Σx / n
2. Median: Middle value when sorted
3. Mode: Most frequent value
4. Standard Deviation: σ = √(Σ(x - μ)² / (n-1))
5. Variance: σ² = Σ(x - μ)² / (n-1)
6. Range: Max - Min
7. Percentiles: Values below which a given percentage of observations fall
8. IQR: Q3 - Q1 (Interquartile Range)
9. Skewness: Measures asymmetry of the distribution
10. Kurtosis: Measures tail heaviness of the distribution
11. Correlation: r = Σ((x-μx)(y-μy)) / √(Σ(x-μx)² * Σ(y-μy)²)
""")

print("\n" + "="*80)
print("=== SUMMARY STATISTICS ===")
summary_stats = df[numerical_columns].describe().round(2)
print(summary_stats)
