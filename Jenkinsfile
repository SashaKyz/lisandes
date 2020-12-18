pipeline {
	agent {
	    label 'linux'
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
		stage('Build') {
		    steps {
		        sh 'docker-compose build'
		    }
		}
		stage('Push to registry') {
		    steps {
			    sh 'docker-compose push'
			}
		}
	}
}
