import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet, BayesianRidge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

merged_df_with_dummies = pd.read_csv("../Data/clean/merged_df_with_dummies.csv", delimiter=',')

X = merged_df_with_dummies[['GDP per Capita', 'Generosity','Government Corruption', 'Life Expectancy', 'Freedom', 'Year_2015', 'Year_2016','Year_2017','Year_2018','Year_2019',
                                'Region_Africa', 'Region_Americas',	'Region_Asia','Region_Europe','Region_Middle East',	'Region_Oceania']]
y = merged_df_with_dummies['Happiness Score']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(random_state=10),
    "Ridge Regression": Ridge(alpha=1.0),
    "SVR": SVR(kernel='rbf', C=1, epsilon=0.1),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
    "AdaBoost Regressor": AdaBoostRegressor(n_estimators=100, random_state=42),
}

results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    results[name] = {'MSE': mse, 'R2 Score': r2}

for model_name, metrics in results.items():
    print(f"{model_name}: MSE = {metrics['MSE']:.2f}, R2 Score = {metrics['R2 Score']:.2f}")

best_model_name = max(results, key=lambda x: results[x]['R2 Score'])
best_model = models[best_model_name]

joblib.dump(best_model, f"{best_model_name.lower().replace(' ', '_')}_model.pkl")
print(f"\nModelo elegido para guardar: {best_model_name}")
