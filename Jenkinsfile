def remote = [:]
remote.name = 'Rundeck'
remote.host = 'rundeck.'+ params['agent-name'] +'.cwds.io'
remote.user = 'ansible'
remote.identityFile = '~/.ssh/id_ansible'
remote.allowAnyHosts = true

pipeline {
	agent {
	    label params['agent-name']
    }
    options {
        ansiColor('xterm')
        timestamps()
    }
    properties(
        [
            [
                $class: 'RebuildSettings',
                autoRebuild: false,
                rebuildDisabled: false
            ],
            parameters(
                [
                    [
                        $class: 'NodeParameterDefinition',
                        allowedSlaves: ['integration', 'preint', 'training'],
                        defaultSlaves: ['integration'],
                        description: '',
                        name: 'agent-name',
                        nodeEligibility: [$class: 'AllNodeEligibility'],
                        triggerIfResult: 'multiSelectionDisallowed'
                    ]
                ]
            ),
            pipelineTriggers(
                [cron('H  H(6-8) * * 1 ')]
            )
        ]
    )

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
			}

		}
	}
}
