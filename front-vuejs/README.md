# front-vuejs

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Run your end-to-end tests
```
npm run test:e2e
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


## Docker

Build

```shell
docker build -t zgreen/front-vuejs .

```

Run

```shell
docker run --name zgreen_vuejs_front -p 8091:8080 -d zgreen/front-vuejs
```

