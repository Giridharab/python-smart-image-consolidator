import docker
import os

# Optional: Cloud cost per vCPU and GB memory per hour
AWS_COST = {
    "cpu_per_hour": 0.05,   # $ per vCPU
    "mem_per_hour": 0.01    # $ per GB memory
}

client = docker.from_env()

def estimate_cost(image_name):
    """
    Estimate resource usage and cost for a Docker image.
    """
    try:
        # Pull image locally to inspect
        image = client.images.pull(image_name)
        image_size_mb = image.attrs['Size'] / (1024 * 1024)

        # Estimate CPU/Memory requirements heuristically
        # (Could also parse Dockerfile for heavy layers, e.g., python + packages)
        cpu = 0.5  # vCPU
        memory = max(image_size_mb / 100, 0.5)  # GB

        # Cost per hour
        cost_per_hour = cpu * AWS_COST["cpu_per_hour"] + memory * AWS_COST["mem_per_hour"]

        return {
            "cpu_vCPU": cpu,
            "memory_GB": memory,
            "image_size_MB": round(image_size_mb, 2),
            "estimated_cost_per_hour": round(cost_per_hour, 4)
        }
    except Exception as e:
        return {"error": str(e)}