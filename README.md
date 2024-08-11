# API server to store measurements

This repository contains a simple API server implementation using Python and [AIOHTTP](https://docs.aiohttp.org/en/stable/) library to store sensor measurements into database storage.

## Getting started

The default available measurement types can be found in the [Dockerfile](/Dockerfile). To change available measurement types, you can modify the ```ENTRYPOINT``` command.

To run the API, follow the steps below:

1. Build the docker image with the command

```
docker build -t measurements:latest .
```

2. Run the docker container with the command:

```
docker run -p 8080:8080 measurements:latest
```

To test whether the server is up and running, try to reaching it out at http://localhost:8080.