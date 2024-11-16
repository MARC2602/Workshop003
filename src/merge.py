import pandas as pd

df15 = pd.read_csv("../Data/raw/2015.csv", delimiter=',')
df16 = pd.read_csv("../Data/raw/2016.csv", delimiter=',')
df17 = pd.read_csv("../Data/raw/2017.csv", delimiter=',')
df18 = pd.read_csv("../Data/raw/2018.csv", delimiter=',')
df19 = pd.read_csv("../Data/raw/2019.csv", delimiter=',')

mapping = {
    'Country or region': 'Country',
    'Happiness Rank': 'Rank',
    'Happiness.Rank': 'Rank',
    'Overall rank': 'Rank',
    'Economy (GDP per Capita)': 'GDP per Capita',
    'GDP per capita': 'GDP per Capita',
    'Economy..GDP.per.Capita.': 'GDP per Capita',
    'Health (Life Expectancy)': 'Life Expectancy',
    'Health..Life.Expectancy.': 'Life Expectancy',
    'Healthy life expectancy': 'Life Expectancy',
    'Trust (Government Corruption)': 'Government Corruption',
    'Trust..Government.Corruption.': 'Government Corruption',
    'Perceptions of corruption': 'Government Corruption',
    'Happiness.Score': 'Happiness Score',
    'Score': 'Happiness Score',
    'Freedom to make life choices': 'Freedom'
}


dataframes = [(df15, 2015), (df16, 2016), (df17, 2017), (df18, 2018), (df19, 2019)]

for df, year in dataframes:
    df.rename(columns=mapping, inplace=True)
    df['Year'] = year

columns_15 = set(df15.columns)
columns_16 = set(df16.columns)
columns_17 = set(df17.columns)
columns_18 = set(df18.columns)
columns_19 = set(df19.columns)

all_columns = [columns_15, columns_16, columns_17, columns_18, columns_19]

shared_columns = set.intersection(*all_columns)
shared_columns = list(shared_columns)

df15_common = df15[shared_columns]
df16_common = df16[shared_columns]
df17_common = df17[shared_columns]
df18_common = df18[shared_columns]
df19_common = df19[shared_columns]

merged_df = pd.concat([df15_common, df16_common, df17_common, df18_common, df19_common], axis=0)

merged_df.reset_index(drop=True, inplace=True)
merged_df = merged_df.dropna()
merged_df.to_csv("../Data/clean/merged.csv", index=False) #Merge normal



#Para el Merge con dummies

merged_df_with_dummies = pd.get_dummies(merged_df, columns=['Year'], drop_first=False)

regions = {
    'Europe': ['Switzerland', 'Iceland', 'Denmark', 'Norway', 'Finland', 'Netherlands', 'Sweden', 'Austria', 
               'Luxembourg', 'Ireland', 'Belgium', 'United Kingdom', 'Germany', 'France', 'Czech Republic', 
               'Italy', 'Poland', 'Russia', 'Portugal', 'Spain', 'Croatia', 'Slovenia', 'Romania', 'Serbia', 
               'Ukraine', 'Estonia', 'Latvia', 'Lithuania', 'Albania', 'Bosnia and Herzegovina', 'Moldova', 
               'Kosovo', 'Cyprus', 'Greece', 'Hungary', 'Bulgaria', 'Slovakia', 'Norway', 'Malta', 'Finland'],
    
    'Americas': ['United States', 'Canada', 'Mexico', 'Brazil', 'Argentina', 'Chile', 'Colombia', 'Peru', 
                 'Uruguay', 'Venezuela', 'Ecuador', 'Panama', 'Costa Rica', 'Puerto Rico', 'Jamaica', 'Haiti', 
                 'Belize', 'Trinidad and Tobago', 'Guyana', 'Barbados'],
    
    'Asia': ['Israel', 'Singapore', 'Japan', 'South Korea', 'China', 'India', 'Indonesia', 'Vietnam', 'Thailand', 
             'Malaysia', 'Philippines', 'Bangladesh', 'Myanmar', 'Sri Lanka', 'Nepal', 'Taiwan', 'Mongolia', 
             'Kazakhstan', 'Kyrgyzstan', 'Uzbekistan', 'Turkmenistan', 'Tajikistan'],
    
    'Africa': ['South Africa', 'Nigeria', 'Kenya', 'Egypt', 'Ghana', 'Uganda', 'Tanzania', 'Zimbabwe', 'Liberia', 
               'Algeria', 'Morocco', 'Angola', 'Mozambique', 'Mauritius', 'Malawi', 'Zambia', 'Cameroon', 'Senegal', 
               'Ivory Coast', 'Mali', 'Burkina Faso', 'Rwanda', 'Benin', 'Togo', 'Mauritania', 'Ethiopia', 'Somalia', 
               'Sierra Leone', 'Sudan', 'Chad', 'Congo', 'Gabon', 'Togo', 'Botswana', 'Tunisia'],
    
    'Oceania': ['Australia', 'New Zealand', 'Fiji', 'Papua New Guinea', 'Samoa', 'Vanuatu'],
    
    'Middle East': ['United Arab Emirates', 'Oman', 'Qatar', 'Saudi Arabia', 'Bahrain', 'Lebanon', 'Jordan', 
                    'Kuwait', 'Iraq', 'Syria', 'Palestinian Territories', 'Yemen']
}

country_to_region = {country: region for region, countries in regions.items() for country in countries}

merged_df_with_dummies['Region'] = merged_df_with_dummies['Country'].map(country_to_region)

region_dummies = pd.get_dummies(merged_df_with_dummies['Region'], prefix='Region')

merged_df_with_dummies = pd.concat([merged_df_with_dummies, region_dummies], axis=1)

merged_df_with_dummies.to_csv("../Data/clean/merged_df_with_dummies.csv", index=False) #Merge con dummies