columns_to_keep = ['GDP per Capita', 'Generosity','Government Corruption', 'Life Expectancy', 'Freedom', 'Year_2015', 'Year_2016','Year_2017','Year_2018','Year_2019',
                    'Region_Africa', 'Region_Americas',	'Region_Asia','Region_Europe','Region_Middle East',	'Region_Oceania']
features = merged_df_with_dummies[columns_to_keep]


features.to_csv("../../Data/clean/features.csv", index=False)