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

# 5. Copy Custom Node Files
# Now, we will copy the HTML (node editor UI) and JS (node logic) files for our
# custom Snowflake nodes into the container.
COPY snowflake-nodes/ /data/nodes/snowflake-nodes/

# 6. Install Node Dependencies for Custom Nodes
# If our custom nodes had their own package.json, we would run 'npm install' here.
# For this example, our nodes only rely on the globally installed snowflake-sdk.

# 7. Switch back to the non-root 'node-red' user
# It's a security best practice to run the application as a non-root user.
USER node-red
```javascript
// snowflake-nodes/snowflake-in.js
// This file contains the server-side logic for the "snowflake-in" node.

module.exports = function(RED) {
    "use strict";
    const snowflake = require('snowflake-sdk');

    function SnowflakeInNode(config) {
        RED.nodes.createNode(this, config);
        this.connection = RED.nodes.getNode(config.connection);
        var node = this;

        // Listen for input messages
        node.on('input', function(msg, send, done) {
            // Retrieve connection details from the config node
            if (!node.connection) {
                node.error("Snowflake connection not configured", msg);
                if (done) { done(); }
                return;
            }

            const conn = snowflake.createConnection({
                account: node.connection.account,
                username: node.connection.username,
                password: node.connection.password,
                warehouse: node.connection.warehouse,
                database: node.connection.database,
                schema: node.connection.schema
            });

            // Connect to Snowflake
            conn.connect(function(err, conn) {
                if (err) {
                    node.error('Unable to connect to Snowflake: ' + err.message, msg);
                    if (done) { done(); }
                    return;
                }

                // Use the query from the node's configuration, or from the incoming message
                const sqlText = config.query || msg.payload;

                // Execute the SQL statement
                conn.execute({
                    sqlText: sqlText,
                    complete: function(err, stmt, rows) {
                        if (err) {
                            node.error('Failed to execute statement due to the following error: ' + err.message, msg);
                        } else {
                            // On success, send the rows as the message payload
                            msg.payload = rows;
                            send(msg);
                        }

                        // Close the connection
                        conn.destroy(function(err, conn) {
                            if (err) {
                                node.error('Failed to close connection: ' + err.message, msg);
                            }
                        });

                        // Signal that the processing is complete
                        if (done) { done(); }
                    }
                });
            });
        });
    }

    // Register the node with Node-RED
    RED.nodes.registerType("snowflake-in", SnowflakeInNode);

    // This section is for the configuration node that holds the connection details
    function SnowflakeConnectionNode(n) {
        RED.nodes.createNode(this, n);
        this.account = n.account;
        this.username = n.username;
        this.password = n.password;
        this.warehouse = n.warehouse;
        this.database = n.database;
        this.schema = n.schema;
    }
    RED.nodes.registerType("snowflake-connection", SnowflakeConnectionNode, {
        credentials: {
            password: {type: "password"}
        }
    });
}
```html
<!-- snowflake-nodes/snowflake-in.html -->
<!-- This file defines the user interface for the "snowflake-in" node in the Node-RED editor. -->

<!-- Node Definition -->
<script type="text/javascript">
    RED.nodes.registerType('snowflake-in',{
        category: 'storage', // Appears in the "storage" category in the palette
        color: '#44A8DE', // A nice Snowflake blue
        defaults: {
            name: {value:""},
            connection: {value:"", type:"snowflake-connection", required: true},
            query: {value:"SELECT * FROM my_table LIMIT 10;", type:"text", required:true}
        },
        inputs:1,   // This node has one input
        outputs:1,  // This node has one output
        icon: "db.svg", // A generic database icon
        label: function() {
            return this.name || "Snowflake In";
        }
    });
</script>

<!-- Node Edit Dialog (the HTML for the configuration panel) -->
<script type="text/html" data-template-name="snowflake-in">
    <div class="form-row">
        <label for="node-input-name"><i class="fa fa-tag"></i> Name</label>
        <input type="text" id="node-input-name" placeholder="Name">
    </div>
    <div class="form-row">
        <label for="node-input-connection"><i class="fa fa-globe"></i> Connection</label>
        <input type="text" id="node-input-connection">
    </div>
    <div class="form-row" style="position: relative; min-height: 250px;">
        <label for="node-input-query" style="width: 100%"><i class="fa fa-file-text-o"></i> SQL Query</label>
        <div style="height: 250px; min-height:150px;" class="node-text-editor" id="node-input-query"></div>
    </div>
</script>

<!-- Help Text (appears in the "Help" tab in the Node-RED editor) -->
<script type="text/html" data-help-name="snowflake-in">
    <p>Executes a SQL query against a Snowflake database.</p>
    <p>This node takes a query from its configuration or from <code>msg.payload</code>.</p>
    <p>The result set (an array of objects) is returned in <code>msg.payload</code>.</p>
</script>

<!-- The following is for the shared Connection Configuration Node -->
<script type="text/javascript">
    RED.nodes.registerType('snowflake-connection',{
        category: 'config',
        defaults: {
            name: {value:"Snowflake Connection", required:true},
            account: {value:"", required:true},
            username: {value:"", required:true},
            password: {value:"", type:"password", required:true},
            warehouse: {value:"", required:true},
            database: {value:"", required:true},
            schema: {value:"", required:true}
        },
        label: function() {
            return this.name;
        }
    });
</script>

<script type="text/html" data-template-name="snowflake-connection">
    <div class="form-row">
        <label for="node-config-input-name"><i class="fa fa-tag"></i> Name</label>
        <input type="text" id="node-config-input-name" placeholder="Name">
    </div>
    <div class="form-row">
        <label for="node-config-input-account"><i class="fa fa-server"></i> Account</label>
        <input type="text" id="node-config-input-account" placeholder="your_account.snowflakecomputing.com">
    </div>
    <div class="form-row">
        <label for="node-config-input-username"><i class="fa fa-user"></i> Username</label>
        <input type="text" id="node-config-input-username" placeholder="Username">
    </div>
    <div class="form-row">
        <label for="node-config-input-password"><i class="fa fa-lock"></i> Password</label>
        <input type="password" id="node-config-input-password">
    </div>
    <div class="form-row">
        <label for="node-config-input-warehouse"><i class="fa fa-cogs"></i> Warehouse</label>
        <input type="text" id="node-config-input-warehouse" placeholder="COMPUTE_WH">
    </div>
    <div class="form-row">
        <label for="node-config-input-database"><i class="fa fa-database"></i> Database</label>
        <input type="text" id="node-config-input-database" placeholder="MY_DATABASE">
    </div>
    <div class="form-row">
        <label for="node-config-input-schema"><i class="fa fa-sitemap"></i> Schema</label>
        <input type="text" id="node-config-input-schema" placeholder="PUBLIC">
    </div>
</script>
```javascript
// snowflake-nodes/snowflake-out.js
// This file contains the server-side logic for the "snowflake-out" node.
// For brevity and focus on the core concept, this implementation is simplified.
// A production version would have more robust error handling, batching, and data type mapping.

module.exports = function(RED) {
    "use strict";
    const snowflake = require('snowflake-sdk');

    function SnowflakeOutNode(config) {
        RED.nodes.createNode(this, config);
        this.connection = RED.nodes.getNode(config.connection);
        this.table = config.table;
        var node = this;

        node.on('input', function(msg, send, done) {
            if (!node.connection) {
                node.error("Snowflake connection not configured", msg);
                if (done) { done(); }
                return;
            }

            // Ensure msg.payload is an array of objects
            let dataToInsert = Array.isArray(msg.payload) ? msg.payload : [msg.payload];
            if (dataToInsert.length === 0 || typeof dataToInsert[0] !== 'object' || dataToInsert[0] === null) {
                node.warn("msg.payload is not an array of objects or is empty. Nothing to insert.", msg);
                if (done) { done(); }
                return;
            }

            const conn = snowflake.createConnection({
                account: node.connection.account,
                username: node.connection.username,
                password: node.connection.password,
                warehouse: node.connection.warehouse,
                database: node.connection.database,
                schema: node.connection.schema
            });

            conn.connect(function(err, conn) {
                if (err) {
                    node.error('Unable to connect to Snowflake: ' + err.message, msg);
                    if (done) { done(); }
                    return;
                }

                // Construct a multi-row INSERT statement
                const columns = Object.keys(dataToInsert[0]).join(', ');
                const placeholders = dataToInsert.map(row => '(' + Object.keys(row).map(() => '?').join(', ') + ')').join(', ');
                const binds = [].concat.apply([], dataToInsert.map(row => Object.values(row)));

                const sqlText = `INSERT INTO ${node.table} (${columns}) VALUES ${placeholders}`;

                conn.execute({
                    sqlText: sqlText,
                    binds: binds,
                    complete: function(err, stmt, rows) {
                        if (err) {
                            node.error('Failed to execute INSERT statement: ' + err.message, msg);
                        } else {
                            node.log(`Successfully inserted ${rows.length} row(s).`);
                        }
                        conn.destroy();
                        if (done) { done(); }
                    }
                });
            });
        });
    }
    RED.nodes.registerType("snowflake-out", SnowflakeOutNode);
}
```html
<!-- snowflake-nodes/snowflake-out.html -->
<!-- UI definition for the "snowflake-out" node -->

<script type="text/javascript">
    RED.nodes.registerType('snowflake-out',{
        category: 'storage',
        color: '#44A8DE',
        defaults: {
            name: {value:""},
            connection: {value:"", type:"snowflake-connection", required: true},
            table: {value:"", required: true}
        },
        inputs:1,
        outputs:0, // This node has no output
        align: 'right', // Aligns to the right side of the editor
        icon: "db.svg",
        label: function() {
            return this.name || `to: ${this.table || "Snowflake"}`;
        }
    });
</script>

<script type="text/html" data-template-name="snowflake-out">
    <div class="form-row">
        <label for="node-input-name"><i class="fa fa-tag"></i> Name</label>
        <input type="text" id="node-input-name" placeholder="Name">
    </div>
    <div class="form-row">
        <label for="node-input-connection"><i class="fa fa-globe"></i> Connection</label>
        <input type="text" id="node-input-connection">
    </div>
    <div class="form-row">
        <label for="node-input-table"><i class="fa fa-table"></i> Table</label>
        <input type="text" id="node-input-table" placeholder="e.g., MY_TABLE">
    </div>
</script>

<script type="text/html" data-help-name="snowflake-out">
    <p>Inserts data into a Snowflake table.</p>
    <p>Expects <code>msg.payload</code> to be an object or an array of objects. The object keys must match the column names in the target table.</p>
</script>
```javascript
// snowflake-nodes/snowflake-exec.js
// Logic for the "snowflake-exec" node.
module.exports = function(RED) {
    "use strict";
    const snowflake = require('snowflake-sdk');

    function SnowflakeExecNode(config) {
        RED.nodes.createNode(this, config);
        this.connection = RED.nodes.getNode(config.connection);
        var node = this;

        node.on('input', function(msg, send, done) {
            if (!node.connection) {
                node.error("Snowflake connection not configured", msg);
                if (done) { done(); }
                return;
            }

            const conn = snowflake.createConnection({
                account: node.connection.account,
                username: node.connection.username,
                password: node.connection.password,
                warehouse: node.connection.warehouse,
                database: node.connection.database,
                schema: node.connection.schema
            });

            conn.connect(function(err, conn) {
                if (err) {
                    node.error('Unable to connect to Snowflake: ' + err.message, msg);
                    if (done) { done(); }
                    return;
                }

                // Use the statement from the node's config or the incoming message
                const sqlText = config.statement || msg.payload;

                conn.execute({
                    sqlText: sqlText,
                    complete: function(err, stmt, rows) {
                        if (err) {
                            node.error('Failed to execute statement: ' + err.message, msg);
                        } else {
                            msg.payload = {
                                status: "Success",
                                statement: stmt.getSqlText(),
                                rowsAffected: rows ? rows.length : 0 // Note: Not all statements return rows
                            };
                            send(msg);
                        }
                        conn.destroy();
                        if (done) { done(); }
                    }
                });
            });
        });
    }
    RED.nodes.registerType("snowflake-exec", SnowflakeExecNode);
}
```html
<!-- snowflake-nodes/snowflake-exec.html -->
<!-- UI definition for the "snowflake-exec" node -->

<script type="text/javascript">
    RED.nodes.registerType('snowflake-exec',{
        category: 'storage',
        color: '#44A8DE',
        defaults: {
            name: {value:""},
            connection: {value:"", type:"snowflake-connection", required: true},
            statement: {value:"", type:"text", required:false}
        },
        inputs:1,
        outputs:1,
        icon: "db.svg",
        label: function() {
            return this.name || "Snowflake Exec";
        }
    });
</script>

<script type="text/html" data-template-name="snowflake-exec">
    <div class="form-row">
        <label for="node-input-name"><i class="fa fa-tag"></i> Name</label>
        <input type="text" id="node-input-name" placeholder="Name">
    </div>
    <div class="form-row">
        <label for="node-input-connection"><i class="fa fa-globe"></i> Connection</label>
        <input type="text" id="node-input-connection">
    </div>
    <div class="form-row" style="position: relative; min-height: 250px;">
        <label for="node-input-statement" style="width: 100%"><i class="fa fa-file-text-o"></i> SQL Statement</label>
        <div style="height: 250px; min-height:150px;" class="node-text-editor" id="node-input-statement"></div>
    </div>
    <div class="form-row form-tips">
        <b>Tip:</b> If the SQL Statement is left blank, it will be taken from <code>msg.payload</code>.
    </div>
</script>

<script type="text/html" data-help-name="snowflake-exec">
    <p>Executes a generic SQL statement (DML, DDL) against Snowflake.</p>
    <p>This node is for statements that don't return a result set, like <code>CREATE</code>, <code>UPDATE</code>, <code>DELETE</code>, or <code>CALL</code>.</p>
    <p>Outputs a status message on success.</p>
</script>
