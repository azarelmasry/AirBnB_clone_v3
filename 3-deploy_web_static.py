#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists
import os

env.hosts = ['142.44.167.228', '144.217.246.195']


def do_pack():
    """
    Generates a tgz archive of the web_static folder.

    Returns:
        str: The file path of the generated archive, or None on failure.
    """
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_dir = "versions"
        
        if not os.path.exists(archive_dir):
            os.mkdir(archive_dir)
        
        file_name = f"{archive_dir}/web_static_{date}.tgz"
        source_dir = "web_static"
        
        local(f"tar -cvzf {file_name} {source_dir}")
        
        return file_name
    except Exception as e:
        print(f"An error occurred during archive creation: {e}")
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path (str): The path to the archive file to be deployed.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not exists(archive_path):
        print(f"Archive {archive_path} not found on the local machine.")
        return False

    try:
        file_name = os.path.basename(archive_path)
        no_ext = os.path.splitext(file_name)[0]
        remote_path = "/data/web_static/releases/"

        # Upload the archive to the server's /tmp directory
        put(archive_path, '/tmp/')

        # Create the release directory and extract the archive
        run('mkdir -p {}/{}'.format(remote_path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, remote_path, no_ext))

        # Remove the uploaded archive
        run('rm /tmp/{}'.format(file_name))

        # Move the contents to the web_static directory
        run('mv {0}{1}/web_static/* {0}{1}/'.format(remote_path, no_ext))

        # Remove the redundant web_static directory
        run('rm -rf {}{}/web_static'.format(remote_path, no_ext))

        # Update the symbolic link to the new release
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(remote_path, no_ext))

        return True

    except Exception as e:
        print(f"An error occurred during deployment: {e}")
        return False


def deploy():
    """
    Creates and distributes an archive to the web servers.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
