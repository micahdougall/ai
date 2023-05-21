import os

# The Vertex AI Workbench Notebook product has specific requirements
IS_WORKBENCH_NOTEBOOK = os.getenv("DL_ANACONDA_HOME")
IS_USER_MANAGED_WORKBENCH_NOTEBOOK = os.path.exists(
    "/opt/deeplearning/metadata/env_version"
)

# Vertex AI Notebook requires dependencies to be installed with '--user'
USER_FLAG = ""
if IS_WORKBENCH_NOTEBOOK:
    USER_FLAG = "--user"

!pip install --upgrade --no-warn-conflicts '{USER_FLAG}' -q \
    google-cloud-pubsub==2.13.6 \
    google-api-core==2.8.2 \
    google-apitools==0.5.32 \
    plotly==5.10.0 \
    itables==1.2.0 \
    xgboost==1.6.2 \
    apache_beam==2.40.0 \
    plotly==5.10.0 \
    google-cloud-aiplatform \
    google-cloud-pipeline-components \
    google-cloud-bigquery-storage \
    kfp


# Automatically restart kernel after installs
import os

if not os.getenv("IS_TESTING"):
    import IPython

    app = IPython.Application.instance()
    app.kernel.do_shutdown(True)

import random
import string
from typing import Union

import pandas as pd
from google.cloud import bigquery

# Generate unique ID to help w/ unique naming of certain pieces
ID = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))

GCP_PROJECTS = !gcloud config get-value project
PROJECT_ID = GCP_PROJECTS[0]
BUCKET_NAME = f"{PROJECT_ID}-fraudfinder"
REGION = "us-central1"
TRAINING_DS_SIZE = 1000


# Create a Google Cloud Storage bucket and save the config data.
config = f"""
BUCKET_NAME          = \"{BUCKET_NAME}\"
PROJECT              = \"{PROJECT_ID}\"
REGION               = \"{REGION}\"
ID                   = \"{ID}\"
FEATURESTORE_ID      = \"fraudfinder_{ID}\"
MODEL_NAME           = \"ff_model\"
ENDPOINT_NAME        = \"ff_model_endpoint\"
TRAINING_DS_SIZE     = \"{TRAINING_DS_SIZE}\"
"""

!gsutil mb -l {REGION} gs://{BUCKET_NAME}

!echo '{config}' | gsutil cp - gs://{BUCKET_NAME}/config/notebook_env.py


# Wrapper to use BigQuery client to run query/job, return job ID or result as DF
def run_bq_query(sql: str) -> Union[str, pd.DataFrame]:
    """
    Run a BigQuery query and return the job ID or result as a DataFrame
    Args:
        sql: SQL query, as a string, to execute in BigQuery
    Returns:
        df: DataFrame of results from query,  or error, if any
    """

    bq_client = bigquery.Client()

    # Try dry run before executing query to catch any errors
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    bq_client.query(sql, job_config=job_config)

    # If dry run succeeds without errors, proceed to run query
    job_config = bigquery.QueryJobConfig()
    client_result = bq_client.query(sql, job_config=job_config)

    job_id = client_result.job_id

    # Wait for query/job to finish running. then get & return data frame
    df = client_result.result().to_arrow().to_pandas()
    print(f"Finished job_id: {job_id}")
    return df


run_bq_query(
    """
SELECT
  *
FROM
  tx.tx
LIMIT 5
"""
)



def read_from_sub(project_id, subscription_name, messages=10):
    """
    Read messages from a Pub/Sub subscription
    Args:
        project_id: project ID
        subscription_name: the name of a Pub/Sub subscription in your project
        messages: number of messages to read
    Returns:
        msg_data: list of messages in your Pub/Sub subscription as a Python dictionary
    """
    
    import ast

    from google.api_core import retry
    from google.cloud import pubsub_v1

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        # The subscriber pulls a specific number of messages. The actual
        # number of messages pulled may be smaller than max_messages.
        response = subscriber.pull(
            subscription=subscription_path,
            max_messages=messages,
            retry=retry.Retry(deadline=300),
        )

        if len(response.received_messages) == 0:
            print("no messages")
            return

        ack_ids = []
        msg_data = []
        for received_message in response.received_messages:
            msg = ast.literal_eval(received_message.message.data.decode("utf-8"))
            msg_data.append(msg)
            ack_ids.append(received_message.ack_id)

        # Acknowledges the received messages so they will not be sent again.
        subscriber.acknowledge(subscription=subscription_path, ack_ids=ack_ids)

        print(
            f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
        )

        return msg_data



messages_tx = read_from_sub(
    project_id=PROJECT_ID, subscription_name="ff-tx-sub", messages=2
)

messages_tx