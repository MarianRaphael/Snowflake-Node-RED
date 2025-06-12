-- setup.sql
-- This script is executed when the application is installed.

-- Create the application role. This allows for dedicated permissions.
CREATE APPLICATION ROLE IF NOT EXISTS app_role;

-- Create a schema to hold our application's objects.
CREATE OR ALTER VERSIONED SCHEMA app_schema;
GRANT USAGE ON SCHEMA app_schema TO APPLICATION ROLE app_role;

-- Step 1: Create the individual network rules first.
CREATE OR REPLACE NETWORK RULE app_schema.allow_https_rule
  TYPE = 'HOST_PORT'
  MODE = 'EGRESS'
  VALUE_LIST = ('0.0.0.0:443');

CREATE OR REPLACE NETWORK RULE app_schema.allow_http_rule
  TYPE = 'HOST_PORT'
  MODE = 'EGRESS'
  VALUE_LIST = ('0.0.0.0:80');

-- Step 2: Create the external access integration and reference the network rules.
-- This command is corrected from 'CREATE SECURITY INTEGRATION' to the proper 'CREATE EXTERNAL ACCESS INTEGRATION'.
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION allow_all_integration
  ALLOWED_NETWORK_RULES = (app_schema.allow_https_rule, app_schema.allow_http_rule)
  ENABLED = true;

-- Create a compute pool to run our container.
-- Note: 'STANDARD_1' is a common instance family. You may need to adjust this
-- based on what's available in your Snowflake region.
CREATE COMPUTE POOL IF NOT EXISTS nodered_compute_pool
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = 'STANDARD_1';

-- Create the service that runs the Node-RED container.
-- IMPORTANT: The 'image:' path below is a placeholder. You MUST replace
-- '<database>/<schema>/<repo>' with the path to your Snowflake image repository
-- where you have pushed the Node-RED image.
CREATE SERVICE IF NOT EXISTS nodered_service
  IN COMPUTE POOL nodered_compute_pool
  FROM SPECIFICATION $$
spec:
  containers:
  - name: nodered
    image: /<database>/<schema>/<repo>/node-red:latest
    ports:
    - name: http
      port: 1880
  endpoints:
  - name: api
    port: http
    public: true
  $$
  EXTERNAL_ACCESS_INTEGRATIONS = (allow_all_integration);

-- Grant necessary privileges to the application role.
GRANT USAGE ON SERVICE nodered_service TO APPLICATION ROLE app_role;
GRANT USAGE ON COMPUTE POOL nodered_compute_pool TO APPLICATION ROLE app_role;
GRANT USAGE ON INTEGRATION allow_all_integration TO APPLICATION ROLE app_role;
GRANT USAGE ON NETWORK RULE app_schema.allow_https_rule TO APPLICATION ROLE app_role;
GRANT USAGE ON NETWORK RULE app_schema.allow_http_rule TO APPLICATION ROLE app_role;

