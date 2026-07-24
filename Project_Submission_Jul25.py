
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set plotting style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# ----------------------------------------------------
# 1. DATASET OVERVIEW & LOADING
# ----------------------------------------------------
print("--- Step 1: Loading Dataset ---")

df = pd.read_csv("/retail_large_dataset.csv")

# Derived column with high kurtosis due to extreme high values (bulk purchases)
df['final_price'] = (df['product_price'] * df['quantity']) * (1 - df['discount_percentage']/100)
# Injecting artificial extreme outliers
df.loc[np.random.choice(df.index, 500), 'final_price'] *= 5 

print(df.info())
print(df.head())


# ----------------------------------------------------
# 2. UNIVARIATE ANALYSIS
# ----------------------------------------------------
print("\n--- Step 2: Univariate Analysis ---")

# 4.1 Numerical Variables Summary
num_cols = ['product_price', 'final_price', 'discount_percentage', 'quantity', 'age', 'delivery_days']
univariate_summary = pd.DataFrame({
    'Mean': df[num_cols].mean(),
    'Median': df[num_cols].median(),
    'Std Dev': df[num_cols].std(),
    'Min': df[num_cols].min(),
    'Max': df[num_cols].max(),
    'Skewness': df[num_cols].skew(),
    'Kurtosis': df[num_cols].kurtosis()
})
print("Numerical Variables Distribution Summary:")
print(univariate_summary)

# Plotting distributions matching insights
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
sns.histplot(df['product_price'], kde=True, ax=axes[0], color='blue').set_title('Product Price (Positive Skew)')
sns.histplot(df['final_price'], kde=True, ax=axes[1], color='green').set_title('Final Price (High Kurtosis)')
sns.histplot(df['discount_percentage'], ax=axes[2], color='orange').set_title('Discount % (Uniform)')
plt.tight_layout()
plt.show()

# 4.2 Categorical Variables Summary
cat_cols = ['product_category', 'customer_segment', 'payment_method', 'shipping_type']
for col in cat_cols:
    print(col.upper(), "Frequency Distribution:")
    print(df[col].value_counts(normalize=True) * 100)
    print("-" * 30)


# ----------------------------------------------------
# 3. OUTLIER DETECTION
# ----------------------------------------------------
print("\n--- Step 3: Outlier Detection ---")

# Method A: Interquartile Range (IQR) Method
Q1 = df['final_price'].quantile(0.25)
Q3 = df['final_price'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

iqr_outliers = df[(df['final_price'] < lower_bound) | (df['final_price'] > upper_bound)]
print(f"Number of outliers detected via IQR method in final_price: {len(iqr_outliers)}")

# Method B: Z-score Method
z_scores = np.abs(stats.zscore(df['final_price']))
z_outliers = df[z_scores > 3]
print(f"Number of outliers detected via Z-score method (>3 std dev): {len(z_outliers)}")

# Boxplot Visualization
