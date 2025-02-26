# Build stage
FROM node:18.19.0-alpine3.19 AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Runtime stage
FROM node:18.19.0-alpine3.19

WORKDIR /app

# Install serve to run the built application
RUN npm install -g serve

# Copy the built application from builder stage
COPY --from=builder /app/build ./build

# Expose port
EXPOSE 3001

# Start the application with single-page application support
CMD ["serve", "-s", "build", "-l", "3001", "--single"]