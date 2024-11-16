from kafka import KafkaProducer
import json
import time
import pandas as pd

# Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092', #Al correrse desde mi maquina virtual no necesito cambiarlo por la ip.
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

#Cargar features
df = pd.read_csv('../../Data/clean/features.csv')

# Streaming
for _, row in df.iterrows():
    data = row.to_dict()
    
    # Enviar los datos al topic de Kafka
    try:
        print("Sending data to Kafka...")
        producer.send('happiness_topic', value=data)
        producer.flush()
        print("Data sent successfully.")
    except Exception as e:
        print("Error sending data:", e)
    

    time.sleep(1)  # Retraso de 1 segundo (Se puede ajustar el tiempo)