// nodered-container/settings.js
module.exports = {
    // The TCP port that the Node-RED web editor runs on
    uiPort: process.env.PORT || 1880,

    // The `https` setting can be used to enable SSL connections to the editor.
    // To use this, you will need to generate your own certificates and keys.
    // See https://nodered.org/docs/user-guide/runtime/securing-node-red#generating-a-certificate
    //https: {
    //    key: require("fs").readFileSync("privatekey.pem"),
    //    cert: require("fs").readFileSync("certificate.pem")
    //},

    // By default, the Node-RED editor is not secured. This allows anyone with
    // access to the editor's IP address to deploy flows. The following property
    // can be used to secure the editor. See https://nodered.org/docs/user-guide/runtime/securing-node-red
    // for more details on the options available.
    //adminAuth: {
    //    type: "credentials",
    //    users: [{
    //        username: "admin",
    //        password: "$2a$08$zZWtXTja0fB1pzD4sHCMyOCMYz2Z6dNbM6vd.5cOiJzdsJV9BCob2",
    //        permissions: "*"
    //    }]
    //},

    // The settings for the runtime flows. This is used when the editor is disabled.
    //httpNodeAuth: {user:"user",pass:"$2a$08$zZWtXTja0fB1pzD4sHCMyOCMYz2Z6dNbM6vd.5cOiJzdsJV9BCob2"},

    // The file containing the flows. If not set, it defaults to flows.json.
    //flowFile: 'flows.json',

    // The directory containing the user data. If not set, it defaults to the
    // Node-RED installation directory.
    userDir: '/data',

    // Node-RED scans the `nodes` directory in the userDir to find local node files.
    nodesDir: '/data/nodes',

    // Any other settings from the original settings.js file can be included here,
    // or you can start with a fresh file.
    editorTheme: {
        projects: {
            enabled: false // Disable projects feature for simplicity in this context
        }
    }
}
