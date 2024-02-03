FROM node:16-alpine
WORKDIR /web_backend
COPY package*.json ./
COPY ./ ./
RUN npm install --save
EXPOSE 5000
CMD ["npm", "start"]
