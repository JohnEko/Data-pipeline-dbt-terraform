import os
import io
from io import BytesIO
import pandas as pd
import requests
import time
from google.cloud import storage
from google.cloud import bigquery


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "..\data\keys\de-projects-373304-8905dd150db9.json"


bucket_name = "de-pipelines"
project_id = "de-projects-373304"
destination_path = "de-projects-373304.production_hunt.production"
client = bigquery.Client()


def load_df():
    print("Loading")
    df = pd.read_csv("\Program Files\Docker Toolbox\docker_DE\product-hunt-prouducts-1-1-2014-to-12-31-2021.csv")
    print(df)
    return df
    

def upload_data_gcs(bucket_name, destination_path):
    print("load data")
    gcp_storage_client = storage.Client.from_service_account_json(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    bucket = gcp_storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_path)
    blob.upload_from_filename(load_df())

    print(f"Successfully loaded from {load_df()} to GCS bucket{destination_path}")


def load_bigquery():
  
    print("load to big query")
    job_config = bigquery.LoadJobConfig(
        source_format = bigquery.SourceFormat.CSV,
        allow_quoted_newlines = True,
        write_disposition = 'WRITE_TRUNCATE',
        field_delimiter =',',
        skip_leading_rows = 1,
        autodetect=True
       
    )
    data = load_df()
    
    job = client.load_table_from_dataframe(data, destination_path, job_config=job_config)
        
    print(job.result())
    
    data = client.get_table(destination_path)

    return data
    

def main():
    #load_df()
    #upload_data_gcs(bucket_name, destination_path)
    #load_bigquery()
    print("successfully loaded")


if __name__ == '__main__':
    main()