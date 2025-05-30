#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['3.92.48.63', '44.202.237.194']  
env.user = 'ubuntu'
# env.key_filename = '~/.ssh/id_rsa

def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not exists(archive_path):
        return False

    try:
        # Upload archive
        put(archive_path, "/tmp/")

        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]
        release_path = f"/data/web_static/releases/{folder_name}"

        # Create target directory
        run(f"mkdir -p {release_path}")

        # Uncompress archive
        run(f"tar -xzf /tmp/{file_name} -C {release_path}")

        # Remove archive
        run(f"rm /tmp/{file_name}")

        # Move contents
        run(f"mv {release_path}/web_static/* {release_path}")
        run(f"rm -rf {release_path}/web_static")

        # Update symbolic link
        run("rm -rf /data/web_static/current")
        run(f"ln -s {release_path} /data/web_static/current")

        print("New version deployed!")
        return True
    except Exception as e:
        print(f"Deployment failed: {str(e)}")
        return False
