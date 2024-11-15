import streamlit as st
import psycopg2
import pandas as pd
import time
import matplotlib.pyplot as plt

# Conectar a la base de datos PostgreSQL
def get_data_from_db():
    conn = psycopg2.connect(
        host="192.168.100.2",  # Cambia esto por la IP o nombre del host de tu base de datos
        port="5432",
        database="happinessdb",  # Cambia esto por tu nombre de base de datos
        user="myuser",  # Cambia esto por tu usuario
        password="mypassword"  # Cambia esto por tu contraseña
    )
    query = "SELECT * FROM predictions ORDER BY id DESC LIMIT 300"  # Últimos 300 registros
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Crear un título para el dashboard
st.title("Predicciones en Tiempo Real")

# Configuración del gráfico en Streamlit
st.subheader("Gráfico de Predicciones")

# Usar st.empty() para actualizar el gráfico sin duplicados
placeholder = st.empty()

# Ejecutar un bucle infinito que actualiza el gráfico cada 2-3 segundos
while True:
    df = get_data_from_db()

    # Crear gráfico (sin puntos, solo línea)
    fig, ax = plt.subplots(figsize=(16, 6))  # Haciendo el gráfico más largo horizontalmente
    ax.plot(df['id'], df['predicted_score'], linestyle='-', color='b')  # Solo línea sin puntos
    ax.set_title('Predicciones de Felicidad')
    ax.set_xlabel('ID de Registro')
    ax.set_ylabel('Predicción')
    
    # Ajustar el tamaño del gráfico para hacerlo más ancho
    ax.set_xticks(df['id'][::10])  # Mostrar solo algunos IDs en el eje X para no sobrecargarlo
    ax.set_xticklabels(df['id'][::10], rotation=45)  # Rotar etiquetas para mejor visualización

    # Usar el placeholder para actualizar el gráfico
    placeholder.pyplot(fig)
    
    # Esperar 2-3 segundos antes de actualizar
    time.sleep(2)  # Puedes ajustar el tiempo según tus necesidades