## ✅ How to Deploy to Kubernetes (Local Cluster)

### 1. **Build the Docker Image**

If you're running Kubernetes locally (Minikube, Docker Desktop, kind, etc.), just build the image as usual:

```bash
docker build -t linkaja-qa:latest .
```

> ✅ No need to push to Docker Hub — the image will be available locally.

---

### 2. **Create Secret and Apply Manifests**

#### Option A – Using `.env` file (recommended)

If you have a `.env` file like this:

```env
OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_api_key
```

Run the following to create the secret and apply the manifests:

```bash
kubectl create secret generic linkaja-qa-secret --from-env-file=.env
kubectl apply -f k8s/
```

#### Option B – Manually edit `k8s/secret.yaml`

Replace the placeholder values in `secret.yaml` with your actual keys:

```yaml
OPENAI_API_KEY: your_openai_api_key_here
SERPAPI_API_KEY: your_serpapi_api_key_here
```

Then:

```bash
kubectl apply -f k8s/
```

---

### 3. **Access the App via Port Forward**

Since the service is set as `ClusterIP`, you can access it using:

```bash
kubectl port-forward service/linkaja-qa-service 8501:80
```

Then open your browser at:

```
http://{your-host}:8501
```

---

### 🧹 Optional: Clean Up

To delete all deployed resources:

```bash
kubectl delete -f k8s/
kubectl delete secret linkaja-qa-secret
```