FROM node:latest

WORKDIR /website

COPY package*.json ./

RUN npm install

COPY frontend/ .

CMD [ "npm", "start" ]
