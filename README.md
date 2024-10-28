# Panda.ai - Real-time Intelligent Log Analysis Assistant

![Panda.ai Architecture Placeholder](https://github.com/user-attachments/assets/8ff1026f-5045-440a-8e23-9e98b38699c8)

[Check out Panda.ai on Devpost](https://devpost.com/software/panda-ai)

---

### Inspiration
In today’s data-driven world, real-time log analysis is essential for businesses needing quick insights and responses. Managing complex logs across multiple systems can be overwhelming. Panda.ai simplifies this by transforming raw logs into actionable insights that enhance reliability, performance, and proactive issue-solving. Our vision is an AI-driven assistant that keeps teams informed and empowered, removing the need for manual log interpretation.

### Problem
Large-scale systems generate vast amounts of log data, making it challenging to identify issues, especially across distributed components like databases and caches. Traditional monitoring lacks real-time, context-aware analysis, causing teams to respond after problems escalate—leading to inefficiencies, potential downtime, and reduced performance.

### Solution
Panda.ai bridges this gap by centralizing log data from Red Panda Kafka, AWS S3, AWS Cloudwatch, Redis, and more. With the power of the ReAct AI Agent, Panda.ai provides real-time log analysis, anomaly detection, and actionable insights to enable proactive issue management.

---

### Key Features
- **Log Collection**: Aggregates logs from Red Panda Kafka, AWS S3, Redis, and other sources.
- **Real-Time Analysis**: Uses the ReAct AI Agent to analyze logs, detect patterns, flag anomalies, and suggest solutions.
- **Notifications**: Delivers actionable insights and recommendations to team members for timely issue resolution.
- **Efficiency**: Reduces manual log monitoring, boosting the team's efficiency in maintaining optimal system performance.

---

## Project Setup

### Prerequisites
1. **Local Installation**:
   - [Redpanda](https://vectorized.io/docs/quick-start/) - for Kafka-compatible log streaming.
   - **Postgres** - with the `pgvector` extension for RAG (Retrieve-and-Generate) querying.
   
2. Set the AWS credentials, PostgreSQL connection details, and mail client details  in `.env`.

## Running Panda.ai

### Backend:
1. Set up the environment variables in `.env`.
2. Install requirements: `pip install -r backend/requirements.txt`
3. Run database setup (if first-time setup): navigate to `backend/app/dbsetup` and execute the setup script.
4. Start the Flask app.

### Frontend:
1. Navigate to `client`.
2. Run `npm install` to install dependencies.
3. Start the application with `npm start`.
