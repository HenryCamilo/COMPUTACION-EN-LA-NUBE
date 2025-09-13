# Archivos de Kubernetes – Práctica

Este repositorio contiene los siguientes archivos YAML para desplegar y exponer aplicaciones en Kubernetes:

- **k8s-deploy-final.yaml**  
  Define un **Deployment** para la aplicación *Image Classifier*, asegurando que siempre haya pods en ejecución con la imagen correspondiente.

- **k8s-svc.yaml**  
  Define un **Service** tipo *LoadBalancer* que expone al exterior la aplicación *Image Classifier* desplegada.

- **k8s-deploy-fastapi.yaml**  
  Define un **Deployment** para la aplicación *Hello FastAPI*, garantizando la ejecución de sus pods.

- **k8s-svc-fastapi.yaml**  
  Define un **Service** tipo *LoadBalancer* que expone la aplicación *Hello FastAPI* hacia Internet.

---
