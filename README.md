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

Other then that the only thing to note is that due to how much the configuration changes depending on where your kube cluster is deployed (GKE, Azure, AWS, baremetal, etc.) this demo does NOT do anything with volumes. While volumes do have some quirks to them it shouldn't take much to understand them with some research.

You should also be aware of the node IP for your cluster, asuming of course it is a single node cluster. A single node cluster is easiest to demo with.

The Demo
---------------
```
--> Go to the presentation
# Quick demo of a few kubectl commands
kubectl
kubectl get
kubectl get po
kubectl get deploy
kubectl get svc

# Lets go over a deployment config and deploy it
--> Return to the presentation
--> Go and view kube-configs/app-1.deployment.yaml
kubectl create -f kube-configs/app-1.deployment.yaml
kubectl get deploy
kubectl describe deploy app-1-deployment
kubectl get po
kubectl describe po {POD_ID_HERE}
  Note: The pod failed a readiness check at the beginning

# Lets now review and deploy a service to make it accessible
kubectl get svc
--> Return to the presentation
--> Go and view kube-configs/app-1.service.yaml
kubectl create -f kube-configs/app-1.service.yaml
kubectl get svc
kubectl describe svc
--> Go to the node ip and service port /app-1

# Lets check the logs of our little visit
kubectl get po
kubectl logs -f {POD_ID_HERE}
  Note: When fetching logs you can specicify which container from the pod. Otherwise it just takes the first one.

# Lets see how scaling works
kubectl scale --replicas=5 deployment/app-1-deployment
kubectl get po
kubectl describe svc
  Note: The endpoints in the service definition now list all the pods.

# Lets purposly do a bad update to demo rollbacks
kubectl set image deployment/app-1-deployment app-1=regner/kubernetes-demo:badupdate
kubectl rollout status deployments app-1-deployment
kubectl get deployments
kubectl get po
kubectl rollout history deployment/app-1-deployment
kubectl rollout undo deployment/app-1-deployment
  Note: You can specify version with --to-revision={REVISION_ID}

# Now for a proper good update
kubectl set image deployment/app-1-deployment app-1=regner/kubernetes-demo:v2
kubectl rollout status deployments app-1-deployment
kubectl get deployments
kubectl get po
--> Go to the node ip and service port
  Note: The web site should now mention version 2

# Time to deploy some more services!
# Start with traefik
--> Return to the presentation
--> Go and view kube-configs/traefik.deployment.yaml
kubectl create -f kube-configs/traefik.deployment.yaml
--> Go to node ip

--> Go and view kube-configs/app-3.deployment.yaml
--> Go and view kube-configs/app-3.service.yaml
--> Go and view kube-configs/app-3.ingress.yaml
kubectl create -f kube-configs/app-2.deployment.yaml
kubectl create -f kube-configs/app-2.service.yaml
kubectl create -f kube-configs/app-2.ingress.yaml
--> Go and view app-2 at node-ip/app-2

# Now with a deployment that uses config maps to create a file
--> Go and view kube-configs/app-3.configmap.yaml
--> Go and view kube-configs/app-3.deployment.yaml
kubectl create -f kube-configs/app-3.configmap.yaml
kubectl create -f kube-configs/app-3.deployment.yaml
kubectl create -f kube-configs/app-3.service.yaml
kubectl create -f kube-configs/app-3.ingress.yaml
--> Go and view app-3 at node-ip/app-3

# At this point app-1 is still found on the node port
--> Remove `type: NodePort` from kube-configs/app-1.service.yaml
kubectl apply -f kube-configs/app-1.service.yaml
kubectl create -f kube-configs/app-1.ingress.yaml
--> Return to the presentation

# If you can easily do it, clean your cluster completely and run:
kubectl create -f kube-configs/
```


Missing Things
--------------
Pause Rollout
Secrets
Pet Set
Daemon Set
Job
Finishing the presentation



