
FROM python:3.8.9

# Set the working directory in the container
WORKDIR /app

# Copy the entire face_thinner_server directory to the working directory

# Entry point
COPY ./server.py    ./server.py

# Req.
COPY ./requirements.txt ./requirements.txt

# App
COPY ./app/                 ./app/

# Log
COPY ./log_config/              ./log_config/

# classification
COPY ./classification/                 ./classification/

# Install any dependencies
RUN pip install --no-cache-dir -r ./requirements.txt
# RUN apt-get update && apt-get -y install libgl1-mesa-glx libopencv-imgproc-dev
RUN apt-get update
RUN apt-get install libgl1 -y
RUN apt-get install vim

# Expose port 5502
EXPOSE 5502

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=5502

# Command to run on container start
CMD [ "python", "./server.py" ]
