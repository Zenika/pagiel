FROM node:16

WORKDIR /app

COPY package.json .

RUN npm install

COPY ./src ./src

ENTRYPOINT [ "node", "src/app.js" ]