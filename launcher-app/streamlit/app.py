# launcher-app/streamlit/app.py

import streamlit as st
from snowflake.snowpark.context import get_active_session

# Get the active Snowflake session
session = get_active_session()

st.set_page_config(layout="wide")

# --- Main App UI ---
st.title("🚀 Node-RED for Snowflake")
st.write(
    "Welcome! This application allows you to launch and manage a Node-RED instance "
    "directly within your Snowflake environment using Snowpark Container Services."
)

st.info(
    "**What is Node-RED?** Node-RED is a powerful open-source flow-based development "
    "tool for visual programming. You can use it to wire together hardware devices, "
    "APIs, and online services in new and interesting ways.",
    icon="ℹ️"
)

# --- Launch Control ---
col1, col2 = st.columns([1, 4])

with col1:
    # Fetch the service endpoint
    try:
        service_info = session.sql("SHOW SERVICES LIKE 'nodered_service' IN SCHEMA core").collect()
        if service_info:
            service_status_df = session.sql("CALL SYSTEM$GET_SERVICE_STATUS('core.nodered_service')").collect()
            service_status = service_status_df[0]['status'] if service_status_df else "UNKNOWN"
            
            if service_status == 'READY':
                endpoints = session.sql("SHOW ENDPOINTS IN SERVICE core.nodered_service").collect()
                if endpoints:
                    nodered_url = endpoints[0]['ingress_url']
                    st.link_button("🎉 Launch Node-RED", nodered_url, use_container_width=True)
                    st.success(f"Status: {service_status}")
                else:
                    st.error("Endpoint not found.")
                    st.warning("Status: PENDING")
            else:
                st.warning(f"Status: {service_status}")
                st.button("Launch Node-RED", disabled=True, use_container_width=True)

        else:
            st.error("Node-RED service not found. Please ensure it has been created.")
            st.button("Launch Node-RED", disabled=True, use_container_width=True)
            
    except Exception as e:
        st.error(f"Could not get service status. Error: {e}")
        st.button("Launch Node-RED", disabled=True, use_container_width=True)


with col2:
    st.write("") # Spacer

# --- Documentation Section ---
st.header("Getting Started with Custom Snowflake Nodes")
st.write(
    "Your Node-RED instance comes pre-installed with custom nodes to interact "
    "seamlessly with your Snowflake data."
)

st.subheader("❄️ snowflake-in")
st.write(
    """
    An **input node** that executes a SQL query against your Snowflake database.
    - **Usage:** Drag this node onto your canvas to start a flow.
    - **Configuration:**
        - `Name`: A display name for the node.
        - `Query`: The SQL query to execute. You can use Mustache-style `{{{payload}}}` templating.
    - **Output:** The result set of the query is passed as an array of objects in `msg.payload`.
    """
)

st.subheader("❄️ snowflake-out")
st.write(
    """
    An **output node** that writes data into a Snowflake table.
    - **Usage:** Place this node at the end of a flow.
    - **Configuration:**
        - `Name`: A display name for the node.
        - `Table`: The name of the target table (e.g., `MY_DATABASE.MY_SCHEMA.MY_TABLE`).
        - `Columns`: A comma-separated list of column names to insert into.
    - **Input:** The node expects `msg.payload` to be an object or an array of objects matching the column structure.
    """
)

st.subheader("❄️ snowflake-exec")
st.write(
    """
    A **function node** that executes any arbitrary SQL statement.
    - **Usage:** Use this node to perform DDL, DML, or call stored procedures.
    - **Configuration:**
        - `Name`: A display name for the node.
        - `Statement`: The SQL statement to execute. Can use `{{{payload}}}` templating.
    - **Input:** The `msg.payload` can be used for templating in the SQL statement.
    - **Output:** Outputs the result from the Snowflake connector on success.
    """
)
