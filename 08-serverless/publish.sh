ECR_URL = 499193102200.dkr.ecr.us-east-1.amazonaws.com
REPO_URL = ${ECR_URL}/hair-classifier-lambda
LOCAL_IMAGE = hair-classifier-lambda

docker build -t ${hair-classifier-lambda}

alias aws='"C:\Program Files\Amazon\AWSCLIV2\aws.exe"'

aws ecr get-login-password \
  --region "us-east-1" \
| docker login \
  --username AWS \
  --password-stdin ${ECR_URL}