import os
import sys
from common import run_cmd, check_cluster_connection
from installations import is_tool_installed, check_and_install, install_kubectl, install_helm

def ensure_prerequisites():
    """Ensure that both kubectl and helm are installed."""
    print("Checking if 'kubectl' and 'helm' are installed...")
    check_and_install("kubectl", install_kubectl)
    check_and_install("helm", install_helm)

def verify_helm():
    """Verify if Helm is installed and functioning."""
    try:
        run_cmd("helm version")
    except SystemExit:
        print("Helm not found. Please install helm before proceeding.")
        sys.exit(1)

def install_keda(namespace="keda"):
    """Install KEDA using Helm in the specified namespace."""
    run_cmd(f"kubectl create namespace {namespace} --dry-run=client -o yaml | kubectl apply -f -")
    run_cmd("helm repo add keda https://kedacore.github.io/charts")
    run_cmd("helm repo update")
    # Install or upgrade KEDA using Helm
    run_cmd(f"helm upgrade --install keda keda/keda --namespace {namespace}")
    # Verify KEDA pods
    print(run_cmd(f"kubectl get pods -n {namespace}"))

if __name__ == "__main__":
    # Ensure prerequisites (kubectl and helm) are installed
    ensure_prerequisites()
    
    # Check if the current cluster is accessible
    check_cluster_connection()
    
    # Verify Helm functionality
    verify_helm()
    
    # Install KEDA
    install_keda()
    
    print("KEDA installed and cluster is ready.")
