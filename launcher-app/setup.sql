-- setup.sql
-- This script is executed when the application is installed.

-- Create the application role. This allows for dedicated permissions.
CREATE APPLICATION ROLE IF NOT EXISTS app_role;

-- Create a schema to hold our application's objects.
CREATE OR ALTER VERSIONED SCHEMA app_schema;

-- Create a compute pool to run our container.
-- You might need to adjust the instance_family based on your needs.
-- For a simple Node-RED instance, the smallest size is usually sufficient.
CREATE COMPUTE POOL IF NOT EXISTS nodered_compute_pool
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_XS;

-- Create a security integration to allow outbound network access from Node-RED.
-- This is crucial for Node-RED to be able to connect to external APIs and services.
CREATE SECURITY INTEGRATION IF NOT EXISTS allow_all_integration
  TYPE = EXTERNAL_ACCESS
  ENABLED = true
  ALLOWED_NETWORK_RULES = (
    (HOST = '0.0.0.0', PORT = 443),
    (HOST = '0.0.0.0', PORT = 80)
  );

-- Create the service that runs the Node-RED container.
-- We use the official Node-RED Docker image from Docker Hub.
CREATE SERVICE IF NOT EXISTS nodered_service
  IN COMPUTE POOL nodered_compute_pool
  FROM SPECIFICATION $$
spec:
  containers:
  - name: nodered
    image: /reponame/nodered/node-red:latest  # Note: You need to pull this image into a Snowflake image repository
    ports:
    - name: http
      port: 1880
  endpoints:
  - name: api
    port: http
    public: true
  $$
  EXTERNAL_ACCESS_INTEGRATIONS = (allow_all_integration);

-- Grant permissions to the application role.
GRANT USAGE ON SCHEMA app_schema TO APPLICATION ROLE app_role;
GRANT USAGE ON SERVICE nodered_service TO APPLICATION ROLE app_role;
GRANT USAGE ON COMPUTE POOL nodered_compute_pool TO APPLICATION ROLE app_role;

-- This is a placeholder for where you would grant more specific permissions.
-- For example, if you create tables or functions, you would grant usage on them here.
