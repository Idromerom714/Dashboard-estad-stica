import streamlit as st
import plotly.express as px
import pandas as pd

# Load or regenerate the dataframes
# Assuming the data is available at this path or can be re-read
try:
    datos = pd.read_csv('consumer_behavior_dataset.csv')
    datos = datos.drop(['user_id', 'product_id'], axis=1)
    datos['purchase_date'] = pd.to_datetime(datos['purchase_date'])
    datos['purchase_month'] = datos['purchase_date'].dt.month
    categorical_cols = ['category', 'payment_method', 'gender', 'income_level']
    datos = pd.get_dummies(datos, columns=categorical_cols, drop_first=True)
    monthly_category_sales = datos.groupby(['purchase_month', 'category_Clothing', 'category_Electronics', 'category_Furniture', 'category_Grocery'])['price'].sum().reset_index()

except FileNotFoundError:
    st.error("Data file not found. Please ensure 'consumer_behavior_dataset.csv' is in the correct path.")
    st.stop()


# Design the layout
st.title('Consumer Behavior Dashboard')

# Monthly Sales by Category
st.header('Monthly Sales by Category')
# Melt the monthly_category_sales dataframe to long format for easier plotting
monthly_category_sales_melted = monthly_category_sales.melt(
    id_vars=['purchase_month', 'price'],
    value_vars=['category_Clothing', 'category_Electronics', 'category_Furniture', 'category_Grocery'],
    var_name='category',
    value_name='is_category'
)
monthly_category_sales_melted = monthly_category_sales_melted[monthly_category_sales_melted['is_category'] == True]
monthly_category_sales_melted['category'] = monthly_category_sales_melted['category'].str.replace('category_', '')

fig_monthly_sales = px.bar(
    monthly_category_sales_melted,
    x='purchase_month',
    y='price',
    color='category',
    title='Total Sales per Category by Month'
)
st.plotly_chart(fig_monthly_sales)

# Distribution of Numerical Features
st.header('Distribution of Numerical Features')
numerical_cols = ['price', 'discount_applied', 'pages_visited', 'time_spent', 'rating', 'age', 'sentiment_score']
selected_numerical_col = st.selectbox('Select a numerical feature:', numerical_cols)

fig_hist = px.histogram(datos, x=selected_numerical_col, title=f'Distribution of {selected_numerical_col}')
st.plotly_chart(fig_hist)

# Distribution of Categorical Features
st.header('Distribution of Categorical Features')
categorical_cols_display = ['payment_method', 'gender', 'income_level']
selected_categorical_col = st.selectbox('Select a categorical feature:', categorical_cols_display)

# Need to get the original categorical data before one-hot encoding for count plots
# Reloading a small part of the data just for categorical counts for display purposes
# In a real app, you might want to store the original categorical data
datos_original_categorical = pd.read_csv('/consumer_behavior_dataset.csv')
datos_original_categorical = datos_original_categorical.drop(['user_id', 'product_id'], axis=1)


fig_count = px.histogram(datos_original_categorical, x=selected_categorical_col, title=f'Count of {selected_categorical_col}')
st.plotly_chart(fig_count)
