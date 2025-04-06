FROM python:3.10-slim
LABEL authors="AdamFremund"

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Create a virtual environment and activate it
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.in

ENV PYTHONUNBUFFERED=1\
STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
STREAMLIT_SERVER_PORT=8501

ENV PATH="/app/venv/bin:$PATH"

# Expose the port used by Streamlit
EXPOSE 8501

# Start the app
CMD ["python", "main.py"]