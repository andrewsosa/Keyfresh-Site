###############
### imports ###
###############

from fabric.api import cd, env, lcd, put, prompt, local, sudo
from fabric.contrib.files import exists

##############
### config ###
##############

from fabconfig import *
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
    sudo('apt update')
    sudo('apt install -y python')
    sudo('apt install -y python-pip')
    sudo('apt install -y python-virtualenv')
    sudo('apt install -y nginx')
    sudo('apt install -y gunicorn')
    sudo('apt install -y supervisor')
    sudo('apt install -y git')
    sudo('apt install -y npm')
    sudo('apt install -y nodejs-legacy')


def setup_libs():
    with cd(remote_app_dir):
        sudo('pip install -r requirements.txt')
        sudo('npm install -g gulp')
        sudo('npm install')
        sudo(chown + 'node_modules/')

def configure_dirs():
    """
    1. Create project directories
    2. Create and activate a virtualenv
    3. Copy Flask files to remote host
    """
    if exists(remote_app_dir) is False:
        sudo('mkdir ' + remote_app_dir)
    if exists(remote_flask_dir) is False:
        sudo('mkdir ' + remote_flask_dir)
    with lcd(local_app_dir):
        with cd(remote_app_dir):
            sudo('virtualenv env')
            sudo('source env/bin/activate')
        # with cd(remote_flask_dir):
        #     put('*', './', use_sudo=True)
    sudo(chown + remote_app_dir)

def wipe_nginx_config():
    if exists('/etc/nginx/sites-enabled/keyfresh-site'):
        sudo('rm /etc/nginx/sites-enabled/keyfresh-site')
        sudo('rm /etc/nginx/sites-available/keyfresh-site')


def configure_nginx():
    """
    # 1. Remove default nginx config file
    2. Create new config file
    3. Setup new symbolic link
    4. Copy local config to remote config
    5. Restart nginx
    """
    # sudo('/etc/init.d/nginx start')
    # if exists('/etc/nginx/sites-enabled/default'):
    #     sudo('rm /etc/nginx/sites-enabled/default')
    if exists('/etc/nginx/sites-enabled/keyfresh-site') is False:
        sudo('touch /etc/nginx/sites-available/keyfresh-site')
        sudo('ln -s /etc/nginx/sites-available/keyfresh-site' +
             ' /etc/nginx/sites-enabled/keyfresh-site')
    with lcd(local_config_dir):
        with cd(remote_nginx_dir):
            put('./keyfresh-site', './', use_sudo=True)
    sudo('/etc/init.d/nginx restart')


def configure_supervisor():
    """
    1. Create new supervisor config file
    2. Copy local config to remote config
    3. Register new command
    """
    if exists('/etc/supervisor/conf.d/keyfresh-site.conf'):
        with cd(remote_supervisor_dir):
            sudo('rm ./keyfresh-site.conf')

    with lcd(local_config_dir):
        with cd(remote_supervisor_dir):
            put('./keyfresh-site.conf', './', use_sudo=True)
            sudo('supervisorctl reread')
            sudo('supervisorctl update')


def configure_git():
    """
    1. Setup bare Git repo
    2. Create post-receive hook
    """
    if exists(remote_git_dir):
        sudo ('rm -rf ' + remote_git_dir)
    sudo('mkdir ' + remote_git_dir)
    with cd(remote_git_dir):
        sudo('mkdir keyfresh-site.git')
        with cd('keyfresh-site.git'):
            sudo('git init --bare')
            with lcd(local_config_dir):
                with cd('hooks'):
                    put('./post-receive', './', use_sudo=True)
                    sudo('chmod +x post-receive')
    # make sure our user has permissions
    sudo(chown + remote_git_dir + remote_repo_name)

def run_app():
    """ Run the app! """
    with cd(remote_flask_dir):
        sudo('supervisorctl start keyfresh-site')

def deploy_code():
    """ Pushes changes to production. """
    with lcd(local_app_dir):
        local('git push production master')

def build_static():
    """ Rebuilds static resources on server. """
    with cd(remote_app_dir):
        sudo('gulp build')

def deploy():
    """
    1. Upload new app files
    2. Update app requirements
    3. Build static resources
    4. Restart gunicorn via supervisor
    """
    with lcd(local_app_dir):
        deploy_code()
        setup_libs()
        build_static()
        sudo('supervisorctl restart keyfresh-site')


def rollback():
    """
    1. Quick rollback in case of error
    2. Restart gunicorn via supervisor
    """
    with lcd(local_app_dir):
        local('git revert master  --no-edit')
        local('git push production master')
        sudo('supervisorctl restart keyfresh-site')


def status():
    """ Is our app live? """
    sudo('supervisorctl status')


def create():
    # Configuration
    setup_env()
    configure_git()
    configure_nginx()
    configure_supervisor()
    configure_dirs()

    # Deploy w/o running
    deploy_code()
    setup_libs()
    build_static()
