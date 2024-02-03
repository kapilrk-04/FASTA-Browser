FROM node:16-alpine
WORKDIR /website
COPY package*.json ./
COPY ./ ./
RUN npm install --save
EXPOSE 5000
CMD ["npm", "start"]