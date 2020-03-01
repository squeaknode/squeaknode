FROM mhart/alpine-node:latest AS builder
WORKDIR /app
COPY ./frontend/squeakclient-frontend .
RUN npm install
RUN yarn run build

FROM mhart/alpine-node
RUN yarn global add serve
WORKDIR /app
COPY --from=builder /app/build .
CMD ["serve", "-p", "80", "-s", "."]
