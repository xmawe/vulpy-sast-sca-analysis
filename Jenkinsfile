pipeline {
    agent any
    
    stages {
        // ========== Static Code Analysis - Bad (Vulnerable) ==========
        stage('Code Security Scan - Bad Version') {
            steps {
                sh '''
                    mkdir -p ${WORKSPACE}/reports
                    
                    # Create virtual environment if needed
                    if [ ! -d "/var/jenkins_home/bandit-venv" ]; then
                        python3 -m venv /var/jenkins_home/bandit-venv
                        . /var/jenkins_home/bandit-venv/bin/activate
                        pip install bandit
                    fi
                    
                    . /var/jenkins_home/bandit-venv/bin/activate
                    
                    cd /vulpy/vulpy
                    bandit -r bad -f html -o ${WORKSPACE}/reports/bandit-bad.html || true
                '''
            }
        }
        
        // ========== Static Code Analysis - Good (Secure) ==========
        stage('Code Security Scan - Good Version') {
            steps {
                sh '''
                    . /var/jenkins_home/bandit-venv/bin/activate
                    
                    cd /vulpy/vulpy
                    bandit -r good -f html -o ${WORKSPACE}/reports/bandit-good.html || true
                '''
            }
        }
        
        // ========== Dependency Analysis - Bad Version ==========
        stage('Dependency Scan - Bad Version') {
            steps {
                sh '''
                    cd /vulpy/vulpy/bad
                    trivy fs --scanners vuln --format json --output ${WORKSPACE}/reports/trivy-dependencies-bad.json . || true
                '''
            }
        }
        
        // ========== Dependency Analysis - Good Version ==========
        stage('Dependency Scan - Good Version') {
            steps {
                sh '''
                    cd /vulpy/vulpy/good
                    trivy fs --scanners vuln --format json --output ${WORKSPACE}/reports/trivy-dependencies-good.json . || true
                '''
            }
        }
        
        // ========== Requirements Analysis ==========
        stage('Requirements Vulnerability Scan') {
            steps {
                sh '''
                    cd /vulpy/vulpy
                    trivy fs --format json --output ${WORKSPACE}/reports/trivy-requirements.json requirements.txt || true
                '''
            }
        }
        
        // ========== Transitive Dependencies Check ==========
        stage('All Dependencies Analysis') {
            steps {
                sh '''
                    cd /vulpy/vulpy
                    python3 -m venv /tmp/scan-venv
                    . /tmp/scan-venv/bin/activate
                    pip install -r requirements.txt
                    pip freeze > ${WORKSPACE}/reports/all-dependencies.txt
                    cp ${WORKSPACE}/reports/all-dependencies.txt ${WORKSPACE}/reports/all-deps.txt
                    trivy fs ${WORKSPACE}/reports/all-dependencies.txt || true
                '''
            }
        }
        
        // ========== Secret & Configuration Scan - Bad Version ==========
        stage('Secret Scan - Bad Version') {
            steps {
                sh '''
                    cd /vulpy/vulpy/bad
                    trivy fs --scanners secret,config --format json --output ${WORKSPACE}/reports/trivy-secrets-bad.json . || true
                '''
            }
        }
        
        // ========== Secret & Configuration Scan - Good Version ==========
        stage('Secret Scan - Good Version') {
            steps {
                sh '''
                    cd /vulpy/vulpy/good
                    trivy fs --scanners secret,config --format json --output ${WORKSPACE}/reports/trivy-secrets-good.json . || true
                '''
            }
        }
        
        // ========== Supply Chain Analysis - Bad Version ==========
        stage('Supply Chain - Bad Version') {
            steps {
                sh '''
                    cd /vulpy/vulpy/bad
                    trivy fs --format json --output ${WORKSPACE}/reports/trivy-supply-chain-bad.json . || true
                '''
            }
        }
        
        // ========== Supply Chain Analysis - Good Version ==========
        stage('Supply Chain - Good Version') {
            steps {
                sh '''
                    cd /vulpy/vulpy/good
                    trivy fs --format json --output ${WORKSPACE}/reports/trivy-supply-chain-good.json . || true
                '''
            }
        }
        
        stage('Generate Security Reports') {
            steps {
                sh '''
                    echo "=== Security Reports Generated ==="
                    ls -lh ${WORKSPACE}/reports/
                '''
            }
        }
        
        // ========== Container Security - Bad Version ==========
        stage('Build Bad Application Image') {
            steps {
                sh '''
                    cd /vulpy/vulpy
                    docker build -f Dockerfile --build-arg APP_DIR=bad -t vulpy-bad:local .
                '''
            }
        }
        
        stage('Container Scan - Bad Version') {
            steps {
                sh '''
                    docker save vulpy-bad:local -o ${WORKSPACE}/vulpy-bad-image.tar
                    trivy image --input ${WORKSPACE}/vulpy-bad-image.tar --format json --output ${WORKSPACE}/reports/trivy-container-bad.json || true
                    rm -f ${WORKSPACE}/vulpy-bad-image.tar
                '''
            }
        }
        
        // ========== Container Security - Good Version ==========
        stage('Build Good Application Image') {
            steps {
                sh '''
                    cd /vulpy/vulpy
                    docker build -f Dockerfile --build-arg APP_DIR=good -t vulpy-good:local .
                '''
            }
        }
        
        stage('Container Scan - Good Version') {
            steps {
                sh '''
                    docker save vulpy-good:local -o ${WORKSPACE}/vulpy-good-image.tar
                    trivy image --input ${WORKSPACE}/vulpy-good-image.tar --format json --output ${WORKSPACE}/reports/trivy-container-good.json || true
                    rm -f ${WORKSPACE}/vulpy-good-image.tar
                '''
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            
            publishHTML([
                reportDir: 'reports',
                reportFiles: 'bandit-bad.html, bandit-good.html',
                reportName: 'Security Reports',
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true
            ])
        }
    }
}
