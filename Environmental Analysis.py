import pandas as pd
import re
data = {
    'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Description': [
        'Forest Conservation Project in Spain',
        'River Cleanup Initiative Project 2021 in Portugal',
        'Urban Gardening Community Project in Germany',
        'Forest Reforestation Project 2022 in France',
        'Wildlife Protection Project Plan in Italy',
        'Endangered Species Conservation Project in Greece',
        'Wetland Restoration Project in Spain',
        'Marine Life Conservation Project in Portugal',
        'Air Quality Improvement Project Initiative in Germany',
        'Habitat Preservation Project for Birds in France'
    ],
    'Date': ['2021-03-15', '2021-06-20', '2022-01-11', '2022-04-05', '2023-02-22', '2023-05-30', '2021-09-13', '2022-07-19', '2023-03-08', '2022-11-21'],
    'Location': ['madrid, spain', 'LISBON, Portugal', 'berlin, germany', 'Paris, France', 'rome, Italy', 'Athens, GREECE', 'Valencia, Spain', 'PORTO, Portugal', 'Munich, Germany', 'Lyon, France'],
    'Budget': ['$20000', '€15000', '€12000', '£18000', '$25000', '€20000', '$17000', '€13000', '€11000', '£16000'],
    'Notes': [
        'Focusing on native forest species in Spain',
        'Cleanup of the Tagus river in Portugal. Endangered species alert!',
        'Community project in urban Berlin, Germany',
        'Reforestation of oak trees in Paris, France',
        'Plan for protecting local wildlife in Italy. Endangered species identified.',
        'Study on the impact on endangered bird species in Greece',
        'Restoration of wetlands in Valencia, Spain',
        'Conservation of marine life in Porto, Portugal',
        'Initiative for improving air quality in Munich, Germany',
        'Preservation of bird habitats in Lyon, France'
    ]
}



environment_df = pd.DataFrame(data)

print(environment_df)




# Standardising 'Location'
environment_df['Location'] = environment_df['Location'].apply(lambda x: x.title())

""" 
Standardise the format of the 'Location' column where each location should be in the format "City, Country". 

"""

# Extracting 'Year'
environment_df['Year'] = pd.to_datetime(environment_df['Date']).dt.year

"""
Additionally, extract the year from the 'Date' column and create a new column, 'Year'_summary__summary_
   
"""
print(environment_df)

# convert it to a numeric format for calculations
# Fixed conversion rates
conversion_rates = {'$': 1.0, '€': 1.1, '£': 1.3}  # Example rates: 1 Euro = 1.1 USD, 1 Pound = 1.3 USD

def convert_to_usd(budget_str):
    # Extracting the currency symbol and amount
    currency_symbol = budget_str[0]
    amount = float(budget_str[1:])

    # Converting to USD
    if currency_symbol in conversion_rates:
        return amount * conversion_rates[currency_symbol]
    else:
        return amount

# Converting 'Budget' to numeric USD values
environment_df['Budget_USD'] = environment_df['Budget'].apply(convert_to_usd)

# Calculating total budget for "forest"-related projects in USD
total_budget_forest_usd = environment_df[environment_df['Description'].str.contains("forest", case=False)]['Budget_USD'].sum()
print(total_budget_forest_usd)

# Identify all records in the Notes column that mention endangered species in a new column, 
# Using regex to identify mentions of endangered species
environment_df['Endangered_species'] = environment_df['Notes'].str.contains(r'endangered species', flags=re.IGNORECASE).map({True: 'Yes', False: 'No'})

print(environment_df)


# Extract 'Country' from 'Location'
"""
This code extracts 'Country' and 'Project Type' from the 'Location' and 'Description' columns respectively, 
generates a report summarising total projects and average budget by country, 
and identifies the top three most common project types in the dataset.
"""
environment_df['Country'] = environment_df['Location'].apply(lambda x: x.split(', ')[-1])
# Extract 'Project Type' from 'Description'
environment_df['Project_Type'] = environment_df['Description'].str.extract(r'(\b\w+\b) Project')[0]

# Generate the report
report = environment_df.groupby('Country').agg(
    Total_Projects=('ID', 'count'),
    Average_Budget=('Budget_USD', 'mean')
)

# Identify top three most common project types
top_project_types = environment_df['Project_Type'].value_counts().nlargest(3).index.tolist()
report['Top_Project_Types'] = ', '.join(top_project_types)

print(report)

