# nodered-container/Dockerfile

# Use the official Node-RED image as the base
FROM nodered/node-red:latest

# Switch to the root user to install system dependencies
USER root

# Install Python and other build tools required for node-gyp and snowflake-sdk
RUN apk add --no-cache python3 make g++

# Switch back to the node-red user
USER node-red

# Copy the package.json for the main Node-RED environment
COPY package.json .

# Install the Snowflake SDK for Node.js
RUN npm install

# Copy the custom nodes and their package.json into the data directory
COPY --chown=node-red:node-red ./data/nodes/ /data/nodes/

# Go to the custom nodes directory and install their dependencies
RUN cd /data/nodes/node-red-contrib-snowflake && npm install

# Copy the custom settings file
COPY settings.js /data/settings.js

