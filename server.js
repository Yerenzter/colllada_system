const express = require("express");
const app = express();
const APP_HOST = "127.0.0.1";
const APP_PORT = 1024;

app.use(express.static("public"));

app.listen(APP_PORT, () => {
    console.log(`Collada monitor appplication is now running at http://${APP_HOST}:${APP_PORT}...`);
})
