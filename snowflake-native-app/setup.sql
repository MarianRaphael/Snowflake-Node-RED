```sql
-- setup.sql
-- This SQL script runs when a consumer installs your Native App.
-- Its purpose is to set up the necessary environment for the application.

-- 1. Create Application Role
-- This role will own the objects created by the application and can be granted to users
-- who need to use the app. This is a best practice for security and access control.
CREATE APPLICATION ROLE IF NOT EXISTS app_public;

-- 2. Create a versioned schema
-- Using a versioned schema allows for future upgrades without breaking the existing installation.
-- The app_public role is granted usage on this schema.
CREATE OR REPLACE VERSIONED SCHEMA app_schema;
GRANT USAGE ON SCHEMA app_schema TO APPLICATION ROLE app_public;

-- 3. Create the Streamlit application object
-- This command creates the actual Streamlit object within Snowflake, pointing to our Python code.
-- The FROM clause references the 'streamlit' directory in the application package.
-- The MAIN_FILE points to the entry point of our Streamlit app.
CREATE OR REPLACE STREAMLIT app_schema.streamlit_app
  FROM '/streamlit'
  MAIN_FILE = '/app.py';

-- 4. Grant usage on the Streamlit object to the application role
-- This allows users with the app_public role to view and interact with the Streamlit UI.
GRANT USAGE ON STREAMLIT app_schema.streamlit_app TO APPLICATION ROLE app_public;

-- Note on Snowpark Container Services:
-- In a real-world scenario, this setup script would also include the logic to:
-- 1. Create a COMPUTE POOL.
-- 2. Create a SERVICE using the Docker image we defined earlier.
-- 3. Create a FUNCTION to get the public endpoint of that service.
-- The Streamlit app would then call that function to get the URL for the "Launch" button.
-- For this example, we will use a placeholder URL in the Streamlit app.
```python