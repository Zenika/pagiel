const express = require("express");
const dotenv = require("dotenv");
const { execFile } = require("child_process");

dotenv.config({ path: "./config/config.env" });

const app = express();

app.use(express.json());

app.post("/start", (req, res) => {
  const options = req.body;
  let scriptArgs = [];

  if (options.disablePowerAPI) {
    scriptArgs.push("-P");
  }

  if (options.disableGreenItAnalysis) {
    scriptArgs.push("-G");
  }

  if (options.disableSitespeed) {
    scriptArgs.push("-S");
  }

  if (options.disableYellowLabTools) {
    scriptArgs.push("-Y");
  }

  if (options.disableReportGeneration) {
    scriptArgs.push("-R");
  }

  if (options.disableRobotFramework) {
    scriptArgs.push("-F");
  }

  if (options.dockerMode === "image") {
    scriptArgs.push("-d");
    scriptArgs.push("--docker-image");
    scriptArgs.push(options.dockerImage);
    scriptArgs.push("--docker-port");
    scriptArgs.push(options.dockerPort || "80");
    scriptArgs.push("--docker-front-container");
    scriptArgs.push(options.dockerFrontContainer || "test-container");
  } else if (options.dockerMode === "compose") {
    scriptArgs.push("-D");
    scriptArgs.push("--docker-compose-file");
    scriptArgs.push(options.dockerComposeFile);
  }
  console.log("Pagiel is launched");
  console.log("Requête: ../pagiel.sh", ...scriptArgs);
  res.status(200).send("Pagiel is launched");

  execFile("bash", ["../pagiel.sh", ...scriptArgs], (error, stdout, stderr) => {
    console.log(`Script output: ${stdout}`);

    if (error) {
      console.error(`Error executing script: ${error}`);
      return res
        .status(500)
        .send("An error occurred while executing the script");
    }
  });
});

const PORT = process.env.PORT || 5005;
const server = app.listen(PORT, () => {
  console.log(`server is running in ${process.env.NODE_ENV} mode on ${PORT}`);
});

process.on("unhandledRejection", (err, promise) => {
  console.log(`Error', ${err.message}`);
  server.close(() => process.exit(1));
});
