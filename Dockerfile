# Use NodeJS base image
FROM python:3.7-stretch

# Create app directory in Docker
WORKDIR /app
COPY . .


# Install app dependencies by copying
# package.json and package-lock.json

# Install dependencies in Docker
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


# Copy app from local environment into the Docker image
ARG argAUTH0_DOMAIN
ARG argALGORITHMS
ARG argAPI_AUDIENCE
ARG argDATABASE_URL
ENV AUTH0_DOMAIN=$argAUTH0_DOMAIN
ENV ALGORITHMS=$argALGORITHMS
ENV API_AUDIENCE=$argAPI_AUDIENCE
ENV DATABASE_URL=$argDATABASE_URL

# Set the API’s port number

# Define Docker’s behavior when the image  is run
RUN chmod u+x entrypoint.sh
ENTRYPOINT ["/bin/bash","entrypoint.sh"]
