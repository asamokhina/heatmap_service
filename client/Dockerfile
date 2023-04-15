FROM node:16-alpine AS builder

WORKDIR /client
COPY package.json ./
COPY package-lock.json ./
RUN npm install

COPY src /client/src
COPY public /client/public

CMD ["npm", "start"]