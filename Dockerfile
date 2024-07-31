# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install cron
RUN apt-get update && apt-get install -y cron

WORKDIR /usr/src/app
# Add the Python script and crontab file to the container:
COPY . /usr/src/app
# Give execution rights on the cron job and script
RUN pip install -r ./requirements.txt
# Apply the cron job
RUN crontab /usr/src/app/job.txt

# # Run the cron service and tail the cron log file
CMD ["cron", "-f"]
# CMD ["python3", "script.py"]