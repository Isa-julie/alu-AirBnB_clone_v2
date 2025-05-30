#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from fabric.api import env, put, run, sudo
from os.path import exists

env.hosts = ['3.92.48.63', '44.202.237.194']  # Your actual server IPs
env.user = 'ubuntu'
# env.key_filename = '~/.ssh/id_rsa'  # Uncomment if using SSH key


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    
    Args:
        archive_path: Path to the archive to deploy
        
    Returns:
        True if all operations succeeded, False otherwise
    """
    if not exists(archive_path):
        return False

    try:
        # Upload archive
        put(archive_path, "/tmp/")

        # Extract archive filename and folder name
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]
        release_path = "/data/web_static/releases/{}".format(folder_name)

        # Create target directory
        run("mkdir -p {}".format(release_path))

        # Uncompress archive
        run("tar -xzf /tmp/{} -C {}".format(file_name, release_path))

        # Remove archive
        run("rm /tmp/{}".format(file_name))

        # Move contents and remove web_static folder
        run("mv {}/web_static/* {}".format(release_path, release_path))
        run("rm -rf {}/web_static".format(release_path))

        # Update symbolic link
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed:", str(e))
        return False