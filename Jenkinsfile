def remote = [:]
remote.name = 'Rundeck'
remote.host = 'rundeck.integration.cwds.io'
remote.user = 'ansible'
remote.identityFile = '~/.ssh/id_ansible'
remote.allowAnyHosts = true

pipeline {
	agent {
	    label 'integration'
    }
    options {
        ansiColor('xterm')
        timestamps()
    }
	stages {
		stage('Preparation') {
			steps {
				cleanWs()
				// Get some code from a GitHub repository
				git branch: 'master', credentialsId: '433ac100-b3c2-4519-b4d6-207c029a103b', url: 'git@github.com:SashaKyz/lisandes.git'
			}
		}
		stage('Build and run') {
			steps {
				sh 'mkdir -p config'
				sshGet remote: remote, from: '/opt/rundeck/jobs/jobs-facilities-lis/current/config/elasticsearch.yml', into: 'config/elasticsearch.yml', override: true
				withCredentials([usernamePassword(credentialsId: '212dd917-62a9-45ae-9b6f-3eb0de725a5a', passwordVariable: 'AWS_SECRET_ACCESS_KEY', usernameVariable: 'AWS_ACCESS_KEY_ID')]) {
					sh 'docker-compose up --build'
				}
				sh 'rm -rf config'
			}

		}
		stage('Push to registry') {
					sh 'docker-compose push'
		}
	}
}
