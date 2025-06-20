# TRACE

This repository contains the source code and documentation for **TRACE** (Targeted Reconnaissance for Advanced Content Exploitation), a cybersecurity platform designed to streamline penetration testing workflows through intuitive visualizations, shallow learning algorithms, and automation. TRACE is built to help analysts discover vulnerabilities faster by offering centralized control over reconnaissance tools and AI-generated credential creation.

#### Link to Complete Project:
https://github.com/SophiaMontenegro/CS4311_TRACE_Alpha_Spring2025

## ✨ Features

- Web-based platform optimized for real-time, intranet-based testing.
- Project management: Create, lock, import, export, or delete projects. (Included in seperate repo)
- Tool dashboard: Configure and run tools like Crawler, SQL Injection, Brute Force, WFuzz, and Intruder.
- Real-time scanning: Visualize progress and results via interactive tree graphs and terminals.
- AI Credential Generator: Uses NLP and shallow learning to build username/password wordlists.
- Automatic logging, checkpoints, and role-based access controls.

## 🎨 Design

The UI was custom-built using **SvelteKit**, **shadcn-svelte**, and modern cybersecurity dashboard principles. TRACE emphasizes usability, minimalism, and accessibility—including support for analysts with color vision deficiencies and disability accommodations. You can view the Figma desgin created [here](https://www.figma.com/design/NPguwVks5wNzuG3mCRH8Zq/TRACE?node-id=0-1&t=HS4s2IDZKp6C2ytJ-1).

## 🛠️ Getting Started

To run TRACE locally:

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

Navigate to [http://localhost:3000](http://localhost:3000) to access the TRACE interface.

## 🚀 Tech Stack

- **Frontend**: SvelteKit v2.16.1 + shadcn-svelte
- **Backend**: Python 3.11.4 + FastAPI
- **Database**: Neo4j 5.26.1 (Graph DB)
- **Design Tools**: Figma, Tailwind CSS
- **Target OS**: Kali Linux (VM compatible)

## 🔐 Security

TRACE meets 30+ CAT I STIG requirements (see `STIG-compliance.md`). All data is encrypted and confined to internal network protocols (no internet dependency). Role-based access control, session timeout, input validation, and recovery checkpoints are built-in.

## 👥 Members

Meet the amazing team behind TRACE:

- **Alejandro Olivas** 
- **Valeria Contreras**
- **Ricardo Garcia**
- **Melina Levario**
- **Jorge Rodriguez**
- **Ivan Alonso**
- **Aaron Lozano**
  
## 📦 Deployment

TRACE is designed for secure internal deployment within DoD or air-gapped environments. Contact your system administrator for secure installation protocols.
