# Select most lightweight possible base image
FROM alpine:3.19

# TODO: create user to not run as ROOT

# Get tor and copy configuration
RUN apk add --no-cache tor
COPY torrc /etc/tor/torrc

# Start process
CMD ["tor"]
