[![DOI](https://zenodo.org/badge/836272240.svg)](https://doi.org/10.5281/zenodo.14236862)

This repository is the third part of the [FAIRification pipeline](https://github.com/BBMRI-cz/NGS-data-FAIRification) and is responsible for uploading metadata to [data.bbmri.cz](https://data.bbmri.cz/) catalogue.

## Supported sequencing types
Miseq, New Miseq, MammaPrint

## How to run the scripts
### Locally - Development
#### Using main.py
1. Install requirements
```bash
pip install -r requiremenents.txt
```
2. Run main.py
```bash
python main.py -r path/to/pseudonymized/runs/folder  -o /path/to/root/organisation/folder -p /path/to/patients/folder
```
#### Using docker-compose
```bash
docker-compose up -d --build
```
### In production
Production is running on Kubernetes cluster SensitiveCloud
#### Using kubernetes (kubectl)
Deploy dependent secrets
```bash
## Supported sequencing types
Miseq, New Miseq, MammaPrint

## How to run the scripts
### Locally - Development
#### Using main.py
1. Install requirements
```bash
pip install -r requiremenents.txt
```
2. Run main.py
```bash
python main.py -r path/to/pseudonymized/runs/folder  -o /path/to/root/organisation/folder -p /path/to/patients/folder
```
#### Using docker-compose
```bash
docker-compose up -f compose.yml -d --build
```
### In production
Production is running on Kubernetes cluster SensitiveCloud
#### Using kubernetes (kubectl)
Deploy dependent secrets
```bash
kubectl apply -f kubernetes/catalog-secret.yaml -n bbmri-mou-ns
```
```bash
kubectl apply -f kubernetes/uploader-job.yaml -n bbmri-mou-ns
```
#### Deploying new version in production
Build new docker image
```bash
docker build --no-cache <public-dockerhub-repository>/data-catalogue-organiser:<version> .
docker push <public-dockerhub-repository>/data-catalogue-organiser:<version> 
# change version in kubernetes/organiser-job.yaml
```
#### Debigging
You can visit kubernetes UI [Rancher](https://rancher.cloud.trusted.e-infra.cz/) find the failing pod and investigate in logs.
On how to use Rancher and SensitiveCloud visit [Docs](https://docs.cerit.io/en/platform/overview)

Other option is running a testing job and investigation inside the cluster filemanager (to check user permissions etc.)
```bash
kubectl apply kubectl apply -f kubernetes/testing-job.yaml -n bbmri-mou-ns
```
Then connect to terminal of this job/pod on [Rancher](https://rancher.cloud.trusted.e-infra.cz/)

```bash
kubectl apply -f kubernetes/organiser-job.yaml -n bbmri-mou-ns
```
#### Deploying new version in production
Build new docker image
```bash
docker build --no-cache <public-dockerhub-repository>/data-catalogue-uploader:<version> .
docker push <public-dockerhub-repository>/data-catalogue-uploader:<version> 
# change version in kubernetes/organiser-job.yaml
```
#### Debigging
You can visit kubernetes UI [Rancher](https://rancher.cloud.trusted.e-infra.cz/) find the failing pod and investigate in logs.
On how to use Rancher and SensitiveCloud visit [Docs](https://docs.cerit.io/en/platform/overview)

Other option is running a testing job and investigation inside the cluster filemanager (to check user permissions etc.)
```bash
kubectl apply kubectl apply -f kubernetes/testing-job.yaml -n bbmri-mou-ns
```
Then connect to terminal of this job/pod on [Rancher](https://rancher.cloud.trusted.e-infra.cz/)
