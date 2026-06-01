"""
Customer Shopping Behavior Analysis

Tasks:
1. Data exploration
2. Missing value handling
3. Feature engineering
4. Data cleaning
5. PostgreSQL data loading
"""

import pandas as pd

df = pd.read_csv('customer_shopping_behavior.csv')

print(df.head())
df.info()
print(df.tail())
print(df.describe(include='all'))
print(df.isnull().sum())

# fill the null value with median

df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
print(df.isnull().sum())

# claen the columns name

df.columns = df.columns.str.lower().str.replace(' ','_')
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})
print(df.columns)

# create a column age_group
my_labels = ['Young Adult', 'Adult', 'Middle_Aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=my_labels)
print(df[['age','age_group']].head(10))

# create column purchase_frequency_days
# print(df['frequency_of_purchases'].unique())
frequency_mapping = {
                'Fortnightly':14, 
                'Weekly':7, 
                'Monthly': 30,  
                'Quarterly': 90, 
                'Bi-Weekly': 14, 
                'Annually': 365, 
                'Every 3 Months': 90 }

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
print(df[['frequency_of_purchases', 'purchase_frequency_days' ]].head(10))

print((df['discount_applied'] == df['promo_code_used']).all())
df = df.drop('promo_code_used', axis=1)
print(df.columns)

from sqlalchemy import create_engine

# Step 1: Connect to PostgreSQL
# replace placeholder with your actual details
username = "postgres"  #default user
password = "your_password"  #password which set during installation
host = "localhost"  # if running locally
port = "5432"  #default postgreSQL port
database = "customer_behavior"  #database which was created in pgAdmin

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# Step 2: Load Dataframe into PostgreSQL
table_name = "customer"  #choose the table name 
df.to_sql(table_name, engine, if_exists="replace", index= False )

print(f"Data successfully loaded into table '{table_name} in database '{database}'.")

