# Deployment strategy decision (31 Oct 2026)

Full write-up, a living doc: https://claude.ai/artifact/9A3oqCKnADBgKnLSHtoCzT

**Decision:** deploy on AWS.
- **Regions:** Mumbai (ap-south-1) as primary, Hyderabad (ap-south-2) for recovery.
- **Services:** ECS on Fargate (Arm), RDS for PostgreSQL Multi-AZ, ElastiCache, S3 and CloudFront, all through the existing dhruva-infra Terraform.

**Estimated infrastructure cost, USD a month at list prices (staging included, 1-year commitment price in brackets):**

| Phase | AWS | GCP |
|---|---|---|
| A | ~1,110 (~925) | ~1,220 (~1,035) |
| B | ~2,940 (~2,400) | ~3,330 (~2,815) |
| C | ~7,950 (~6,300) | ~8,810 (~7,350) |

**AI model costs, USD a month at Phase C:**
- **Usage assumed:** 1.5 million requests a month.
- **By model:** Claude about 9,400 (the same price on Bedrock and Vertex); Amazon Nova about 3,600; Gemini about 1,900.
- **Speech-to-text:** about 720 on AWS, 480 on Google.
- **Cheapest whole-stack option:** AWS infrastructure plus Gemini through Vertex AI in Mumbai, about 10,600. Google Cloud for everything with Gemini is about 11,200.
- **Model choice:** separate from the cloud. Take the cheapest model that passes evaluation (AI 5.7), with inference in India, called through dhruva-ai's provider adapter.
- **Confidence:** model prices are approximate, from memory.

**Why AWS:**
- The gap is containers: Fargate Arm costs about half of Cloud Run per vCPU. PostgreSQL costs about the same on both clouds.
- The Terraform in dhruva-infra already targets AWS.
- Both clouds keep primary and recovery regions in India.

**What would change it:**
- The AI model only runs in India on Vertex AI and legal rejects a cross-cloud call.
- Google's startup credits exceed AWS's by USD 15,000 or more.
- The team is two engineers with no infrastructure specialist.
- A client mandates a cloud.

**Open items, with due dates:**
- Verify AWS Mumbai prices in the AWS calculator; they are approximate in the doc (by 7 Nov 2026).
- Check India-region AI model availability on Bedrock and Vertex AI with legal, then run the AI evaluation on Claude, Gemini and Nova (by 7 Nov 2026).
- Compare startup credit offers (by 30 Nov 2026).
- Client decision on region-loss recovery: a disaster allowance, or move the warm standby into Phase B for about USD 450 a month (by 30 Nov 2026).
- Apply the infra, then run the Phase A load test and a restore drill before the 5 Jan 2027 pilot (by 15 Dec 2026).
