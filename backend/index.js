const express = require("express");
const cors = require("cors");
const yaml = require("js-yaml");
const fs = require("fs");

const app = express();
app.use(express.json());
app.use(cors());

const port = 5000;

app.post("/process-url", (req, res) => {
  const webPages = req.body;
  const data = [];
  webPages.forEach((webPage) => {
    data.push({
      url: webPage.url,
      name: webPage.name,
      require: {
        eco: {
          ecoindex: {
            ">=": 80,
          },
        },
        images: {
          lazyLoadableImagesBelowTheFold: {
            "==": 0,
          },
        },
        DOM: {
          DOMelementMaxDepth: {
            "<=": 20,
          },
        },
      },
    });
  });

  const yamlData = yaml.dump(data);
  const yamlDataFormatted = yamlData.replaceAll("<=", "'<='");
  const filePath = "./urls.yaml";
  fs.writeFileSync(filePath, yamlDataFormatted);
  res.status(200).json({ message: "Data received successfully" });
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
