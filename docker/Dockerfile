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

# 3. Install your custom Snowflake nodes package from NPM
# This single command replaces the ARG/COPY steps. It pulls your package
# from the npm registry and installs it, along with its dependencies (like snowflake-sdk).
RUN npm install --global --unsafe-perm @marianraphael/node-red-contrib-snowflake

# 6. Switch back to the non-root 'node-red' user
# It's a security best practice to run the application as a non-root user.
USER node-red