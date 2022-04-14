# Helm Chart for Apache NiFi

## Prerequisites

- Kubernetes cluster 1.10+
- Helm 3.0.0+

## Add & Update Relevant Charts

```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add dysnix https://dysnix.github.io/charts/
helm repo update
helm dep up
```

## Install Nifi
```
helm install nifi . --namespace nifi --create-namespace --wait
```

## Access Nifi
```
kubectl port-forward -n nifi1 svc/nifi 8443:8443
```

## Login
Credentials are set in the values.yml file. Currently, 
```
username=username
password=changemechangeme
```
