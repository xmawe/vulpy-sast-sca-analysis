# TP - Analyse de Sécurité SAST et SCA avec Vulpy

## 📋 Description

Ce travail pratique consiste à effectuer une analyse de sécurité complète d'une application Python vulnérable (Vulpy) en utilisant des outils d'analyse statique (SAST) et d'analyse de composition logicielle (SCA).

L'application Vulpy existe en deux versions :
- **Bad** (vulnérable) : contient intentionnellement des vulnérabilités de sécurité
- **Good** (sécurisée) : version corrigée avec les bonnes pratiques de sécurité

## 🎯 Objectifs du TP

1. Comprendre les vulnérabilités courantes dans les applications web Python
2. Utiliser des outils automatisés pour détecter les failles de sécurité
3. Analyser les dépendances et identifier les CVE (Common Vulnerabilities and Exposures)
4. Comparer les résultats entre une version vulnérable et une version sécurisée
5. Interpréter les rapports de sécurité générés

## 🛠️ Outils Utilisés

### SAST (Static Application Security Testing)
- **Bandit** : Analyse statique du code Python pour détecter les problèmes de sécurité

### SCA (Software Composition Analysis)
- **Trivy** : Scanner de vulnérabilités pour les dépendances, conteneurs et configurations
  - Analyse des dépendances directes et transitives
  - Détection de secrets et configurations dangereuses
  - Analyse de la chaîne d'approvisionnement (supply chain)
  - Scan des images de conteneurs

### CI/CD
- **Jenkins** : Automatisation de l'analyse de sécurité via pipeline

## 📁 Structure du Projet

```
vulpy-sast-sca-analysis/
├── docker-compose.yml          # Configuration Docker
├── Dockerfile.jenkins          # Image Jenkins personnalisée
├── Jenkinsfile                 # Pipeline d'analyse de sécurité
├── requirements.txt            # Dépendances du projet
└── vulpy/                      # Application cible
    ├── bad/                    # Version vulnérable
    │   ├── *.py               # Code Python avec vulnérabilités
    │   ├── templates/         # Templates HTML
    │   └── static/            # Fichiers statiques
    ├── good/                   # Version sécurisée
    │   ├── *.py               # Code Python sécurisé
    │   ├── templates/         # Templates HTML
    │   └── static/            # Fichiers statiques
    └── utils/                  # Utilitaires de sécurité
```

## 🚀 Installation et Lancement

### Prérequis
- Docker et Docker Compose installés
- Au moins 4 GB de RAM disponible
- Port 8080 disponible pour Jenkins

### Démarrage de l'environnement

1. **Cloner le projet** (si ce n'est pas déjà fait)
   ```bash
   cd c:/Users/user/Desktop/vulpy-sast-sca-analysis
   ```

2. **Lancer les conteneurs**
   ```bash
   docker-compose up -d
   ```

3. **Accéder à Jenkins**
   - URL : http://localhost:8080
   - Attendre que Jenkins soit complètement démarré (environ 1-2 minutes)

4. **Récupérer le mot de passe initial de Jenkins** (première connexion uniquement)
   ```bash
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```

5. **Configurer Jenkins**
   - Installer les plugins recommandés
   - Créer un utilisateur administrateur
   - Créer un nouveau pipeline et pointer vers le `Jenkinsfile`

## 🔍 Exécution de l'Analyse

### Via Jenkins

1. Ouvrir Jenkins : http://localhost:8080
2. Créer ou ouvrir le job de pipeline
3. Cliquer sur "Build Now"
4. Suivre l'exécution dans la console

### Pipeline d'Analyse

Le pipeline exécute les étapes suivantes :

#### 1. **Analyse Statique du Code (SAST)**
   - Scan de la version **bad** avec Bandit
   - Scan de la version **good** avec Bandit
   - Génération de rapports HTML

#### 2. **Analyse des Dépendances**
   - Scan des dépendances de la version **bad**
   - Scan des dépendances de la version **good**
   - Analyse du fichier `requirements.txt`
   - Analyse des dépendances transitives

#### 3. **Détection de Secrets**
   - Recherche de secrets hardcodés dans la version **bad**
   - Recherche de secrets hardcodés dans la version **good**

#### 4. **Analyse de la Chaîne d'Approvisionnement**
   - Vérification de l'intégrité des dépendances (bad)
   - Vérification de l'intégrité des dépendances (good)

#### 5. **Scan des Conteneurs**
   - Construction de l'image Docker de la version **bad**
   - Scan de vulnérabilités de l'image **bad**
   - Construction de l'image Docker de la version **good**
   - Scan de vulnérabilités de l'image **good**

## 📊 Rapports Générés

Tous les rapports sont archivés dans le répertoire `reports/` et accessibles via Jenkins.

### Aperçu du Pipeline

![Pipeline Overview](screenshoots/pipline-overview.png)
*Vue d'ensemble du pipeline d'analyse de sécurité dans Jenkins*

### Artefacts de Build

![Build Artifacts](screenshoots/build-artifacts.png)
*Rapports générés et disponibles en téléchargement*

### Rapports Bandit (HTML)
- **bandit-bad.html** : Analyse de sécurité du code vulnérable
- **bandit-good.html** : Analyse de sécurité du code sécurisé

### Rapports Trivy (JSON)

#### Version Bad (Vulnérable)
- **trivy-dependencies-bad.json** : Vulnérabilités des dépendances
- **trivy-secrets-bad.json** : Secrets et configurations dangereuses
- **trivy-supply-chain-bad.json** : Analyse de la chaîne d'approvisionnement
- **trivy-container-bad.json** : Vulnérabilités de l'image Docker

#### Version Good (Sécurisée)
- **trivy-dependencies-good.json** : Vulnérabilités des dépendances
- **trivy-secrets-good.json** : Secrets et configurations dangereuses
- **trivy-supply-chain-good.json** : Analyse de la chaîne d'approvisionnement
- **trivy-container-good.json** : Vulnérabilités de l'image Docker

#### Rapports Communs
- **all-dependencies.txt** / **all-deps.txt** : Liste complète des dépendances
- **trivy-requirements.json** : Analyse du fichier requirements.txt

## 📖 Interprétation des Résultats

### Niveaux de Sévérité

Les vulnérabilités sont classées selon leur gravité :
- **CRITICAL** : Critique - Nécessite une action immédiate
- **HIGH** : Élevée - Correction prioritaire
- **MEDIUM** : Moyenne - À corriger rapidement
- **LOW** : Faible - À surveiller

### Types de Vulnérabilités Courantes

#### Vulnérabilités SAST (Bandit)
- Injection SQL
- Cross-Site Scripting (XSS)
- Utilisation de fonctions dangereuses (eval, exec)
- Gestion incorrecte des mots de passe
- Génération faible de nombres aléatoires
- Désérialisation non sécurisée

#### Vulnérabilités SCA (Trivy)
- CVE dans les dépendances
- Versions obsolètes de bibliothèques
- Secrets exposés dans le code
- Configurations non sécurisées
- Vulnérabilités dans les images de base

## 📝 Questions du TP

### Partie 1 : Analyse SAST

1. Combien de vulnérabilités critiques sont détectées dans la version **bad** ?
2. Quels types de vulnérabilités sont les plus fréquents ?
3. Comparez les résultats entre la version **bad** et **good**. Quelles différences observez-vous ?
4. Identifiez 3 vulnérabilités spécifiques et expliquez leur impact potentiel

### Partie 2 : Analyse SCA

1. Quelles dépendances présentent des vulnérabilités connues (CVE) ?
2. Quelle est la sévérité la plus élevée des CVE détectées ?
3. Des secrets sont-ils détectés dans le code ? Si oui, lesquels ?
4. Y a-t-il des différences entre les dépendances de **bad** et **good** ?

### Partie 3 : Analyse des Conteneurs

1. Quelle est la différence de vulnérabilités entre les images Docker **bad** et **good** ?
2. D'où proviennent principalement les vulnérabilités (code applicatif ou image de base) ?
3. Proposez des mesures pour réduire la surface d'attaque des conteneurs

### Partie 4 : Synthèse

1. Quelle est la différence principale entre l'analyse SAST et SCA ?
2. Pourquoi est-il important d'utiliser les deux types d'analyse ?
3. Quelles recommandations feriez-vous pour améliorer la sécurité de l'application ?

## 🔧 Commandes Utiles

### Docker

```bash
# Voir les logs de Jenkins
docker logs jenkins -f

# Redémarrer Jenkins
docker restart jenkins

# Arrêter l'environnement
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v

# Accéder au conteneur Jenkins
docker exec -it jenkins bash
```

### Analyse Manuelle

```bash
# Lancer Bandit manuellement sur la version bad
docker exec jenkins bash -c "cd /vulpy/vulpy && bandit -r bad"

# Lancer Trivy manuellement
docker exec jenkins trivy fs /vulpy/vulpy/bad
```

## 📚 Ressources Complémentaires

- [Documentation Bandit](https://bandit.readthedocs.io/)
- [Documentation Trivy](https://aquasecurity.github.io/trivy/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)
- [CVE - Common Vulnerabilities and Exposures](https://cve.mitre.org/)

## 🤝 Livrables Attendus

1. **Rapport d'analyse** comprenant :
   - Captures d'écran des rapports Jenkins
   - Analyse comparative entre les versions bad et good
   - Réponses aux questions du TP
   - Recommandations de sécurité

2. **Exports des rapports** :
   - Rapports Bandit (HTML)
   - Rapports Trivy (JSON)

## 👥 Auteur

TP réalisé par JADA Mohamed

## 📄 Licence

Ce projet utilise l'application Vulpy à des fins éducatives uniquement.