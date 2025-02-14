# AWS URL Shortner

Simple url-shorter using AWS DynamoDB, Lambdas, ApiGateway. This mini-project created for practising in AWS CDK (IaaC) and batter understanding its principals.

## Installation
### 1 Install AWS CDK
```
npm install -g aws-cdk
```

### 2 Install all dependencies
```
pip install --requirements requirements.txt
pip install --requirements requirements-dev.txt
```
### 3 Fill the .env.example

### 4 Deploy your code
```
cdk deploy
```

## Usage
### POST shorten/ --data {"url": "Your url"}
