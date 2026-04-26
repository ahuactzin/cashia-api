# Cashia Installation Instructions

## Step 1: Create the Server

### 1. Create your EC2 server
In the console search:
- EC2

Open the service:
- Amazon EC2

Then click:
- Launch instance

---

### 2. Basic configuration
Set these values:

**Name**
- cashia-server

**Operating system**
- Ubuntu Server 22.04 LTS  
(It is the easiest for Python)

**Instance type**
- t3.micro  
Characteristics:
- 1 vCPU
- 1 GB RAM
- Free Tier eligible

This is enough for FastAPI + small models.

---

### 3. Create the SSH key (VERY IMPORTANT)
In **Key pair** select:
- Create new key pair

Configure:
- Key pair name: cashia-key
- Key type: RSA
- Private key format: .pem

AWS will download a file:
- cashia-key.pem

⚠️ Save it very well.  
It is the only way to access the server.

---

### 4. Network configuration
In **Network settings** click **Edit**

Configure:

**Allow SSH**
- Type: SSH
- Port: 22
- Source: My IP

**Allow access to FastAPI (Create a new rule)**
- Type: Custom TCP
- Port: 8000
- Source: Anywhere

---

### 5. Disk
- 20 GB
- gp3

Free Tier allows up to 30 GB.

---

### 6. Launch server
Click:
- Launch instance

---

### 7. Get the IP
Look for:
- IPv4 public address

---

### 8. Connect from your computer

```bash
ssh -i cashia-key.pem ubuntu@IP_DEL_SERVIDOR
```

Example:
```bash
ssh -i cashia-key.pem ubuntu@3.145.21.44
```

---

### 9. Verify connection
You should see:
```
Welcome to Ubuntu 22.04
```

---

## Step 2: Create Python Environment

### 1. Update server
```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install tools
```bash
sudo apt install software-properties-common -y
```

### 3. Add Python repository
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
```

### 4. Install Python 3.11
```bash
sudo apt install python3.11 python3.11-venv python3.11-dev -y
```

### 5. Verify
```bash
python3.11 --version
```

### 6. Create virtual environment
```bash
mkdir cashia
cd cashia
python3.11 -m venv cashia_env
source cashia_env/bin/activate
```

### 7. Upgrade pip
```bash
pip install --upgrade pip
```

---

## Step 3: GitHub Access

### Generate SSH key
```bash
ssh-keygen -t ed25519 -C "aws-cashia"
```

### View and copy your public key
```bash
cat ~/.ssh/id_ed25519.pub
```

### Add the key to GitHub

Go to GitHub.

Top right:
- Profile → Settings

Then:
- SSH and GPG keys

Click on:
- New SSH key

Enter:
- **Title:** aws-cashia-server  
- **Key:** (paste the key you copied)

Save.

### Test connection
```bash
ssh -T git@github.com
```

### Clone repositories
```bash
git clone git@github.com:TU_USUARIO/cashia-core.git
git clone git@github.com:TU_USUARIO/cashia-model.git
git clone git@github.com:TU_USUARIO/cashia-api.git
```

---

## Step 4: Install dependencies

```bash
cd cashia_api
pip install -r requirements.txt

cd ..
pip install -e cashia-core
pip install -e cashia-model
pip install -e cashia-credit-engine
pip install -e cashia-api
```

---

## Step 5: Environment variables

Edit:
```bash
nano ~/.bashrc
```

Add:
```bash
export STORAGE_BACKEND=s3
export S3_BUCKET=cashia-prod-data
export S3_PREFIX=cashia
```

The name assigned to `S3_BUCKET` (in this case `cashia-prod-data`) must be globally unique within your S3 bucket environment. Save and run:

```bash
source ~/.bashrc
```

Verify:

```bash
echo $STORAGE_BACKEND
echo $S3_BUCKET
echo $S3_PREFIX
```
It should display:

```bash
s3
cashia-prod-data
cashia
```

Verify that your settings.py detects the configuration

Run a quick test:

If the cashia_env environment was deactivated after running source ~/.bashrc, reactivate it by navigating to the cashia_env directory and running:

```bash
s3
cashia-prod-data
cashia
```

Now run:

```bash
python
>>> from cashia_core.common_tools.settings import print_settings
>>> print_settings()
```

It should display something like:

```bash
BASE_DIR = /home/ubuntu/cashia
STORAGE_BACKEND = s3
LOCAL_STORAGE_ROOT = /home/ubuntu/cashia/data
S3_BUCKET = cashia-test-data
S3_PREFIX = cashia
>>>
```

---
## Step 6: Create the bucket

### 1 Create the bucket
- Go to S3  
- Click on **Create bucket**  
- Use the same globally unique name that you selected in the previous step, for example:  
  `cashia-test-data`  
- Choose the same region where your EC2 is located, to avoid latency and unnecessary costs  
- Leave **Block Public Access** enabled  

### 2 Create the cashia folder
You can create folders from the console:
1. Enter the bucket  
2. Click **Create folder**  
3. Name: `cashia`  

### 3 Upload the files required by cashia to the folder
From the AWS console:
1. Enter your bucket  
2. Enter the folder you already created: `cashia`  
3. Click on **Upload**  
4. Drag the entire `data` folder  

### 4 Create the policy for the bucket
- Go to IAM  
- In the left menu select **Policies**  
- Click on **Create policy**  

### Choose JSON editor

On the policy creation screen:
1. Select **JSON**  
2. Delete the content that appears  
3. Paste this policy (adapted to your bucket):  

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListBucketWithinPrefix",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::cashia-test-data",
      "Condition": {
        "StringLike": {
          "s3:prefix": [
            "cashia/*",
            "cashia"
          ]
        }
      }
    },
    {
      "Sid": "ObjectAccessWithinPrefix",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::cashia-test-data/cashia/*"
    }
  ]
}
```

**Important note:**

The lines:
```json
"Resource": "arn:aws:s3:::cashia-test-data"
```
and
```json
"Resource": "arn:aws:s3:::cashia-test-data/cashia/*"
```

Must match the name you selected for the bucket:  
`cashia-test-data`

## Save the policy

Then:
1. Click **Next**  
2. Policy name (for example): `cashia-s3-access`  
3. Click **Create policy**  

---

## Create or edit the EC2 Role

Now:
1. Go to **IAM → Roles**  
2. Click **Create role**  
3. Type: **AWS Service**  
4. Select: **EC2**  
5. In **Permissions policies** search for: `cashia-s3-access`  
6. Select it  
7. Role name (example): `cashia-test-ec2-role`  
8. Click **Create role**  

---

## Associate role to the server

1. Go to EC2  
2. Select your instance  
3. Click **Actions**  
4. Go to **Security**  
5. Click **Modify IAM role**  
6. Select: `cashia-test-ec2-role`  
7. Save  

---

## Test from your server (configuration and S3)

On your EC2 run:

```python
import boto3
s3 = boto3.client("s3")
print(s3.list_objects_v2(
    Bucket="cashia-test-data",
    Prefix="cashia/"
))
```

Then:

```python
from cashia_core.common_tools.settings import print_settings
print_settings()
```

It should display something like:

```
STORAGE_BACKEND = s3
LOCAL_STORAGE_ROOT = /home/ubuntu/cashia/data
S3_BUCKET = cashia-test-data
S3_PREFIX = cashia
```

Now:

```python
import pandas as pd
from cashia_core.common_tools.storage import get_storage

storage = get_storage()

df = pd.DataFrame({
    "a":[1,2,3],
    "b":[4,5,6]
})

storage.write_csv("cashia-api/outputs/test.csv", df)

df2 = storage.read_csv("cashia-api/outputs/test.csv")
print(df2)
```

Go to the bucket:  
`cashia-test-data`

You should see:

```
Cashia-test
 └── cashia-api
      └── outputs
           └── test.csv
```
---

## Step 8: Start server

```bash
gunicorn -k uvicorn.workers.UvicornWorker cashia_api.main:app --bind 0.0.0.0:8000
```

On your local machine open the file:

`test_cashia_from_file.ipynb`

Change the IP in the `server` variable and run the execution using **"Run All"**.

---

## Step 9: Test credit engine

With the `cashia` environment activated, run:

```bash
cc-engine
```

You will see the engine execute and the file:
└───cashia-credit-engine
    └───storage
     └── applications.csv

---

## 🎉 Done

Congratulations you have finished!
