from kafka import KafkaProducer
import json
import time
import pandas as pd

# Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Cargar los datos reales desde un CSV (o cualquier otra fuente de datos)
# Asegúrate de tener un archivo de datos, por ejemplo "real_data.csv"
df = pd.read_csv('../Data/clean/features.csv')  # Cambia esto por la fuente de datos real

# Simular el streaming de datos
for _, row in df.iterrows():
    data = row.to_dict()  # Convierte la fila a un diccionario
    
    # Enviar los datos al topic de Kafka
    try:
        print("Sending data to Kafka...")
        producer.send('happiness_topic', value=data)
        producer.flush()
        print("Data sent successfully.")
    except Exception as e:
        print("Error sending data:", e)
    
    # Introducir un pequeño retraso para simular el streaming
    time.sleep(1)  # Retraso de 1 segundo (puedes ajustar el tiempo)