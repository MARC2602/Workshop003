from kafka import KafkaProducer
import json
import time

# Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Datos de ejemplo a enviar
data = {'GDP per Capita': 1.39651, 'Life Expectancy': 0.94143, 'Freedom': 0.66557}

try:
    print("Sending data to Kafka...")
    producer.send('happiness_topic', value=data)
    producer.flush()
    print("Data sent successfully.")
except Exception as e:
    print("Error sending data:", e)
