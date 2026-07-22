FROM node:22-alpine

WORKDIR /app

# Lockfile first so dependency layers cache when only source changes
COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# -H 0.0.0.0: accept connections from outside the container (Docker port publish)
CMD ["npm", "run", "dev", "--", "-H", "0.0.0.0", "-p", "3000"]