import pandas as pd

df15 = pd.read_csv("../../Data/raw/2015.csv", delimiter=',')
df16 = pd.read_csv("../../Data/raw/2016.csv", delimiter=',')
df17 = pd.read_csv("../../Data/raw/2017.csv", delimiter=',')
df18 = pd.read_csv("../../Data/raw/2018.csv", delimiter=',')
df19 = pd.read_csv("../../Data/raw/2019.csv", delimiter=',')


# Crear un diccionario de mapeo común para estandarizar nombres de columnas
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

# Crear una lista de los DataFrames y los años correspondientes
dataframes = [(df15, 2015), (df16, 2016), (df17, 2017), (df18, 2018), (df19, 2019)]

# Renombrar columnas y agregar columna Year
for df, year in dataframes:
    df.rename(columns=mapping, inplace=True)
    df['Year'] = year


# Crear un conjunto de columnas para cada DataFrame
columns_15 = set(df15.columns)
columns_16 = set(df16.columns)
columns_17 = set(df17.columns)
columns_18 = set(df18.columns)
columns_19 = set(df19.columns)

# Crear una lista de todos los conjuntos de columnas
all_columns = [columns_15, columns_16, columns_17, columns_18, columns_19]

# Calcular las columnas compartidas por todos los DataFrames (intersección)
shared_columns = set.intersection(*all_columns)
shared_columns = list(shared_columns)

# Seleccionar únicamente las columnas compartidas en cada DataFrame
df15_common = df15[shared_columns]
df16_common = df16[shared_columns]
df17_common = df17[shared_columns]
df18_common = df18[shared_columns]
df19_common = df19[shared_columns]

# Concatenar los DataFrames usando solo las columnas compartidas
merged_df = pd.concat([df15_common, df16_common, df17_common, df18_common, df19_common], axis=0)

# Reiniciar el índice del DataFrame final
merged_df.reset_index(drop=True, inplace=True)
merged_df = merged_df.dropna()
merged_df.to_csv("../../Data/clean/merged.csv", index=False)