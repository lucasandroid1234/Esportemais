FROM node:20-alpine

WORKDIR /usr/src/app

# 1. Instala dependências de compilação
RUN apk add --no-cache python3 make g++

# 2. Copia e instala dependências
COPY package.json package-lock.json ./
RUN npm install --omit=optional --legacy-peer-deps

# 3. Copia o código fonte
COPY . .

# 4. Executa o build
RUN npm run build

EXPOSE 3000
CMD ["npm", "run", "preview"]