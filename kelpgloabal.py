import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load the credit ratings dataset and mapping dataset
credit_ratings_df = pd.read_csv('credit_ratings.csv')
mapping_df = pd.read_excel('mapping.xlsx')

# Function to extract the link from the screener.in page
def get_screener_link(cin, rating_agency):
    url = f'https://www.screener.in/company/{cin}/ratings/{rating_agency}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    link = soup.find('a', {'class': 'icon-ratios doc'}).get('href') if soup.find('a', {'class': 'icon-ratios doc'}) else None
    return link

# Map the links to the credit ratings dataset
credit_ratings_df['Link'] = credit_ratings_df.apply(lambda row: get_screener_link(row['CIN number'], row['Rating Agency']), axis=1)

# Merge with the mapping dataset to get the screener link
final_df = pd.merge(credit_ratings_df, mapping_df, on='CIN number', how='left')

# Save the final dataset to an excel file
final_df.to_excel('final_dataset.xlsx', index=False)