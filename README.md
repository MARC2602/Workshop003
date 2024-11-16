# ETL Workshop 003 - Machine learning and Data streaming


## Project Context

This project aims to predict the happiness index across different countries using a regression model and store the data through data streaming to a database. The data is contained in five CSV files that include relevant information about various factors that could influence people's happiness in each country.


# Structure

```bash
Workshop003
├── Data
│   ├── clean
│   └── raw
│       ├── 2015.csv
│       ├── 2016.csv
│       ├── 2017.csv
│       ├── 2018.csv
│       └── 2019.csv
├── src
│   ├── EDA
│   │   └── generalEDA.ipynb
│   ├── kafka
│   │   ├── consumer.py
│   │   └── producer.py
│   ├── dashboard.py
│   ├── docker-compose.yml
│   ├── feature_selection.py
│   ├── merge.py
│   ├── model_training.py
│   ├── random_forest_model.pkl
├── .gitignore
├── README.md
├── requirements.txt
└── requirementsubuntu.txt
```
## Tools Used
- **Python**: Used for creating scripts to upload data to the database and process information in real-time.
- **Jupyter**: Jupyter Notebooks were used for Exploratory Data Analysis (EDA), enabling data cleaning, transformation, and visualization to identify patterns and insights.
- **Ubuntu**: The project was executed on an Ubuntu virtual machine, leveraging the Linux environment for tools like Docker and Kafka, and addressing compatibility issues with certain processes on my local machine.
- **psycopg2**: A Python library for connecting to the PostgreSQL database, allowing efficient and secure data querying and updating.
- **Git and GitHub**: Git was used for version control to track code changes, and GitHub served as the central repository.
- **Pandas**: A key Python library for data manipulation and analysis, used extensively for cleaning, transforming, and analyzing large datasets.
- **PostgreSQL**: The relational database used for storing processed data, known for its robustness and scalability.
- **Apache Kafka**: Utilized for data streaming, sending real-time updates to the Looker dashboard.
- **Docker**: Employed to containerize Kafka, ZooKeeper, and PostgreSQL services.
- **scikit-learn (sklearn)**: Used for training and evaluating machine learning models for predictions based on processed data.
- **Streamlit**: A framework for developing a live dashboard, providing real-time data visualization dynamically updated via Kafka and PostgreSQL.

---

## Installation

## Cloning the Repository

To get started, clone the repository using the following command:

```bash
git clone https://github.com/MARC2602/Workshop003
```

### Virtual Environment Setup
To execute the EDA and Python scripts, you need to create a virtual environment (e.g., using `venv`). Install the required dependencies using the following commands:
- **For Windows**:  
  ```bash
  pip install -r requirements.txt

- **For Linux**:  
  ```bash
  pip install -r requirementsubuntu.txt
---


# Exploratory Data Analysis (EDA)

The EDA process was conducted to analyze the given datasets. The EDA notebook is located in the `src/EDA` folder, along with related Python scripts (`merge.py`, `features.py`, and `model_training.py`). Key steps include:

## Initial Dataset Analysis

### Description of each dataset and their shared columns:
- **Country/Region**
- **Rank (Happiness)** - [Invalid for modeling]
- **Happiness Score** - (Target variable)
- **GDP per Capita** - (Economy)
- **Life Expectancy** - (Health)
- **Government Corruption** - (Trust)
- **Generosity**
- **Freedom**

## Dataset Merge
- Standardized column names across datasets.
- Added a **Year** column based on the dataset source.
- Merged datasets and removed rows with null values

## Dummies Creation

- **Year**: Converted to dummy variables.
- **Region**: Generated via mapping from Country.

The processed dataset (`merged_df_with_dummies`) was used to compute a detailed correlation matrix and select features for model training.


# Machine Learning Models

The processed dataset was split into training (70%) and testing (30%) sets. The following models were evaluated:

- **Linear Regression**: Assumes linear relationships; fast and interpretable but limited for non-linear data.
- **Random Forest**: Ensemble model combining multiple decision trees; robust for complex, non-linear datasets.
- **Ridge Regression**: Linear regression with L2 regularization to reduce overfitting.
- **SVR (Support Vector Regressor)**: Optimizes points within a margin; effective for non-linear data but computationally expensive.
- **Gradient Boosting**: Sequentially improves weak models; sensitive to overfitting if not tuned.
- **AdaBoost Regressor**: Focuses on harder-to-predict points using weighted trees; less robust to noise.

## Best Model

The **Random Forest** model was selected for its highest R² score [0.84] and lowest MSE [0.20], making it the most representative and best-performing model.

The trained model is saved automatically as a `.pkl` file.
---
### Notes

While individual Python scripts (merge.py, features.py, and model_training.py) can execute specific processes, the Jupyter Notebook provides a more comprehensive, documented workflow.
- Make sure you run all the python codes (And have all the .csv files) before start with kafka/docker part.
---

# Docker

If Docker is not installed, you can install it using the following command:

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

To bring up the containers with docker-compose, I required an Ubuntu 22.04 Box in Vagrant (my Windows system got damaged from trying to use Docker locally). The Vagrantfile is as follows:

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  if Vagrant.has_plugin? "vagrant-vbguest"
    config.vbguest.no_install = true
    config.vbguest.auto_update = false
    config.vbguest.no_remote = true
  end
  config.vm.define :clienteUbuntu do |clienteUbuntu|
    clienteUbuntu.vm.box = "bento/ubuntu-22.04"
    clienteUbuntu.vm.network :private_network, ip: "192.168.100.2"
    clienteUbuntu.vm.hostname = "clienteUbuntu"
  end
  config.vm.define :servidorUbuntu do |servidorUbuntu|
    servidorUbuntu.vm.box = "bento/ubuntu-22.04"
    servidorUbuntu.vm.network :private_network, ip: "192.168.100.3"
    servidorUbuntu.vm.hostname = "servidorUbuntu"
  end
end
```

# Setting up the Environment

In this virtual machine, Docker and Docker Compose are already installed.

1. Clone or copy the repository inside the virtual machine.
2. Navigate to the `src` folder in the repository.
3. Run the following command to start the containers:

    ```bash
    docker-compose up -d
    ```

This command will start the containers for **Kafka**, **ZooKeeper**, and **PostgreSQL**. Kafka is configured to automatically create the necessary topics, and you can proceed to data streaming.

---

# Kafka (Data Streaming)

For data streaming, follow these steps:

### 1. Start the Consumer

1. Navigate to the `src/kafka/` folder.
2. Run the **consumer** script:

    ```bash
    python consumer.py
    ```

    The consumer is configured to run on **localhost** (Windows), but it connects to the virtual machine's IP to access the services. If the containers are running locally, you can replace the parameter with **"localhost"**. Otherwise, use the host's **IP address**.

    The consumer will:
    - Connect to the database.
    - Load the model.
    - Listen to the **happiness_topic**.
    - Be ready to store predictions in the database.

### 2. Start the Producer

1. After the consumer is running correctly, start the **producer** script.

    ```bash
    python producer.py
    ```

    The producer is configured to run from the **virtual machine (Ubuntu)**, so it uses **localhost**. If the producer is run from a different host, change this parameter to the host where the containers are running.

    The producer will:
    - Load the features (make sure the dataset of features is available if you're using a virtual machine).
    - Send data to the **happiness_topic** with a 1-second delay.

### 3. Logs

After running the scripts:
- **Consumer logs** will show how the data is being saved in the database.
- **Producer logs** will show how the data is being sent to Kafka.

With everything running, data will be streamed and processed, and logs will provide real-time feedback on the system's performance.


---
## Real-time Dashboard

Once the producer and consumer are running, the predictions generated by the model can be visualized graphically. To do this, you need to run `dashboard.py`.

It is connected in the same way as the consumer to the virtual machine's IP. It is designed to be executed on Windows. When run, a browser tab will open, presenting the Streamlit dashboard:
