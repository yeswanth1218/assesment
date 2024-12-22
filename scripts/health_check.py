import os
import json
import sys
from common import run_cmd

if __name__ == "__main__":
    namespace = os.getenv("NAMESPACE", "myapp")
    deployment_name = os.getenv("DEPLOYMENT_NAME", "my-nginx")

    # Get Deployment Status
    dep_info_str = run_cmd(f"kubectl get deployment {deployment_name} -n {namespace} -o json")
    dep_info = json.loads(dep_info_str)
    available_replicas = dep_info["status"].get("availableReplicas", 0)
    desired_replicas = dep_info["spec"]["replicas"]

    print(f"Deployment {deployment_name} in {namespace}: {available_replicas}/{desired_replicas} pods available.")

    # Get Pod Status
    pod_info_str = run_cmd(f"kubectl get pods -n {namespace} -l app={deployment_name} -o json")
    pod_info = json.loads(pod_info_str)

    if not pod_info.get("items"):
        print("No pods found for the deployment. It might be starting up or scaling.")
        sys.exit(0)

    print("Pod statuses:")
    for item in pod_info.get("items", []):
        name = item["metadata"]["name"]
        phase = item["status"]["phase"]
        print(f"  Pod: {name}, Phase: {phase}")

    # Check if metrics are available (optional)
    top_pods_result = run_cmd(f"kubectl top pods -n {namespace} --selector=app={deployment_name} --no-headers")
    if top_pods_result:
        print("Resource usage (CPU/MEM):")
        for line in top_pods_result.split("\n"):
            if not line.strip():
                continue
            cols = line.split()
            pod_name = cols[0]
            cpu = cols[1]
            mem = cols[2]
            print(f"  {pod_name}: CPU={cpu}, MEM={mem}")
    else:
        print("No resource usage metrics available (metrics-server may not be installed).")

