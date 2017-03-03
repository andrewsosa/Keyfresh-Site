###############
### imports ###
###############

from fabric.api import cd, env, lcd, put, prompt, local, sudo, run
from fabric.contrib.files import exists

##############
### config ###
##############

from config.fabconfig import *
# local_app_dir = './'
# local_config_dir = './config'
#
# remote_app_dir = '/home/keyfresh/site'
# remote_git_dir = '/var/repo'
# remote_repo_name = '/keyboard-site.git'
# remote_flask_dir = remote_app_dir + '/flask'
# remote_nginx_dir = '/etc/nginx/sites-enabled'
# remote_supervisor_dir = '/etc/supervisor/conf.d'
#
# env.hosts = ['104.131.20.188']  # replace with IP address or hostname
# env.user = 'keyfresh'
# # env.password = 'blah!'

chown = 'chown -R {0}:{0} '.format(env.user)

#############
### tasks ###
#############

def setup_env():
    """ Install required packages. """
    # system dependencies
    sudo('apt update')
    sudo('apt install -y python')
    sudo('apt install -y python-pip')
    sudo('apt install -y python-virtualenv')
    sudo('apt install -y nginx')
    sudo('apt install -y git')

    # node dependencies
    sudo('apt install -y npm')
    sudo('apt install -y nodejs-legacy')
    sudo('npm install -g gulp')

def setup_libs():
    with cd(remote_app_dir):
        sudo('npm install')
        sudo('npm install gulp')
        sudo(chown + 'node_modules/')

def configure_dirs():
    """  Create remote project directories """
    if exists(remote_app_dir) is False:
        sudo('mkdir ' + remote_app_dir)
        sudo(chown + remote_app_dir)

def wipe_nginx_config():
    """ Erase the nginx server configuration """
    if exists(nginx_enabled):
        sudo('rm ' + nginx_enabled)
    if exists(nginx_available):
        sudo('rm ' + nginx_available)

def configure_nginx():
    """ Set up remote nginx configuration
    1. Remove old nginx config
    2. Create new config file
    3. Setup new symbolic link
    4. Copy local config to remote config
    5. Restart nginx
    """
    wipe_nginx_config()
    if exists(nginx_enabled) is False:
        sudo('touch ' + nginx_available)
        sudo('ln -s '+ nginx_available + ' ' + nginx_enabled)
    with lcd(local_config_dir):
        # with cd(nginx_available):
        put(nginx_name, nginx_available, use_sudo=True)
    sudo('systemctl restart nginx')

def configure_git():
    """
    1. Create updated post-receive hook
    2. Setup bare Git repo
    3. Create post-receive hook
    4. Make sure we own directories
    """
    # create a new hook
    # setup bare repo
    if not exists(remote_git_dir):
        sudo('mkdir ' + remote_git_dir)
    if exists(remote_repo_dir):
        sudo ('rm -rf ' + remote_repo_dir)
    with cd(remote_git_dir):
        sudo('mkdir ' + remote_repo_name)
        with cd(remote_repo_name):
            sudo('git init --bare')
            # add hook
            with lcd(local_config_dir):
                local('echo \'' + post_receive_template + '\'> ./post-receive')
                with cd('hooks'):
                    put('./post-receive', './', use_sudo=True)
                    sudo('chmod +x post-receive')
    # make sure our user has permissions
    sudo(chown + remote_repo_dir)


def deploy_code():
    """ Pushes changes to production. """
    sudo(chown + remote_app_dir)
    with lcd(local_app_dir):
        local('git push production master')
    sudo(chown + remote_app_dir)

def build_static():
    """ Rebuilds static resources on server. """
    with cd(remote_app_dir):
        sudo('gulp build')

def deploy():
    """
    1. Upload new app files
    2. Update app requirements
    3. Build static resources
    """
    with lcd(local_app_dir):
        deploy_code()
        setup_libs()
        build_static()

def rollback():
    """ Revert to previous version.
    1. Quick rollback in case of error
    2. Restart gunicorn via supervisor
    """
    with lcd(local_app_dir):
        local('git revert master  --no-edit')
        local('git push production master')
        sudo('supervisorctl restart keyfresh-site')

def create():
    """Init completely fresh server instance. """
    # Configuration
    setup_env()
    configure_git()
    configure_nginx()
    configure_dirs()

    # Deploy
    # deploy_code()
    # setup_libs()
    # build_static()
