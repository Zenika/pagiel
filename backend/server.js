const express = require("express");
const dotenv = require("dotenv");
const { execFile } = require("child_process");

//Load env vars
dotenv.config({ path: "./config/config.env" });

//Route files
const app = express();

//Body Parser
app.use(express.json());

app.get("/start", (req, res) => {
  execFile("bash", ["../pagiel.sh"], (error, stdout, stderr) => {
    console.log(`Script output: ${stdout}`);

    if (error) {
      console.error(`Error executing script: ${error}`);
      return res
        .status(500)
        .send("An error occurred while executing the script");
    }

    res.send("Script execution completed");
  });
});

const PORT = process.env.PORT || 5001;
const server = app.listen(PORT, () => {
  console.log(`server is running in ${process.env.NODE_ENV} mode on ${PORT}`);
});
// Handle unhandled promise rejections
process.on("unhandledRejection", (err, promise) => {
  console.log(`Error', ${err.message}`);
  //Close Server & exit process
  server.close(() => process.exit(1));
});
