FROM    node:12-alpine

# last commit=v1.12.0
ENV     VERSION=develop
ENV     CHROMIUM_VERSION 86.0.4240.111-r0


WORKDIR /usr/src/ylt

COPY ./src/package.json .

RUN apk upgrade --update && apk --no-cache add gcc make g++ zlib-dev libjpeg-turbo-dev nasm automake autoconf libtool \
  && npm install \
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" > /etc/apk/repositories \
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
  && echo "http://dl-cdn.alpinelinux.org/alpine/v3.12/main" >> /etc/apk/repositories \
  && apk upgrade -U -a \
  && apk add \
    libjpeg-turbo-dev \
    chromium \
    ca-certificates \
    freetype \
    freetype-dev \
    harfbuzz \
    nss \
    ttf-freefont \
  && which chromium-browser && chromium-browser --no-sandbox --version &&  chown -R nobody:nogroup . \
  && rm -rf test doc

COPY ./src .

# Tell Puppeteer to skip installing Chrome. We'll be using the installed binary
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true



# Run everything after as non-privileged user.
USER nobody


# Tell phantomas where Chromium binary is and that we're in docker
ENV PHANTOMAS_CHROMIUM_EXECUTABLE /usr/bin/chromium-browser
ENV DOCKERIZED yes

# ENV DEBUG ylt:cli

ENTRYPOINT ["node", "bin/cli.js"]