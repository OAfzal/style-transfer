# first building react project, using node base image
FROM node:10 as build-stage

# setting working dir inside container
WORKDIR /react-app

# required to install packages
COPY package*.json ./

# installing npm packages
RUN npm install

<<<<<<< HEAD
# copying over react source material
COPY src ./src
=======
COPY frontend/ .
>>>>>>> 3a6130ff178f81feffc9e6cb6ba18b4f0426888e

# copying over further react material
COPY public ./public

# copying over our nginx config file
COPY container_server.conf ./

# creating production build to serve through nginx
RUN npm run build

# starting second, nginx build-stage
FROM nginx:1.15

# removing default nginx config file
RUN rm /etc/nginx/conf.d/default.conf

# copying our nginx config
COPY --from=build-stage /react-app/container_server.conf /etc/nginx/conf.d/

# copying production build from last stage to serve through nginx
COPY --from=build-stage /react-app/build/ /usr/share/nginx/html

# exposing port 8080 on container
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
