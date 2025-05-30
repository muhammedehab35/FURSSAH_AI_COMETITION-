# Furssah-AI-Competition--Tunisia
A hybrid cybersecurity assistant combining LLM-driven contextual chat and deep learning-based real-time network threat detection.

# 🔐 CYBER-SHIELD INTELLIGENT ASSISTANT

---

## 🚀 Features

🧠 LLM Chat Core — Fine-tuned Qwen-2.5B Instruct using LLaMA Factory, Hugging Face, and Weights & Biases for expert-level cybersecurity assistance (CVEs, pentest guidance, malware behavior, etc.).

📊 Threat Classifier — Hybrid pipeline combining traditional ML models (Decision Tree, Random Forest, SVM, KNN) with deep RNN/LSTM architectures to classify suspicious flows and predict key parameters.

📈 Anomaly Insights — Outputs include:

Risk scores (e.g., 75/100 with confidence)

Detected threats (e.g., port scan, DDoS)

Key anomalies (packet rate, unidirectional flow, uncommon ports)

Actionable recommendations

🖥️ Web-Based Interface — Built with Flask backend and HTML/JavaScript/CSS frontend for a responsive and user-friendly interaction with both the LLM and threat detection modules.

📦 Modular Architecture — Clean project structure separating:

LLM processing

ML threat analysis

File ingestion / pre-processing

Web interface rendering

API routes and communication layers
---

## 📁 Project Structure
<pre>
cybershield-intelligent/
├── app/
│   ├── api/
│   │   ├── chat_handler.py        # Routes for chat (Qwen)
│   │   ├── threat_analyzer.py     # Routes for threat analysis
│   │   └── main.py                # FastAPI or Flask entrypoint
│   ├── llm/
│   │   └── qwen_chat.py           # Inference wrapper for Qwen 2.5B instruct
│   ├── models/
│   │   ├── predictor_rnn.py       # RNN/LSTM inference logic
│   │   ├── preprocess.py          # Input normalization / scaling
│   │   └── model_weights/         # Weights & configs
│   ├── frontend/
│   │   └── streamlit_ui.py        # Chat + Threat Upload UI
│   └── utils/
│       └── helpers.py             # Logging, formatting, scoring utils
├── data/
│   └── samples/                   # Sample PCAPs / logs / threat flows
├── .env.example                   # Environment variable template
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE

<pre>
