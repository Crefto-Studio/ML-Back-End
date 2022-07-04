# Set base image (host OS)
FROM tensorflow/tensorflow

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install boto3
# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY api.py Code.py helper.py ./

# Specify the command to run on container start
CMD [ "python", "./api.py" ]
