#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env, cd
from os.path import exists

env.hosts = ['142.44.167.228', '144.217.246.195']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path (str): The path to the archive file to be deployed.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        remote_path = "/data/web_static/releases/"

        # Upload the archive to the server's /tmp directory
        put(archive_path, '/tmp/')

        # Create the release directory and extract the archive
        with cd(remote_path):
            run('mkdir -p {}/{}'.format(remote_path, no_ext))
            run('tar -xzf /tmp/{} -C {}/{}'.format(file_name, remote_path, no_ext))

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

if __name__ == "__main__":
    # Example usage: deploy an archive by specifying its path
    archive_path = "your_archive_path_here.tgz"
    do_deploy(archive_path)
