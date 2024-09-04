# ps-packager
Packager for PS Projects

Pyhton Utility to create module loadable packages for SugarCRM. Basis are the deltas of two branches in GitHub.
Paramters:
- Sugar Version (-v)
- Base branch in GitHub (-b)
- Target branch in GitHub (-t)
- GitHub Repository, to be provided in the form git@github.com:repository.git (-r)
- Package Name (-a)
- Package Description (-d)
- Package Version (-u)

Example command: 
python3 src/packager.py -t zhinst_1120_phase1_S27 -b zhinst_1120_phase1_S26 -r git@github.com:sugarcrm-ps/ps-dev-zhinst.git -u "1.0" -a "ZHINST Phase 1 S27"



Pre-requisites to use in Jenkins:
- Credentials for GitHub user which has access rights to sugarcrm repositories need to be configured in Jenkins as Username/Password Credentials with ID "GitHub Sugar User"
- GitHub Token for user which has access rights to sugarcrm repositories need to be configured in Jenkins as Secret Text with ID "GitHub Token"
- Git repository needs to be provided in the form git@github.com:repository.git
- Scripts need to be provided in the following folders: customer/upgrade/Target branch name/scripts/php/post and customer/upgrade/Target branch name/scripts/php/pre
- Git needs to be installed on Jenkins Worker
- Pyhton 3 needs to installed on Jenkins worker
- Rsync needs to be installed on Jenkins worker
