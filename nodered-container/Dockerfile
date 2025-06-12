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
# This allows users to write custom functions that interact with Snowflake
RUN npm install

# Copy the custom settings file
COPY settings.js /data/settings.js

