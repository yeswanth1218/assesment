pipeline {
    agent any
    parameters {
        choice(
            name: 'ACTION',
            choices: ['Setup Cluster', 'Deploy Workload', 'Health Check', 'All'],
            description: 'Choose the action to perform'
        )
    }
    environment {
        REPO_URL = 'https://github.com/yeswanth1218/assesment.git' 
        SCRIPTS_DIR = 'scripts'               
        NAMESPACE = "myapp"
        DEPLOYMENT_NAME = "my-nginx"
        IMAGE = "nginx:latest"
        PORT = "80"
        CPU_REQUEST = "100m"
        CPU_LIMIT = "200m"
        MEMORY_REQUEST = "128Mi"
        MEMORY_LIMIT = "256Mi"
        MIN_REPLICAS = "1"
        MAX_REPLICAS = "2"
        TARGET_CPU_UTILIZATION = "50"
        PYTHON_VERSION = "python3"
    }
    stages {
        stage('Checkout Code') {
            steps {
                script {
                    try {
                        echo "Checking out code from repository: ${env.REPO_URL}"
                        git branch: 'master', url: "${env.REPO_URL}"
                        echo "Code checkout completed successfully."
                    } catch (err) {
                        echo "Error during code checkout: ${err}"
                        error "Pipeline aborted during code checkout."
                    }
                }
            }
        }
        stage('Setup Cluster') {
            when {
                anyOf {
                    expression { params.ACTION == 'Setup Cluster' }
                    expression { params.ACTION == 'All' }
                }
            }
            steps {
                dir("${env.SCRIPTS_DIR}") {
                    script {
                        try {
                            echo "Starting cluster setup..."
                            def output = sh(script: "${env.PYTHON_VERSION} setup_cluster.py", returnStdout: true).trim()
                            echo "Cluster setup completed successfully. Output:\n${output}"
                        } catch (err) {
                            echo "Error during cluster setup: ${err}"
                            error "Pipeline aborted during cluster setup."
                        }
                    }
                }
            }
        }
        stage('Deploy Workload') {
            when {
                anyOf {
                    expression { params.ACTION == 'Deploy Workload' }
                    expression { params.ACTION == 'All' }
                }
            }
            steps {
                dir("${env.SCRIPTS_DIR}") {
                    script {
                        try {
                            echo "Starting workload deployment..."
                            def output = sh(script: "${env.PYTHON_VERSION} deploy_workload.py", returnStdout: true).trim()
                            echo "Workload deployment completed successfully. Output:\n${output}"
                        } catch (err) {
                            echo "Error during workload deployment: ${err}"
                            error "Pipeline aborted during workload deployment."
                        }
                    }
                }
            }
        }
        stage('Health Check') {
            when {
                anyOf {
                    expression { params.ACTION == 'Health Check' }
                    expression { params.ACTION == 'All' }
                }
            }
            steps {
                dir("${env.SCRIPTS_DIR}") {
                    script {
                        try {
                            echo "Starting health check..."
                            def output = sh(script: "${env.PYTHON_VERSION} health_check.py", returnStdout: true).trim()
                            echo "Health check completed successfully. Output:\n${output}"
                        } catch (err) {
                            echo "Error during health check: ${err}"
                            error "Pipeline aborted during health check."
                        }
                    }
                }
            }
        }
    }
    post {
        success {
            echo "Pipeline executed successfully based on the selected action!"
        }
        failure {
            echo "Pipeline failed. Please check the logs for detailed error information."
        }
    }
}
