from kafka import KafkaConsumer
import json
import joblib
import pandas as pd
import psycopg2

print("Starting consumer...")

# Configurar la conexión a PostgreSQL
try:
    conn = psycopg2.connect(
        host="192.168.100.2",
        port="5432",
        database="happinessdb",
        user="myuser",
        password="mypassword"
    )
    cursor = conn.cursor()
    print("Connected to PostgreSQL database.")
except Exception as e:
    print("Failed to connect to PostgreSQL:", e)
    exit(1)

# Crear la tabla de predicciones si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id SERIAL PRIMARY KEY,
        feature_data JSONB,
        predicted_score REAL
    )
''')
conn.commit()

# Cargar el modelo entrenado
model = joblib.load('random_forest_model.pkl')
print("Model loaded successfully.")

# Configurar el consumidor de Kafka
consumer = KafkaConsumer(
    'happiness_topic',
    bootstrap_servers=['192.168.100.2:9092'],
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)
print("Connected to Kafka topic 'happiness_topic'.")

for message in consumer:
    data = message.value
    print(f"Received data: {data}")

    # Preparar los datos para la predicción
    features = pd.DataFrame([data]).values  # Convierte el diccionario en DataFrame
    prediction = model.predict(features)[0]

    # Convertir la predicción a float (si es necesario)
    prediction = float(prediction)

    # Guardar la predicción en la base de datos PostgreSQL
    cursor.execute(
        "INSERT INTO predictions (feature_data, predicted_score) VALUES (%s, %s)",
        (json.dumps(data), prediction)
    )
    conn.commit()
    print(f"Stored prediction: {prediction} for data: {data}")

conn.close()
