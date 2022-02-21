# yaapr
Yet another Ansible playbook runner is a utility which allows you to specific multiple playbook repositories and automate running them in a specific order.

## Purpose

I needed a way to run playbooks in a layered/ordered fashion on localhost, with logged output for troubleshooting. It needs to be robust enough to run from a pre-cached directory for offline scenarios (air-gapped systems, kickstart, etc).

On an initial run it clones the git repositories specified in the ini file into a local cache, checks out the branch/tag specified, and then uses ansible-playbook to run them on the local host (-i localhost, -c local --check). Playbook stdout and stderr are captured and logged, as well as details about the execution. On subsequent runs yaapr will attempt to run git pull on the cached repos.

Playbooks are run in order of priority. Sections names must be unique.

Example:

```ini
[DEFAULT]
cachedir = /var/lib/yaapr/cache
logdir = /var/log/yaapr
branch = main
play = main.yml
config = ansible.cfg
skip_tags = exempt,ioheavy,notimplemented

[disa-stig]
priority = 1
logfile = disa-stig.log
repo_url = https://github.com/tazerdev/disa-stig.git
play = local.yml

[org-scp]
priority = 2
logfile = org-scp.log
repo_url = https://your.org.scp/repo.git
branch = production
```

Run with the above ini the disa-stig playbook repo will be cloned, the main branch checked out and the local.yml playbook will be run. The value of skip_tags from the DEFAULT section will be passed to ansible and stdout/stderr will be logged to /var/log/yaapr/disa-stig.log. Next the org-scp playbook will be cloned and the production branch checked out, and then the main.yml playbook will be run.
