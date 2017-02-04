Kubernetes Demo
===============
This is a demo of using Kubernetes. The goal of this is to demonstrate some of the basics of Kubernetes. All of this should work on a local cluster or a cluster in Google Container Engine. The key things being demonstrated in this are:
- Deployments and common settings such as liveness and readiness probes
- Services
- Ingresses
- Common kubectl commands
- How to scale a service
- Rolling updates
- Rollbacks of deployments

Pre-requisits
-------------
This demo assumes you have a working Kubernetes cluster setup somewhere and kubectl configured to work with it. This demo also assumes you understand what containers are.

Other then that the only thing to note is that due to how much the configuration changes depending on where your Kube cluster is deployed (GKE, Azure, AWS, baremetal, etc.) this demo does NOT do anything with volumes. While volumes do have some quirks to them it shouldn't take much to understand them with some research.

You should also be aware of the node IP for your cluster, assuming of course it is a single node cluster. A single node cluster is easiest to demo with.

The Demo
---------------
```
minikube delete
minikube start
minikube ip

# Quick demo of a few kubectl commands
kubectl
kubectl get
kubectl get deploy
kubectl get po
kubectl get svc
kubectl get deploy,po,svc

# Lets go over a deployment config and deploy it
ccat app-1.deployment.yaml
  Note: 1 CPU is 1 AWS vCPU, 1 GCP Core, etc. 100m is 100 millicpu
        Measured in bytes, SI suffix (e, p, t, g, m, k) or power of two (ei, pi, ti, gi, mi, ki)
kubectl apply -f app-1.deployment.yaml
kubectl get deploy
kubectl describe deploy app-1-deployment
kubectl get po
kubectl describe po {POD_ID_HERE}
  Note: The pod failed a readiness check at the beginning

# Lets now review and deploy a service to make it accessible
kubectl get svc
ccat app-1.service.yaml
kubectl apply -f app-1.service.yaml
kubectl get svc
kubectl describe svc app-1-service
--> Go to the node ip and service port /app-1

# Lets check the logs of our little visit
kubectl get po
kubectl logs -f {POD_ID_HERE}
  Note: When fetching logs you can specify which container from the pod. Otherwise it just takes the first one.

# Lets see how scaling works
kubectl scale --replicas=5 deployment/app-1-deployment
kubectl get po
kubectl describe svc app-1-service
  Note: The endpoints in the service definition now list all the pods.

# Lets purposly do a bad update to demo rollbacks
vim app-1.deployment.yaml
  Note: image: regner/kubernetes-demo:badupdate
kubectl apply -f app-1.deployment.yaml
kubectl rollout status deployments app-1-deployment
kubectl get deployments
kubectl get po
kubectl rollout undo deployment/app-1-deployment
  Note: You can specify version with --to-revision={REVISION_ID}

# Now for a proper good update
vim app-1.deployment.yaml
  Note: image: regner/kubernetes-demo:badupdate
        replicas: 5
kubectl rollout status deployments app-1-deployment
kubectl get deployments
kubectl get po
--> Go to the node ip and service port
  Note: The web site should now mention version 2

# Time to deploy some more services!
# Start with traefik
ccat traefik.deployment.yaml
kubectl apply -f traefik.deployment.yaml
kubectl apply -f traefik.service.yaml
kubectl apply -f traefik.ingress.yaml
--> Go to node ip


ccat app-2.deployment.yaml
ccat app-2.service.yaml
ccat app-2.ingress.yaml
kubectl apply -f app-2.deployment.yaml
kubectl apply -f app-2.service.yaml
kubectl apply -f app-2.ingress.yaml
--> Go and view app-2 at node-ip/app-2

# Now with a deployment that uses config maps to apply a file
ccat app-3.configmap.yaml
ccat app-3.deployment.yaml
kubectl apply -f app-3.configmap.yaml
kubectl apply -f app-3.deployment.yaml
kubectl apply -f app-3.service.yaml
kubectl apply -f app-3.ingress.yaml
--> Go and view app-3 at node-ip/app-3

# Now with a deployment that uses config maps to deliver some environment variables
ccat app-4.configmap.yaml
ccat app-4.secret.yaml
ccat app-4.deployment.yaml
kubectl apply -f app-4.configmap.yaml
kubectl apply -f app-4.secret.yaml
kubectl apply -f app-4.deployment.yaml
kubectl apply -f app-4.service.yaml
kubectl apply -f app-4.ingress.yaml
--> Go and view app-4 at node-ip/app-4

# At this point app-1 is still found on the node port
vim app-1.service.yaml
  Note: Remove `type: NodePort`
kubectl apply -f app-1.service.yaml
kubectl apply -f app-1.ingress.yaml

# If you can easily do it, clean your cluster completely and run:
cd ..
kubectl apply -f kube-configs/
kubectl get po --v=99

# What a wonderful API Kube has
--v=99
```


Missing Things
--------------
Pause Rollout
Secrets
Persistent Services
Daemon Set
Job
Names spaces
Finishing the presentation

node plugins
node pools
