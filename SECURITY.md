# 🔒 Security & Secret Management

This document describes the security practices used in the CryptoLab CI/CD pipeline, focusing on how sensitive credentials are managed and protected.

---

## GitHub Secrets

All sensitive values (API tokens, credentials, webhooks) are stored as **GitHub Encrypted Secrets**, never hard-coded in source files.

### How GitHub Secrets Work

1. **Encrypted at rest** — Secrets are encrypted using a **libsodium sealed box** before they even reach GitHub's servers.
2. **Masked in logs** — If a secret value appears in workflow output, GitHub automatically replaces it with `***`.
3. **Scoped access** — Secrets are only available to GitHub Actions workflows within the repository they're defined in.
4. **Injected at runtime** — Secrets are passed as environment variables into the runner at job execution time, not embedded in code.

### Secrets Used in This Project

| Secret Name | Purpose | Pipeline |
|---|---|---|
| `SONAR_TOKEN` | Authenticates with SonarCloud for code quality analysis | Dev + Staging |
| `DOCKERHUB_USERNAME` | Docker Hub account identifier for image push | Staging only |
| `DOCKERHUB_TOKEN` | Docker Hub access token (scoped to push) | Staging only |
| `DISCORD_WEBHOOK` | Webhook URL for sending pipeline notifications | Dev + Staging |
| `GITHUB_TOKEN` | Auto-generated per workflow run; used for API calls (e.g., `gh` CLI) | Dev + Staging |

### How Secrets Are Consumed

```yaml
# Example from staging.yml
- name: Login to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

The `${{ secrets.* }}` syntax retrieves the secret at runtime. The value is **never** written to the workflow file or committed to version control.

---

## Container Security Scanning

The **staging pipeline** includes an automated vulnerability scan using **Trivy** (by Aqua Security) on every Docker image before it is pushed to Docker Hub.

### What Trivy Scans

- **OS packages** (Debian/Ubuntu base image vulnerabilities)
- **Application dependencies** (Python packages installed via `pip`)
- **Known CVEs** cross-referenced against the National Vulnerability Database (NVD)

### Policy

- Severity levels scanned: **CRITICAL** and **HIGH**
- If any CRITICAL or HIGH vulnerability is found, the pipeline **fails** and the image is **not pushed** to Docker Hub.
- This ensures no known-vulnerable images reach production.

---

## Best Practices Followed

| Practice | Implementation |
|---|---|
| **No hard-coded secrets** | All credentials stored in GitHub Secrets |
| **Least-privilege tokens** | Docker Hub token scoped to push only |
| **Auto-rotated tokens** | `GITHUB_TOKEN` is generated per workflow run and expires immediately |
| **Pre-deployment scanning** | Trivy blocks vulnerable images before push |
| **Masked log output** | GitHub auto-redacts secrets in Actions logs |
| **Dependency auditing** | SonarCloud checks for known vulnerabilities in code dependencies |
