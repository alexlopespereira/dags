"""
TestPipe
DAG auto-generated by Astro Cloud IDE.
"""

from airflow.decorators import dag
from astro import sql as aql
import pandas as pd
import pendulum

import requests
import pandas as pd
import json
from airflow.providers.postgres.hooks.postgres import PostgresHook



@aql.dataframe(task_id="load")
def load_func():
    from airflow.operators.python import get_current_context
    
    context = get_current_context()
    start_date = context['dag'].start_date
    print(f"DAG start date: {start_date}")
    
    #### Extract
    url = "https://github.com/alexlopespereira/astro-dags/raw/refs/heads/main/data/pib_municipios.csv"
    response = requests.get(url)
    df = pd.read_csv(pd.io.common.StringIO(response.text), sep=';')
    
    #### Transform
    pivoted_data = df.melt(id_vars=["Cód.", "Município"],
        value_vars=["2007", "2009", "2011", "2013", "2015", "2017"],
        var_name="ano", value_name="populacao")
    
    # Rename columns to align with the specified format
    pivoted_data.rename(columns={"Cód.": "Codigo", "Município": "Municipio"}, inplace=True)
    
    #### Load
    pg_hook = PostgresHook(postgres_conn_id='postgres')
    engine = pg_hook.get_sqlalchemy_engine()
    pivoted_data.to_sql('pib_municipios', con=engine, if_exists='replace', index=False)

default_args={
    "owner": "Alex Lopes,Open in Cloud IDE",
}

@dag(
    default_args=default_args,
    schedule="0 0 * * *",
    start_date=pendulum.from_format("2024-11-29", "YYYY-MM-DD").in_tz("UTC"),
    catchup=False,
    owner_links={
        "Alex Lopes": "mailto:alexlopespereira@gmail.com",
        "Open in Cloud IDE": "https://cloud.astronomer.io/cm3webulw15k701npm2uhu77t/cloud-ide/cm42rbvn10lqk01nlco70l0b8/cm42rceca0m1k01o6cqzaya7p",
    },
)
def TestPipe():
    load = load_func()

dag_obj = TestPipe()
