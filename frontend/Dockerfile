# Use an existing node alpine image as a base image.
FROM node:18-alpine
 
# Set the working directory.
WORKDIR /app
 
# Copy the package.json file.
COPY package.json .
 
# Install application dependencies.
RUN npm install
RUN npm install -g serve
 
# Copy the rest of the application files.
COPY . .
 
# Expose the port.
EXPOSE 3000
 
# Run the application.
# CMD ["npm", "start"]