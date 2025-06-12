# Dockerfile for Node-RED with custom Snowflake nodes

# 1. Base Image
# We'll start with the official Node-RED image, which provides a solid foundation.
# Using a specific version is good practice for stability.
FROM nodered/node-red:3.1.0

# 2. Switch to root user to install packages
# We need root privileges to install the necessary system dependencies and Node.js packages.
USER root

# 3. Install Node.js Snowflake Driver
# This is the official SDK that allows Node.js applications to connect to Snowflake.
# The --unsafe-perm flag is sometimes needed for global installations in container environments.
RUN npm install --global --unsafe-perm snowflake-sdk

# 4. Create a directory for custom nodes
# Node-RED looks for custom nodes in the '.node-red/nodes' directory in the user's home.
# For the default 'node-red' user, this is /data/.node-red/nodes
# Note: In the official Node-RED image, the /data directory is the persistent volume
# where all user configuration, flows, and custom nodes are stored.
WORKDIR /data

# 5. Copy Custom Node Files using a Build Argument
# This makes the Dockerfile more flexible. The build command will pass the location
# of the custom nodes directory via the NODES_DIR build argument.
ARG NODES_DIR
COPY ${NODES_DIR}/ /data/nodes/custom-nodes/

# 6. Switch back to the non-root 'node-red' user
# It's a security best practice to run the application as a non-root user.
USER node-red