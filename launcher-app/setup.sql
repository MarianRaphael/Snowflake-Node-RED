-- launcher-app/setup.sql

-- Create the application role
CREATE APPLICATION ROLE IF NOT EXISTS app_public;

-- Create the schema for the application
CREATE SCHEMA IF NOT EXISTS core;
GRANT USAGE ON SCHEMA core TO APPLICATION ROLE app_public;

-- Create a virtual warehouse for Streamlit
CREATE WAREHOUSE IF NOT EXISTS STREAMLIT_WH;
GRANT USAGE ON WAREHOUSE STREAMLIT_WH TO APPLICATION ROLE app_public;

-- Create a compute pool for Snowpark Container Services
CREATE COMPUTE POOL IF NOT EXISTS NODERED_POOL
MIN_NODES = 1
MAX_NODES = 1
INSTANCE_FAMILY = 'standard_1';

-- Create the Node-RED service
CREATE SERVICE IF NOT EXISTS core.nodered_service
  IN COMPUTE POOL NODERED_POOL
  FROM SPECIFICATION $$
  spec:
    containers:
    - name: nodered
      image: /<db_name>/<schema_name>/<image_repo>/nodered-snowflake:latest
      ports:
      - containerPort: 1880
        name: http
    endpoints:
    - name: ui
      port: 1880
      public: true
  $$;

-- Grant usage on the service to the application role
GRANT USAGE ON SERVICE core.nodered_service TO APPLICATION ROLE app_public;
