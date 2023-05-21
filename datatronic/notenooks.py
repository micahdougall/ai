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

