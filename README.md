# Voting App (Azure DevOps + AKS + ArgoCD)

3-tier microservice voting app with CI (Azure Pipelines) and CD (ArgoCD to AKS).

- vote (Flask) → Redis
- worker (Python) → Redis → Postgres tallies
- result (Flask) → Postgres

## Quick Start (Local)
```bash
make up        # build & start
make health    # verify endpoints
# vote:  http://localhost:5050
# result: http://localhost:5051
```
```bash
make logs      # follow logs
make down      # stop & clean
```

## CI/CD Artifacts
- Pipelines: `azure-pipelines/`
- Manifests: `k8s-specifications/`
- Update script: `scripts/updateK8sManifests.sh`

## Configure (Azure DevOps)
- Create a Docker Registry service connection for ACR
- Replace placeholders in YAMLs:
  - pool: `REPLACE_WITH_SELF_HOSTED_POOL`
  - service connection: `REPLACE_WITH_SERVICE_CONNECTION_ID`
- Set pipeline secrets/variables:
  - `AZURE_REPO_HTTPS` = `https://dev.azure.com/<org>/<project>/_git/<repo>`
  - `AZURE_PAT` = PAT with Code RW + Pipelines + Service Connections

## AKS + ArgoCD (High Level)
- Create AKS and ACR; connect AKS kubeconfig
- Install ArgoCD and expose via NodePort
- Create imagePullSecret (name: `acr-pull-secret`)
- ArgoCD Application → repo path `k8s-specifications`, auto-sync

## Notes
- Do not commit secrets. Use environment variables, Key Vault/Secret Manager, and pipeline secret variables.
- Demo-friendly defaults; add persistence/security hardening for production.
