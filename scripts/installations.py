import os
import platform
import subprocess
import sys

def run_cmd(cmd):
    """Run a shell command and return stdout if successful; exit on error."""
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()

def get_os():
    """Determine the operating system."""
    return platform.system().lower()

def install_kubectl():
    """Install kubectl based on the operating system."""
    os_name = get_os()
    if os_name == "linux":
        run_cmd("curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl")
        run_cmd("chmod +x kubectl")
        run_cmd("sudo mv kubectl /usr/local/bin/")
    elif os_name == "darwin":  # macOS
        run_cmd("curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl")
        run_cmd("chmod +x kubectl")
        run_cmd("sudo mv kubectl /usr/local/bin/")
    elif os_name == "windows":
        print("Please download kubectl manually from https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/")
        sys.exit(1)
    else:
        print(f"Unsupported OS: {os_name}. Cannot install kubectl.")
        sys.exit(1)

def install_helm():
    """Install Helm based on the operating system."""
    os_name = get_os()
    if os_name == "linux":
        run_cmd("curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash")
    elif os_name == "darwin":  # macOS
        run_cmd("brew install helm")
    elif os_name == "windows":
        print("Please download Helm manually from https://helm.sh/docs/intro/install/")
        sys.exit(1)
    else:
        print(f"Unsupported OS: {os_name}. Cannot install Helm.")
        sys.exit(1)

def is_tool_installed(tool):
    """Check if a command-line tool is installed."""
    return run_cmd(f"which {tool}") is not None

def check_and_install(tool_name, install_function):
    """Check if a tool is installed; if not, prompt for installation."""
    if not is_tool_installed(tool_name):
        print(f"{tool_name} is not installed on this machine.")
        choice = input(f"Do you want to install {tool_name}? (Y/N): ").strip().lower()
        if choice in ["y", "yes"]:
            print(f"Installing {tool_name}...")
            install_function()
            print(f"{tool_name} installation complete.")
        else:
            print(f"{tool_name} is required. Please install it manually.")
            sys.exit(1)
    else:
        print(f"{tool_name} is already installed.")


# if __name__ == "__main__":
#     check_and_install("kubectl", install_kubectl)
#     check_and_install("helm", install_helm)
#     print("All necessary tools are installed and ready.")
