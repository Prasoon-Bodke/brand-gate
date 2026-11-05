#!/usr/bin/env python3
"""
Verify local development environment for Brand Gate.
Checks Python version, database connectivity, Ollama, and required environment variables.
"""
import sys
import os
import asyncio
import httpx
from pathlib import Path


def check_python_version():
    """Verify Python version >= 3.11."""
    major, minor = sys.version_info[:2]
    print(f"[CHECK] Python Version: {major}.{minor}...", end=" ")
    if major >= 3 and minor >= 11:
        print("OK")
        return True
    else:
        print("FAIL (Python 3.11+ required)")
        return False


def check_env_file():
    """Verify .env file exists."""
    print("[CHECK] Environment File (.env)...", end=" ")
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        print("OK")
        return True
    else:
        print("FAIL (.env file missing, copy from .env.example)")
        return False


async def check_ollama():
    """Verify Ollama server connection."""
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    print(f"[CHECK] Ollama Connection ({ollama_url})...", end=" ")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{ollama_url}/api/tags")
            if resp.status_code == 200:
                models = [m.get("name") for m in resp.json().get("models", [])]
                print(f"OK (Available models: {', '.join(models) if models else 'none'})")
                return True
            else:
                print(f"FAIL (Status code: {resp.status_code})")
                return False
    except Exception as e:
        print(f"FAIL (Connection error: {e})")
        return False


async def check_litellm():
    """Verify LiteLLM server connection."""
    try:
        litellm_url = os.getenv("LITELLM_MASTER_KEY")
        if litellm_url:
            return True

        litellm_url = "http://localhost:4000"
        print(f"[CHECK] LiteLLM Connection ({litellm_url})...", end=" ")
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{litellm_url}/health")
            if resp.status_code == 200:
                print("OK")
                return True
            else:
                print(f"FAIL (Status code: {resp.status_code})")
                return False
    except Exception:
        print("[SKIP] LiteLLM (not configured)")
        return True


async def check_database():
    """Verify database connectivity."""
    print("[CHECK] Database Connection...", end=" ")
    db_url = os.getenv("DATABASE_URL", "")
    if not db_url:
        print("FAIL (DATABASE_URL not set)")
        return False

    try:
        sys.path.append(str(Path(__file__).parent.parent / "backend"))
        from app.core.database import AsyncSessionLocal

        async with AsyncSessionLocal() as session:
            result = await session.execute("SELECT 1")
            if result.scalar() == 1:
                print("OK")
                return True
            else:
                print("FAIL (Unexpected response)")
                return False
    except Exception as e:
        print(f"FAIL ({type(e).__name__})")
        return False


async def main():
    print("========================================")
    print("   Brand Gate Environment Verification   ")
    print("========================================\n")

    results = []
    results.append(check_python_version())
    results.append(check_env_file())
    results.append(await check_database())
    results.append(await check_ollama())

    print("\n----------------------------------------")
    if all(results):
        print("Result: All essential checks PASSED!")
    else:
        print("Result: Some checks FAILED. Please fix the issues above.")
    print("----------------------------------------")


if __name__ == "__main__":
    asyncio.run(main())