# Running tests in Docker (Windows)

Use Docker to run E2E tests in a Linux container. This avoids:

- **Sandbox limits** (e.g. Cursor/IDE environment blocking subprocesses or network)
- **Proxy issues** (e.g. git or pytest hitting a bad proxy on the host)
- **Conflicting tools** (e.g. global SeleniumBase vs pytest-playwright)

The container has its own network, Python, and Playwright browsers—no host proxy or sandbox.

---

## Prerequisites (Windows)

1. **Docker Desktop for Windows**
   - Install from [docker.com](https://www.docker.com/products/docker-desktop/).
   - Use **WSL2** as the backend (default): *Settings → General → Use the WSL 2 based engine*.
   - Docker runs **Linux containers** by default; keep that. No need for Windows containers.

2. **Open a terminal** in the repo (PowerShell or WSL):
   ```powershell
   cd C:\Users\<You>\.cursor\projects\C-Users-SLethuli\automation-testing-playground
   ```

---

## Build the image (once)

From the repo root:

```powershell
docker compose build
```

Or with plain Docker:

```powershell
docker build -t automation-testing-playground .
```

---

## Run E2E tests in the container

**Recommended (Compose):**

```powershell
docker compose run --rm tests
```

This uses `init: true` and `ipc: host` (see `docker-compose.yml`) to reduce Chromium issues.

**Plain Docker:**

```powershell
docker run --rm --init --ipc=host -e PLAYWRIGHT_HEADED=0 automation-testing-playground
```

**Run a subset of tests:**

```powershell
docker compose run --rm tests pytest tests/e2e/saucedemo/ tests/e2e/blazedemo/ -v
```

---

## Optional: run integration tests in Docker

Same image; override the command:

```powershell
docker compose run --rm tests pytest tests/integration/ -v
```

Integration tests need network (e.g. jsonplaceholder, httpbin); the container has normal outbound access.

---

## If you hit proxy or network inside the container

If your **host** uses a corporate proxy, Docker Desktop can pass it into containers. You can set env vars when running:

```powershell
docker compose run --rm -e HTTP_PROXY= -e HTTPS_PROXY= tests
```

(Empty values disable proxy inside the container if the host sets them.)

Or in `docker-compose.yml` under `tests` → `environment` add:

```yaml
- HTTP_PROXY=
- HTTPS_PROXY=
```

---

## Summary

| Goal                         | Command                                      |
|-----------------------------|----------------------------------------------|
| Build image                 | `docker compose build`                       |
| Run all E2E tests           | `docker compose run --rm tests`              |
| Run specific E2E suite      | `docker compose run --rm tests pytest tests/e2e/saucedemo/ -v` |
| Run integration tests       | `docker compose run --rm tests pytest tests/integration/ -v`   |

Tests run **inside** the container (Linux, headless Chromium). No sandbox or host proxy affects them.

---

## Verification note

Running `docker compose build` or `docker compose run` from inside Cursor (e.g. via the agent) may still hit sandbox limits (e.g. "Access is denied" to the Docker daemon or buildx). **Run Docker locally** (PowerShell or WSL in the repo) to verify:

```powershell
docker compose build
docker compose run --rm tests
```

If those succeed locally, the Docker setup is working and future test runs can use the same flow to avoid proxy and network blocking. See workspace Cursor rule **use-docker-for-tests-and-network** for using Docker across repos.
