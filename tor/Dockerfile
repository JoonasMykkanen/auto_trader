# Select most lightweight possible base image
FROM alpine:3.19

# Get tor and copy configuration
RUN apk add --no-cache tor
COPY ./tools/torrc /etc/tor/torrc

RUN addgroup -S user && adduser -S user -G user
USER user

# Start process
CMD ["tor", "--hush"]
