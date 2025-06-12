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
st.header("Getting Started")
st.write(
    """
    Your Node-RED instance is a standard build. You can interact with Snowflake by:

    1.  **Using the `Function` Node:** Write Node.js code inside a `function` node. You can `require('snowflake-sdk')` to connect to and query your database. You will need to manage connection details securely using environment variables.

    2.  **Installing Nodes:** Use the "Manage Palette" feature in the Node-RED editor to install community-developed nodes for various services.
    """
)

st.subheader("Connecting to Snowflake from a `Function` Node")
st.code("""
// Inside a Function Node:

// IMPORTANT: Store credentials securely as environment variables in your service definition,
// do not hardcode them here.
const snowflake = require('snowflake-sdk');

const connection = snowflake.createConnection({
    account: process.env.SNOWFLAKE_ACCOUNT,
    username: process.env.SNOWFLAKE_USERNAME,
    password: process.env.SNOWFLAKE_PASSWORD,
    //... other parameters
});

// Your logic here...

// Return msg to pass it to the next node in the flow
return msg;
""", language="javascript")
