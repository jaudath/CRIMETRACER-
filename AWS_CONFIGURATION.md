# 🚀 AWS Configuration Guide for Crime Tracer

## 📋 Overview

Crime Tracer uses several AWS services to provide enhanced functionality. **All AWS services are optional** - the application works perfectly without them using local fallbacks.

### 🛠️ AWS Services Used

1. **Amazon S3** - File Storage (complaint photos, attachments)
2. **Amazon SNS** - SMS Notifications (complaint updates, alerts)
3. **Amazon CloudWatch Logs** - Centralized Logging
4. **AWS Lambda** - Background job processing (optional)

---

## 🔧 Required AWS Configuration

### 1. 🔐 AWS Credentials

#### Option A: Environment Variables (Recommended)
```bash
# Add to your .env file
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=ap-south-1
```

#### Option B: AWS CLI Configuration
```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure
```

#### Option C: IAM Roles (Production)
For production deployment on EC2, use IAM roles instead of hardcoded credentials.

### 2. 📱 Required IAM Permissions

Create an IAM user with these policies:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3FileStorage",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::crimetracer-uploads/*",
                "arn:aws:s3:::crimetracer-uploads"
            ]
        },
        {
            "Sid": "SNSMessaging",
            "Effect": "Allow",
            "Action": [
                "sns:Publish",
                "sns:GetTopicAttributes",
                "sns:CreateTopic",
                "sns:Subscribe"
            ],
            "Resource": "*"
        },
        {
            "Sid": "CloudWatchLogs",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogStreams",
                "logs:DescribeLogGroups"
            ],
            "Resource": "*"
        },
        {
            "Sid": "LambdaInvoke",
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": "arn:aws:lambda:*:*:function:crimetracer-*"
        }
    ]
}
```

---

## 🪣 Amazon S3 Setup

### Step 1: Create S3 Bucket
```bash
# Using AWS CLI
aws s3 mb s3://crimetracer-uploads --region ap-south-1
```

### Step 2: Configure Bucket Policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowApplicationAccess",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::YOUR_ACCOUNT_ID:user/crimetracer-user"
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::crimetracer-uploads/*"
        }
    ]
}
```

### Step 3: Environment Variables
```bash
# Add to .env
S3_BUCKET=crimetracer-uploads
```

### 📁 S3 File Structure
```
crimetracer-uploads/
├── complaint_files/
│   ├── photos/
│   │   ├── uuid1.jpg
│   │   └── uuid2.png
│   └── attachments/
│       ├── uuid3.pdf
│       └── uuid4.docx
└── evidence/
    └── case_123/
        ├── photo1.jpg
        └── document.pdf
```

---

## 📱 Amazon SNS Setup

### Step 1: Create SNS Topic (Optional)
```bash
# Create topic for notifications
aws sns create-topic --name crimetracer-notifications --region ap-south-1
```

### Step 2: Environment Variables
```bash
# Add to .env
SNS_TOPIC_ARN=arn:aws:sns:ap-south-1:123456789012:crimetracer-notifications
```

### 📲 SMS Features
- **Complaint Filed**: "Complaint CT-123 filed successfully. Track at: [URL]"
- **Status Updates**: "Complaint CT-123 status: Investigating"
- **Case Closed**: "Your complaint CT-123 has been resolved"
- **Victim Confirmation**: "Please confirm if CT-123 is resolved: [URL]"

### 🌏 SMS Pricing (India Region)
- Transactional SMS: ₹0.00645 per SMS
- Promotional SMS: ₹0.00581 per SMS
- **Monthly Volume**: ~₹65 for 1000 SMS

---

## 📊 CloudWatch Logs Setup

### Step 1: Log Groups (Auto-created)
The application automatically creates:
- `crimetracer-logs` - Application logs
- `crimetracer-errors` - Error logs

### Step 2: Environment Variables
```bash
# Add to .env (optional - auto-configured)
CLOUDWATCH_LOG_GROUP=crimetracer-logs
LOG_LEVEL=INFO
```

### 📈 Log Categories
- **Auth Events**: Login attempts, authentication errors
- **Complaint Events**: Filing, updates, assignments
- **Error Events**: Application errors, API failures
- **Performance**: Response times, database queries

---

## ⚡ AWS Lambda Setup (Optional)

### Step 1: Create Lambda Function
```python
# lambda_function.py
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Background job processor for Crime Tracer
    """
    try:
        job_type = event.get('job_type')
        payload = event.get('payload', {})
        
        if job_type == 'case_closed_notification':
            # Process case closure notifications
            complaint_id = payload.get('complaint_id')
            logger.info(f"Processing case closure for {complaint_id}")
            # Add your notification logic here
            
        return {
            'statusCode': 200,
            'body': json.dumps({'success': True})
        }
        
    except Exception as e:
        logger.error(f"Lambda function error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### Step 2: Deploy Lambda
```bash
# Package and deploy
zip lambda_function.zip lambda_function.py
aws lambda create-function \
  --function-name crimetracer-background-jobs \
  --runtime python3.9 \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda_function.zip \
  --region ap-south-1
```

---

## 🔧 Complete Environment Configuration

### `.env` File Example
```bash
# === AWS Configuration ===
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=ap-south-1

# S3 File Storage
S3_BUCKET=crimetracer-uploads

# SNS Messaging
SNS_TOPIC_ARN=arn:aws:sns:ap-south-1:123456789012:crimetracer-notifications

# CloudWatch Logs
CLOUDWATCH_LOG_GROUP=crimetracer-logs
LOG_LEVEL=INFO

# === Other Configuration ===
DATABASE_URL=sqlite:///crime_tracer.db
JWT_SECRET=your-super-secret-jwt-key
GEMINI_API_KEY=your-gemini-api-key

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Rate Limiting
MAX_COMPLAINTS_PER_PHONE_PER_HOUR=5
ENABLE_RATE_LIMITING=true

# File Uploads
MAX_FILE_SIZE_MB=10
MAX_ATTACHMENTS_PER_COMPLAINT=5
```

---

## 💰 Cost Estimation (Monthly)

### Small Deployment (100 complaints/month)
- **S3 Storage**: ₹1.60 (1GB storage)
- **S3 Requests**: ₹0.81 (1000 requests)
- **SNS SMS**: ₹13 (200 SMS)
- **CloudWatch Logs**: ₹3.20 (1GB logs)
- **Total**: ~₹19/month

### Medium Deployment (1000 complaints/month)
- **S3 Storage**: ₹8 (5GB storage)
- **S3 Requests**: ₹8.10 (10,000 requests)
- **SNS SMS**: ₹65 (1000 SMS)
- **CloudWatch Logs**: ₹16 (5GB logs)
- **Total**: ~₹97/month

### Large Deployment (10,000 complaints/month)
- **S3 Storage**: ₹40 (25GB storage)
- **S3 Requests**: ₹81 (100,000 requests)
- **SNS SMS**: ₹650 (10,000 SMS)
- **CloudWatch Logs**: ₹80 (25GB logs)
- **Total**: ~₹851/month

---

## 🚨 Fallback Behavior (Without AWS)

The application gracefully handles missing AWS services:

### 📁 File Storage Fallback
```python
# Without S3 → Local storage in /uploads directory
if not S3_BUCKET:
    return upload_to_local_storage(file_path, file_data)
```

### 📱 SMS Fallback
```python
# Without SNS → Mock SMS (logged for development)
if not SNS_TOPIC_ARN:
    return mock_sms_send(phone_number, message)
```

### 📊 Logging Fallback
```python
# Without CloudWatch → Local file logging
if not cloudwatch_client:
    logger.info("Using local file logging")
```

---

## 🔍 Testing AWS Configuration

### 1. Health Check Endpoint
```bash
curl http://localhost:8000/health
```

**Response**:
```json
{
  "success": true,
  "data": {
    "database": "connected",
    "aws_s3": "configured",
    "aws_sns": "configured", 
    "aws_cloudwatch": "available"
  }
}
```

### 2. Manual Testing

#### Test S3 Upload:
```python
from Backend.aws_utils import upload_to_s3
result = await upload_to_s3("test.jpg", b"test data")
print(f"Upload result: {result}")
```

#### Test SMS:
```python
from Backend.aws_utils import send_sms_notification
result = await send_sms_notification("+911234567890", "Test message")
print(f"SMS result: {result}")
```

---

## 🛡️ Security Best Practices

### 1. IAM Security
- ✅ Use least-privilege IAM policies
- ✅ Create dedicated service user
- ✅ Rotate access keys regularly
- ✅ Use IAM roles in production

### 2. S3 Security
- ✅ Keep buckets private
- ✅ Use presigned URLs for temporary access
- ✅ Enable versioning for important files
- ✅ Set up lifecycle policies

### 3. Environment Security
- ✅ Never commit `.env` files
- ✅ Use AWS Secrets Manager in production
- ✅ Enable CloudTrail for auditing
- ✅ Set up billing alerts

---

## 📞 Support & Troubleshooting

### Common Issues

#### ❌ "AWS credentials not found"
**Solution**: Add credentials to `.env` file or configure AWS CLI

#### ❌ "S3 bucket does not exist"
**Solution**: Create bucket or update `S3_BUCKET` environment variable

#### ❌ "SNS topic not found"
**Solution**: Create SNS topic or remove `SNS_TOPIC_ARN` for mock SMS

#### ❌ "Access denied" errors
**Solution**: Check IAM permissions and bucket policies

### Debug Mode
```bash
# Enable debug logging
LOG_LEVEL=DEBUG
DEBUG=true
```

### Health Check Command
```bash
# Check all AWS services
python -c "
from Backend.aws_utils import check_aws_services_health
print(check_aws_services_health())
"
```

---

## 🎯 Production Deployment Checklist

- [ ] Create production S3 bucket
- [ ] Set up proper IAM roles and policies  
- [ ] Configure SNS topic for SMS
- [ ] Set up CloudWatch log retention policies
- [ ] Enable S3 versioning and lifecycle rules
- [ ] Configure production domain for CORS
- [ ] Set up AWS CloudTrail for auditing
- [ ] Enable AWS Config for compliance
- [ ] Set up billing alerts and budgets
- [ ] Test all AWS integrations thoroughly

---

**💡 Remember**: AWS services are completely optional. The application works perfectly fine with local storage and mock SMS for development and small deployments!