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
        
        // ========== DAST Preparation ==========
        stage('Prepare DAST Environment') {
            steps {
                sh '''
                    # Créer le dossier pour les rapports DAST
                    mkdir -p ${WORKSPACE}/reports_dast
                    chmod 777 ${WORKSPACE}/reports_dast
                    
                    # Vérifier/Installer OWASP ZAP
                    echo "=== Pulling OWASP ZAP Docker Image ==="
                    docker pull zaproxy/zap-stable
                    
                    # Vérifier l'installation
                    echo "=== Verifying OWASP ZAP Installation ==="
                    docker run --rm zaproxy/zap-stable zap.sh -version
                '''
            }
        }
        
        // ========== DAST - Bad Version ==========
        stage('DAST Scan - Bad Version') {
            steps {
                sh '''
                    # Nettoyer les conteneurs existants
                    echo "=== Cleaning up existing containers ==="
                    docker stop vulpy-bad-app 2>/dev/null || true
                    docker rm vulpy-bad-app 2>/dev/null || true
                    
                    # Démarrer l'application vulnérable (Bad)
                    echo "=== Starting Vulpy Bad Application ==="
                    docker run -d --name vulpy-bad-app --network vulpy-sast-sca-analysis_default -p 5001:5000 vulpy-bad:local
                    
                    # Attendre que l'application démarre (plus longtemps)
                    echo "=== Waiting for application to start ==="
                    sleep 20
                    
                    # Vérifier que le conteneur est toujours en cours d'exécution
                    docker ps | grep vulpy-bad-app
                    
                    # Préparer le répertoire des rapports avec les bonnes permissions
                    chmod 777 ${WORKSPACE}/reports
                    
                    # Lancer le scan OWASP ZAP
                    echo "=== Running OWASP ZAP Baseline Scan on Bad Version ==="
                    docker run --rm -u root --network vulpy-sast-sca-analysis_default \
                        -v ${WORKSPACE}/reports:/zap/wrk:rw \
                        zaproxy/zap-stable \
                        zap-baseline.py \
                            -t http://vulpy-bad-app:5000/ \
                            -r zap-baseline-report-bad.html \
                            -x zap-baseline-report-bad.xml \
                            -J zap-baseline-report-bad.json \
                            -I || echo "ZAP scan completed with warnings (expected for vulnerable app)"
                    
                    # Vérifier si les rapports ont été générés
                    echo "=== Checking generated reports ==="
                    ls -la ${WORKSPACE}/reports/ | grep zap-baseline-report-bad || echo "Reports not found yet"
                    
                    # Fix permissions on generated reports
                    chmod -R 755 ${WORKSPACE}/reports_dast/ || true
                    
                    # Arrêter et supprimer le conteneur
                    echo "=== Stopping Bad Application ==="
                    docker stop vulpy-bad-app || true
                    docker rm vulpy-bad-app || true
                '''
            }
        }
        
        // ========== DAST - Good Version ==========
        stage('DAST Scan - Good Version') {
            steps {
                sh '''
                    # Nettoyer les conteneurs existants
                    echo "=== Cleaning up existing containers ==="
                    docker stop vulpy-good-app 2>/dev/null || true
                    docker rm vulpy-good-app 2>/dev/null || true
                    
                    # Démarrer l'application sécurisée (Good)
                    echo "=== Starting Vulpy Good Application ==="
                    docker run -d --name vulpy-good-app --network vulpy-sast-sca-analysis_default -p 5002:5000 vulpy-good:local
                    
                    # Attendre que l'application démarre (plus longtemps)
                    echo "=== Waiting for application to start ==="
                    sleep 20
                    
                    # Vérifier que le conteneur est toujours en cours d'exécution
                    docker ps | grep vulpy-good-app
                    
                    # Préparer le répertoire des rapports avec les bonnes permissions
                    chmod 777 ${WORKSPACE}/reports
                    
                    # Lancer le scan OWASP ZAP
                    echo "=== Running OWASP ZAP Baseline Scan on Good Version ==="
                    docker run --rm -u root --network vulpy-sast-sca-analysis_default \
                        -v ${WORKSPACE}/reports:/zap/wrk:rw \
                        zaproxy/zap-stable \
                        zap-baseline.py \
                            -t http://vulpy-good-app:5000/ \
                            -r zap-baseline-report-good.html \
                            -x zap-baseline-report-good.xml \
                            -J zap-baseline-report-good.json \
                            -I || echo "ZAP scan completed with warnings"
                    
                    # Vérifier si les rapports ont été générés
                    echo "=== Checking generated reports ==="
                    ls -la ${WORKSPACE}/reports/ | grep zap-baseline-report-good || echo "Reports not found yet"
                    
                    # Fix permissions on generated reports
                    chmod -R 755 ${WORKSPACE}/reports_dast/ || true
                    
                    # Arrêter et supprimer le conteneur
                    echo "=== Stopping Good Application ==="
                    docker stop vulpy-good-app || true
                    docker rm vulpy-good-app || true
                '''
            }
        }
        
        // ========== DAST Reports Summary ==========
        stage('DAST Reports Summary') {
            steps {
                sh '''
                    echo "=== All Security Reports (SAST + DAST) ==="
                    ls -lh ${WORKSPACE}/reports/ | grep -E '(bandit|trivy|zap)'
                '''
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            
            publishHTML([
                reportDir: 'reports',
                reportFiles: 'bandit-bad.html, bandit-good.html, zap-baseline-report-bad.html, zap-baseline-report-good.html',
                reportName: 'Security Reports',
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true
            ])
        }
        
        cleanup {
            // Nettoyage des conteneurs et images si nécessaire
            sh '''
                docker stop vulpy-bad-app vulpy-good-app 2>/dev/null || true
                docker rm vulpy-bad-app vulpy-good-app 2>/dev/null || true
            '''
        }
    }
}
