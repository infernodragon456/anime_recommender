# AI-Powered Anime Recommender

An intelligent anime recommendation system that uses AI to suggest personalized anime titles based on your preferences. The system leverages:
- Large Language Models (Groq) for natural language understanding
- Vector embeddings for semantic search
- ChromaDB for efficient similarity matching
- Streamlit for an intuitive user interface

<img width="1914" height="1034" alt="Screenshot 2025-10-21 233003" src="https://github.com/user-attachments/assets/6f24ae00-72b3-480d-a354-8cf885110c99" />


## Local Deployment (Quick Start)

1. **Clone the Repository**
```bash
git clone https://github.com/infernodragon456/anime_recommender
cd anime_recommender
```

2. **Set Up Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Environment Variables**
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
```

4. **Run the App**
```bash
streamlit run app.py
```
The app will be available at `http://localhost:8501`

## Global Deployment with Kubernetes

### 1. VM Setup on Google Cloud

1. **Create VM Instance**
   - Machine Type: E2 Standard (16 GB RAM)
   - Boot Disk: Ubuntu 24.04 LTS (256 GB)
   - Enable HTTP/HTTPS traffic

2. **Initial Setup**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Configure Docker
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
sudo usermod -aG docker $USER
newgrp docker
```

### 2. Kubernetes Setup

1. **Install Minikube**
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

2. **Install kubectl**
```bash
sudo snap install kubectl --classic
minikube start
```

### 3. Deploy Application

1. **Build and Deploy**
```bash
# Point Docker to Minikube
eval $(minikube docker-env)

# Build Docker image
docker build -t llmops-app:latest .

# Create secrets
kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY="your_groq_api_key" \
  --from-literal=HUGGINGFACEHUB_API_TOKEN="your_huggingface_token"

# Deploy app
kubectl apply -f k8s.yaml
```

2. **Access the Application**
```bash
# Terminal 1: Start minikube tunnel
minikube tunnel

# Terminal 2: Port forward the service
kubectl port-forward svc/llmops-service 8501:80 --address 0.0.0.0
```
Access the app at `http://<vm-external-ip>:8501`

### 4. Monitoring with Grafana Cloud (Optional)

1. **Setup Monitoring Namespace**
```bash
kubectl create ns monitoring
```

2. **Install Helm**
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

3. **Deploy Grafana**
- Create account on Grafana Cloud
- Follow Kubernetes integration setup
- Deploy using provided Helm charts
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade --install --atomic --timeout 300s grafana-k8s-monitoring grafana/k8s-monitoring \
  --namespace "monitoring" --create-namespace --values values.yaml
```

4. **Verify Installation**
```bash
kubectl get pods -n monitoring
```

Visit Grafana Cloud dashboard to monitor your Kubernetes cluster metrics.
