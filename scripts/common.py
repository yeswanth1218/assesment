import subprocess
import sys
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

def run_cmd(cmd):
    """Run a shell command and return stdout if successful; exit on error."""
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"Error running command: {cmd}")
        print("STDERR:", proc.stderr.strip())
        sys.exit(1)
    return proc.stdout.strip()

def check_cluster_connection():
    """Check if kubectl is connected to any cluster and get current context."""
    try:
        run_cmd("kubectl version --client")
    except SystemExit:
        print("kubectl not found or not working properly. Please install/configure kubectl.")
        sys.exit(1)

    context = run_cmd("kubectl config current-context")
    if not context:
        print("No current kubectl context found. Please set the cluster context.")
        sys.exit(1)

    print(f"Current cluster context: {context}")
    proceed = input("Do you want to proceed with deployment on this cluster? (Y/N): ")
    if proceed.lower() not in ["y", "yes"]:
        print("Aborting deployment.")
        sys.exit(0)

def apply_manifest(yaml_content):
    """Apply a YAML manifest to the cluster."""
    # Ensure the content is passed as text
    proc = subprocess.run("kubectl apply -f -", input=yaml_content, shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        print("Error applying manifest:")
        print("STDERR:", proc.stderr.strip())
        sys.exit(1)
    return proc.stdout

def create_namespace(ns):
    """Create a namespace if it does not exist."""
    run_cmd(f"kubectl create namespace {ns} --dry-run=client -o yaml | kubectl apply -f -")

def render_template(template_path, replacements):
    """Render a YAML template with the provided replacements."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, "../", template_path)
    with open(full_path, 'r') as f:
        content = f.read()
    for k, v in replacements.items():
        content = content.replace(f"{{{{{k}}}}}", v)
    return content
