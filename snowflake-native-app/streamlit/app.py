# streamlit/app.py
# This is the Python code for the Streamlit user interface.

import streamlit as st

# --- Page Configuration ---
# Set the page title and icon for a professional look.
st.set_page_config(
    page_title="Node-RED Launcher for Snowflake",
    page_icon="https://nodered.org/about/resources/media/node-red-icon-2.png",
    layout="centered"
)

# --- Main Application UI ---

# Header Section
st.image("https://nodered.org/about/resources/media/node-red-icon-2.png", width=80)
st.title("Node-RED for Snowflake")
st.write("""
Welcome to Node-RED on Snowflake, powered by Snowpark Container Services.
This application provides a one-click launcher for your private, secure Node-RED instance running directly within your Snowflake account.
""")

st.markdown("---")

# Launcher Section
st.header("🚀 Launch Node-RED")
st.write("Click the button below to open the Node-RED editor in a new tab. Your instance is ready and waiting.")

# IMPORTANT: In a real application, this URL would be dynamically retrieved
# from the Snowpark Container Service endpoint.
# For this example, we are using a placeholder.
NODE_RED_URL = "http://<your-snowflake-service-endpoint-url>:1880"

# The launch button is a call-to-action link.
st.link_button("Open Node-RED Editor", NODE_RED_URL, type="primary")

st.info(f"**Note:** Your Node-RED instance is available at: `{NODE_RED_URL}`")


st.markdown("---")

# Documentation / Getting Started Section
st.header("📚 Getting Started with Snowflake Nodes")
st.write("Your Node-RED instance comes pre-installed with custom nodes to interact with your Snowflake data.")

with st.expander("Connection Configuration"):
    st.write("""
    1.  In the Node-RED editor, double-click on any Snowflake node (`snowflake-in`, `snowflake-out`, `snowflake-exec`).
    2.  Click the pencil icon next to the "Connection" field to add a new connection.
    3.  Fill in your Snowflake connection details:
        - **Account:** Your Snowflake account locator (e.g., `xy12345.east-us-2.azure`).
        - **Username:** Your Snowflake username.
        - **Password:** Your Snowflake password.
        - **Warehouse, Database, Schema:** The compute and data context you want Node-RED to use.
    4.  Click "Add" to save the connection. This connection can now be reused across all your Snowflake nodes.
    """)

with st.expander("Using the `snowflake-in` Node"):
    st.write("""
    This node queries data *from* Snowflake.
    - **Purpose:** Execute a `SELECT` statement and pass the results to the next node in your flow.
    - **Usage:**
        - Drag the `snowflake-in` node onto the canvas.
        - Double-click to configure it.
        - Write your SQL query in the editor.
        - Connect its output to a `debug` node to see the results.
    - **Output:** The `msg.payload` will contain an array of objects, where each object represents a row from your query result.
    """)
    st.code("SELECT * FROM my_table WHERE last_updated > CURRENT_DATE();", language="sql")


with st.expander("Using the `snowflake-out` Node"):
    st.write("""
    This node writes data *to* Snowflake.
    - **Purpose:** Insert data from a flow into a specified Snowflake table.
    - **Usage:**
        - The node expects `msg.payload` to be an object or an array of objects.
        - The keys of the object(s) must match the column names in your target table.
        - Configure the node with the target table name.
    - **Example `msg.payload`:**
    """)
    st.code("""
[
    {"ID": 1, "NAME": "Sensor A", "VALUE": 98.6},
    {"ID": 2, "NAME": "Sensor B", "VALUE": 102.1}
]
    """, language="json")

st.markdown("---")
st.write("Happy Flowing!")

```markdown
# README.md

## Node-RED for Snowflake Native App

This Snowflake Native App provides a launcher and management interface for a Node-RED instance running within Snowpark Container Services.

### Overview

* **Launcher UI:** A simple Streamlit interface to launch the Node-RED editor.
* **Custom Nodes:** The Node-RED instance is pre-packaged with custom nodes for seamless integration with Snowflake.
* **Secure:** Everything runs inside your Snowflake account, ensuring your data never leaves your security boundary.

### Installation

1.  Install the app from the Snowflake Marketplace.
2.  Grant the `app_public` role to the Snowflake users who need access.
3.  Open the app in Snowsight to launch Node-RED.