# 🏗️ PACT AWS Architecture

## Production Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          INTERNET / USERS                            │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         │ HTTPS
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│                     AWS ROUTE 53                                     │
│              api.neurobloom.ai → ALB                                 │
│              neurobloom.ai → S3/CloudFront                          │
└────────────────────────┬────────────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                  │
        │ API Traffic                      │ Website Traffic
        │                                  │
┌───────▼──────────┐              ┌───────▼──────────┐
│  Application     │              │   CloudFront     │
│  Load Balancer   │              │   (CDN)          │
│  (ALB)           │              │                  │
│  - SSL/TLS       │              │   ┌──────────┐   │
│  - Health checks │              │   │ S3 Bucket│   │
│  - WAF           │              │   │ (Website)│   │
└───────┬──────────┘              │   └──────────┘   │
        │                         └──────────────────┘
        │
        │ Forward to
        │
┌───────▼──────────────────────────────────────────────────┐
│           AWS ECS FARGATE (Auto Scaling)                  │
│                                                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   PACT API  │  │   PACT API  │  │   PACT API  │      │
│  │   Container │  │   Container │  │   Container │      │
│  │   (FastAPI) │  │   (FastAPI) │  │   (FastAPI) │      │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘      │
│         │                 │                 │              │
└─────────┼─────────────────┼─────────────────┼─────────────┘
          │                 │                 │
          │                 │                 │
          └─────────────────┴─────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        │                   │                   │
┌───────▼────────┐  ┌───────▼────────┐  ┌─────▼──────┐
│ RDS PostgreSQL │  │  ElastiCache   │  │  S3 Bucket │
│                │  │     Redis      │  │            │
│ - Sessions     │  │                │  │ - Archives │
│ - Messages     │  │ - Session      │  │ - Backups  │
│ - Emotions     │  │   cache        │  │ - Logs     │
│ - Memory graph │  │ - Rate limit   │  │            │
│                │  │                │  │            │
│ (Private       │  │ (Private       │  │            │
│  Subnet)       │  │  Subnet)       │  │            │
└────────────────┘  └────────────────┘  └────────────┘
```

---

## Component Details

### 1. **Frontend Layer**

**Route 53:**
- DNS management
- Health checks
- Traffic routing

**CloudFront + S3:**
- Static website hosting
- Global CDN
- HTTPS enforced

### 2. **API Layer**

**Application Load Balancer (ALB):**
- SSL termination
- Health checks
- Auto-scaling trigger
- WAF integration

**ECS Fargate:**
- Serverless containers
- Auto-scaling based on:
  - CPU utilization (>70%)
  - Request count (>1000 req/min)
  - Custom metrics
- Multi-AZ deployment

### 3. **Data Layer**

**RDS PostgreSQL:**
- Multi-AZ deployment
- Automated backups (daily)
- Read replicas (for scaling)
- Encrypted at rest

**ElastiCache Redis:**
- Session caching
- Rate limiting
- Real-time data
- High availability

**S3:**
- Long-term storage
- Backup archives
- CloudWatch logs
- Lifecycle policies

### 4. **Security & Monitoring**

**Security:**
- VPC with public/private subnets
- Security groups
- WAF rules
- Secrets Manager
- IAM roles

**Monitoring:**
- CloudWatch logs
- CloudWatch metrics
- CloudWatch alarms
- X-Ray tracing (optional)

---

## Simplified Starter Architecture

```
                    INTERNET
                       │
                       │
                ┌──────▼──────┐
                │   ALB       │
                │  (HTTPS)    │
                └──────┬──────┘
                       │
                ┌──────▼──────┐
                │ ECS Fargate │
                │  (1 task)   │
                └──────┬──────┘
                       │
            ┌──────────┴──────────┐
            │                     │
     ┌──────▼──────┐      ┌──────▼──────┐
     │    RDS      │      │      S3     │
     │ PostgreSQL  │      │   Backups   │
     └─────────────┘      └─────────────┘
```

**Start Simple, Scale Later!**

---

## Traffic Flow

### User Request Flow:

1. **User** → `pip install pact-langchain`
2. **Code** → `PACTMemory(api_key="sk_test_...")`
3. **Client** → HTTPS request to `api.neurobloom.ai`
4. **Route53** → Routes to ALB
5. **ALB** → Forwards to ECS container
6. **ECS** → Processes request
7. **Container** → Queries PostgreSQL/Redis
8. **Response** → Returns JSON to client
9. **Client** → Uses data in LangChain

### Data Flow:

```
Client Request
    ↓
API Validation (Auth, Rate limit)
    ↓
Check Redis Cache
    ↓ (if miss)
Query PostgreSQL
    ↓
Process (Emotional analysis, Context consolidation)
    ↓
Update Database
    ↓
Update Cache
    ↓
Return Response
```

---

## Cost Optimization

### Phase 1: Launch (100 users)
- 1 ECS task (small)
- 1 RDS instance (t3.small)
- No ElastiCache yet
- **~$100-130/month**

### Phase 2: Growth (1000 users)
- 2-3 ECS tasks (auto-scaled)
- 1 RDS instance (t3.medium)
- 1 ElastiCache node
- **~$300-500/month**

### Phase 3: Scale (10K users)
- 5-10 ECS tasks
- RDS read replicas
- Multi-node Redis cluster
- CloudFront
- **~$1000-2000/month**

---

## Deployment Steps (Quick)

### Week 1: Basic Infrastructure

```bash
# 1. Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# 2. Create subnets (public/private)
# 3. Create Internet Gateway
# 4. Configure Route Tables

# 5. Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier pact-db \
  --db-instance-class db.t3.small \
  --engine postgres \
  --master-username admin \
  --master-user-password <password> \
  --allocated-storage 20

# 6. Create ALB
aws elbv2 create-load-balancer \
  --name pact-alb \
  --subnets <subnet-ids> \
  --security-groups <sg-id>

# 7. Create ECS Cluster
aws ecs create-cluster --cluster-name pact-cluster

# 8. Deploy container
# (Use ECR to store Docker image)
```

### Alternative: Use Terraform/CDK

**Much faster!** Use Infrastructure as Code:

```hcl
# Terraform example
module "pact_api" {
  source = "./modules/ecs-fargate"
  
  cluster_name = "pact-cluster"
  service_name = "pact-api"
  container_image = "pact-api:latest"
  
  vpc_id = aws_vpc.main.id
  subnets = aws_subnet.private[*].id
  
  database_url = aws_rds_cluster.pact.endpoint
}
```

---

**Ready to deploy? Start with the checklist!** 🚀

[View Full Checklist](./AWS_DEPLOYMENT_CHECKLIST.md)
