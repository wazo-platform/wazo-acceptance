def SSH_CREDS_WITH_KEY_ID = '190ac46f-873b-4034-b639-292fcd8ba841'
def VM_NAME = 'daily-wazo-rolling-dev'
def VM_FQDN = "${VM_NAME}.lan.wazo.io"
def helpers = null

pipeline {
  agent {
    label 'acceptance-ci'
  }
  options {
    disableConcurrentBuilds()
    timeout(time: 2, unit: 'HOURS')
    buildDiscarder(logRotator(numToKeepStr: '60'))
    timestamps()
  }

  stages {
    stage ('Prepare') {
      steps {
        script {
          helpers = load('./jenkins/helpers.groovy')
        }
      }
    }
    stage ('Reset server') {
      environment {
        SSH_CREDS = credentials("${SSH_CREDS_WITH_KEY_ID}")
      }
      steps {
        script {
          def remote = helpers.buildSSHRemote(host: VM_FQDN, allowAnyHosts: true)
          sshScript(remote: remote, script: "jenkins/reset-server.sh")
        }
      }
    }
    stage ('Run tests') {
      steps {
        sh "./jenkins/run-tests.sh"
      }
    }
    stage ('Check for missing steps') {
      steps {
        sh "./jenkins/check-missing-steps.sh"
      }
    }
  }
  post {
    success {
      recordCoverage(tools: [[parser: 'COBERTURA', pattern: '**/coverage.xml']])
    }
    failure {
      mattermostSend color: "danger", channel: "#dev-failed-tests", message: "Daily Acceptance Tests [failed :nuke:](${JOB_URL})"
    }
  }
}
