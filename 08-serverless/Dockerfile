# Extend the provided Zoomcamp base image
FROM agrigorev/model-2025-hairstyle:v1

# Install required lightweight Python packages
# AWS Lambda base images use pip directly
RUN pip install requests pillow numpy onnxruntime

# Copy your lambda function code into the container's working directory
COPY lambda_func.py .

# Set the CMD to your handler function
CMD [ "lambda_func.lambda_handler" ]