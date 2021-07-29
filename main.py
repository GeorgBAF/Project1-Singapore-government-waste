import pandas as pd
import numpy as np

# Recycling statistics per waste type for the period 2003 to 2017
df1 = pd.read_csv('datasets/wastestats.csv')

# Recycling statistics per waste type for the period 2018 to 2019
df2 = pd.read_csv('datasets/2018_2019_waste.csv')

# Estimations of the amount of energy saved per waste type in kWh
df3 = pd.read_csv('datasets/energy_saved.csv')

# Dropping cols that will not be used from df1
df1.drop(['waste_disposed_of_tonne', 'recycling_rate'], inplace=True, axis=1)

# Changing measurements of df2 to fit df1
df2["Total Generated ('000 tonnes)"] = df2["Total Generated ('000 tonnes)"].astype(float)*1000.0
df2["Total Recycled ('000 tonnes)"] = df2["Total Recycled ('000 tonnes)"].astype(float)*1000.0

# Changing type Total Generated Waste col in df1 to float
df1["total_waste_generated_tonne"] = df1["total_waste_generated_tonne"].astype(float)

# Changing col order of df1 to fit df2
cols = df1.columns.tolist()
cols = [cols[0], cols[2], cols[1], cols[3]]
df1 = df1[cols]

# Change to apropriate and same headers for both df1 and df2
df1.rename({'waste_type': 'Waste Type', 'total_waste_generated_tonne': 'Generated (tonne)', 'total_waste_recycled_tonne': 'Recycled (tonne)', 'year': 'Year'}, inplace=True, axis=1)
df2.rename({"Total Generated ('000 tonnes)": 'Generated (tonne)', "Total Recycled ('000 tonnes)": 'Recycled (tonne)'}, inplace=True, axis=1)


# Stack df1 and df2 on top of each other 
df = pd.concat([df1, df2])

# Limit df to include only data between 2015 and 2019
years = ['2015', '2016', '2017', '2018', '2019']
df = df.loc[df['Year'].isin(years)]

# Change any spelling of metals to 'Ferrous metals' and 'Non-ferrous metals'
# Currently: Non-Ferrous Metal, Non-ferrous Metal, Non-ferrous metal, Ferrous metals, Ferrous Metal ...
df.loc[df['Waste Type'].str.lower().str.contains("non-ferrous metal"), 'Waste Type'] = 'Non-ferrous metals'
df.loc[df['Waste Type'].str.lower().isin(["ferrous metal", "ferrous metals"]), 'Waste Type'] = 'Ferrous metals'

# Change any spelling of plastic to 'Plastics'
df.loc[df['Waste Type'].str.lower().str.contains("plastic"),'Waste Type'] = 'Plastics'

# Limit df to include only: Plastic, Glass, Ferrous Metal, and Non-Ferrous Metal
waste_types = ['Plastics', 'Glass', 'Ferrous metals', 'Non-ferrous metals']
df = df.loc[df['Waste Type'].isin(waste_types)]

# Sort by the year col
df = df.sort_values('Year', ascending=True)

# Add energy saved per tonne col
df.loc[df['Waste Type'] == 'Plastics', 'Energy (p/t)'] = float(df3.loc[3][1][0:-4])
df.loc[df['Waste Type'] == 'Glass', 'Energy (p/t)'] = float(df3.loc[3][2][0:-4])
df.loc[df['Waste Type'] == 'Ferrous metals', 'Energy (p/t)'] = float(df3.loc[3][3][0:-4])
df.loc[df['Waste Type'] == 'Non-ferrous metals', 'Energy (p/t)'] = float(df3.loc[3][4][0:-4])

# Calculate and add total energy saved col
df['Total Energy Saved (Kwh)'] = df['Recycled (tonne)'] * df['Energy (p/t)']

# Drop a few cols we not needed anymore
df.drop('Energy (p/t)', axis=1, inplace=True)
df.drop('Recycled (tonne)', axis=1, inplace=True)
df.drop('Generated (tonne)', axis=1, inplace=True)
df.drop('Waste Type', axis=1, inplace=True)

# Sum up total saved energy per year and assign the proper col names requested
df = df.groupby('Year')['Total Energy Saved (Kwh)'].sum().reset_index().rename(columns={'Total Energy Saved (Kwh)':'total_energy_saved','Year' : 'year'})

# Set year col as index
df = df.set_index('year')

# Create the final dataframe
annual_energy_savings = pd.DataFrame()

# Assigning df to the new dataframe with the name requested
annual_energy_savings = df

print(annual_energy_savings)

