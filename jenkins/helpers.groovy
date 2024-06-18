def buildSSHRemote(params) {
  def remote = [:]
  remote.name = params.host
  remote.host = params.host
  remote.knownHosts = '/var/lib/jenkins/.ssh/known_hosts'
  remote.allowAnyHosts = params.allowAnyHosts
  remote.user = env.SSH_CREDS_USR
  if (params.withPassword) {
    remote.password = env.SSH_CREDS_PSW
  } else {
    remote.identityFile = env.SSH_CREDS
  }
  remote.logLevel = 'SEVERE'  // Setting any logLevel will remove host from public log
  return remote
}

return this
