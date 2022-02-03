# ps-packager
Packager for PS Projects

Pyhton Utility to create module loadable packages for SugarCRM. Basis are the deltas of two branches in GitHub.
Paramters:
- Sugar Version (-v)
- Base branch in GitHub (-b)
- Target branch in GitHub (-t)
- GitHub Repository, to be provided in the from git@github.com:repository.git (-r)
- Package Name (-a)
- Package Description (-d)
- Package Version (-u)


Pre-requisitesto use in Jenkins:
- Credentials for GitHub user which has access rights to sugarcrm repositories need to be configured in Jenkins as Username/Password Credentials with ID "GitHub Sugar User"
- GitHub Token for user which has access rights to sugarcrm repositories need to be configured in Jenkins as Secret Text with ID "GitHub Token"
- Git repository needs to be provided in the form git@github.com:repository.git
- Git needs to be installed on Jenkins Worker
- Pyhton 3 needs to installed on Jenkins worker
- Rsync needs to be installed on Jenkins worker
