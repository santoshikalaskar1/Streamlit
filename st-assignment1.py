import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from PIL import Image


header_style = '''
    <style>
        table th {
            background-color: #FFF933;
            font-size: 20px;
            font-family: "Courier New";
        }
        h1{
            color:#6B33FF;
            font-size:28px;
            text-align:center;
        }
        h4{
            color:#33ff33;
            font-size:18px;
            text-align:center;
        }
        
    </style>

'''
st.markdown(header_style, unsafe_allow_html=True)

# st.markdown(f'<h1 style="color:#33ff33;font-size:24px;">{"ColorMeBlue text”"}</h1>', unsafe_allow_html=True)
st.markdown("""
# Sample Sales Data
#### Shown are the sample sales data having **Date,Manufacturer,Category,Brand,SKU Name,Volume,Value and Price**
""")

data = pd.read_csv("Input_Sales_Data_v2.csv")
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

data["Date"] = pd.to_datetime(data["Date"]).dt.date

# print (data.Date.min())
# print (data.Date.max())

format = 'MMM DD, YYYY'  

start_date = data.Date.min()  
end_date = data.Date.max()
max_days = end_date-start_date

selected_date = st.slider('Select Date Range', min_value=start_date, value=end_date ,max_value=end_date, format=format)

st.table(pd.DataFrame([[start_date, selected_date, end_date]],
                columns=['start',
                        'selected',
                        'end'],
                index=['date']))

st.write("---")

st.write("#### Total **Volume sales** and **Value sales** at the Manufacturer Level")

# Filter the dataframe based on the selected date range
filtered_df = data[(data['Date'] >= start_date) & (data['Date'] <= selected_date)]

# Display the total volume and value sales at the manufacturer level
manufacturer_sales = filtered_df.groupby('Manufacturer')[['Volume', 'Value']].sum().sort_values(by='Value', ascending=False)
st.dataframe(manufacturer_sales, width=800)
st.markdown("---")

# Get the top 5 manufacturers for the selected period
top_manufacturers = filtered_df.groupby('Manufacturer')['Value'].sum().nlargest(5).index.tolist()
print(top_manufacturers)

# Group the data by manufacturer and date to calculate the total sales over time
manufacturer_sales = filtered_df.groupby(['Manufacturer', 'Date'], as_index=False)['Value'].sum()

# filter out top manufactor data by date wise
new_manufacturer = manufacturer_sales["Manufacturer"].isin(top_manufacturers)
new_manufacturer_df = manufacturer_sales[new_manufacturer].sort_values(by='Date')

for manufacturer in top_manufacturers:
    new_manufacturer_df_plot = new_manufacturer_df[new_manufacturer_df['Manufacturer'] == manufacturer]
    # Plot the filtered data
    plt.plot(new_manufacturer_df_plot['Date'], new_manufacturer_df_plot['Value'], label=manufacturer)

# Set the x-axis label
plt.xlabel('Date')
# Format the x-axis tick labels as months
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
# Rotate the x-axis tick labels for better readability
plt.xticks(rotation=45)
# Set the y-axis label
plt.ylabel('Value Sales')
# Set the plot title
plt.title('Top 5 Manufacturers Sales Trends')
# Move the legend outside the plot
plt.legend(bbox_to_anchor=(0.05, 1), loc='upper left')
# Display the plot

st.write("#### Line chart Showing the trends for top 5 manufacturers")
st.pyplot(plt, use_container_width=True)
st.markdown("---")
st.write("#### Dataframe of Line chart Showing the trends for top 5 manufacturers")
st.dataframe(new_manufacturer_df, width=800)


image = Image.open('Tiger_LOGO.png')

st.sidebar.image(image, caption='Streamlit Assignment-1')

# Extra code

# def resistance(x, color):
#     return np.where(x=='Resistant', f"background-color: {color};", None)

# def null_row(x):
#     return np.where(x=='', "height: 12px;", "height: 1px;")

# df = pd.DataFrame(columns=["interpretation"], data=[[""], ["Resistant"], [""], ["Resistant"]])
# df_style = df.style.apply(resistance, color='#fcdcdc').apply(null_row)
                   
# st.table(df_style)