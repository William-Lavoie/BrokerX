# Dockerfile (dev)

FROM node:18

WORKDIR /app

# Copy only package files to install dependencies
COPY package*.json ./

RUN npm install

# DO NOT copy the rest of the app for dev – it will be mounted as a volume

# Start Next.js dev server
CMD ["npm", "run", "dev"]
