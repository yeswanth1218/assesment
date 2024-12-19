import os
from common import run_cmd, render_template, apply_manifest, create_namespace

if __name__ == "__main__":
    # Load variables from environment
    namespace = os.getenv("NAMESPACE", "myapp")
    deployment_name = os.getenv("DEPLOYMENT_NAME", "my-nginx")
    image = os.getenv("IMAGE", "nginx:latest")
    port = os.getenv("PORT", "80")
    cpu_request = os.getenv("CPU_REQUEST", "100m")
    cpu_limit = os.getenv("CPU_LIMIT", "200m")
    memory_request = os.getenv("MEMORY_REQUEST", "128Mi")
    memory_limit = os.getenv("MEMORY_LIMIT", "256Mi")
    min_replicas = os.getenv("MIN_REPLICAS", "1")
    max_replicas = os.getenv("MAX_REPLICAS", "5")
    target_cpu_utilization = os.getenv("TARGET_CPU_UTILIZATION", "50")

    # Ensure cluster connection (optional)
    # from common import check_cluster_connection
    # check_cluster_connection()

    create_namespace(namespace)

    # Render and apply Deployment
    deployment_yaml = render_template("templates/deployment_template.yaml", {
        "DEPLOYMENT_NAME": deployment_name,
        "NAMESPACE": namespace,
        "IMAGE": image,
        "PORT": port,
        "CPU_REQUEST": cpu_request,
        "CPU_LIMIT": cpu_limit,
        "MEMORY_REQUEST": memory_request,
        "MEMORY_LIMIT": memory_limit,
    })
    apply_manifest(deployment_yaml)

    # Render and apply Service
    service_yaml = render_template("templates/service_template.yaml", {
        "DEPLOYMENT_NAME": deployment_name,
        "NAMESPACE": namespace,
        "PORT": port,
    })
    apply_manifest(service_yaml)

    # Render and apply KEDA ScaledObject
    scaledobject_yaml = render_template("templates/keda_scaledobject_template.yaml", {
        "DEPLOYMENT_NAME": deployment_name,
        "NAMESPACE": namespace,
        "MIN_REPLICAS": min_replicas,
        "MAX_REPLICAS": max_replicas,
        "TARGET_CPU_UTILIZATION": target_cpu_utilization
    })
    apply_manifest(scaledobject_yaml)

    print(f"Deployment '{deployment_name}' created in namespace '{namespace}'.")
    print(f"Service endpoint will be available once the LoadBalancer is provisioned (if using LB).")
