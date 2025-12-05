from analytics_engine import refresh_data, get_manager_kpis

df, model = refresh_data()

print(df.tail())
print(get_manager_kpis())
