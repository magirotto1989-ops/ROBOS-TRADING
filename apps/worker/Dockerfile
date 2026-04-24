FROM node:20-alpine
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json ./
COPY ../../packages/database/package.json ./packages/database/
RUN npm install --legacy-peer-deps

COPY . .
COPY ../../packages/database ./packages/database

RUN npx prisma generate --schema=./packages/database/prisma/schema.prisma
RUN npm run build

CMD ["node", "dist/index.js"]
