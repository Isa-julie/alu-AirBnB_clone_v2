#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run
from os.path import exists

# Updated with your actual server IPs
env.hosts = ['3.92.48.63', '44.202.237.194']  # web-01 and web-02
env.user = 'ubuntu'
# Note: The load balancer (54.167.27.17) is not included as we deploy to web servers

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path (str): Path to the archive to be deployed.

    Returns:
        bool: True if all operations were successful, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/
        put(archive_path, "/tmp/")

        # Get the base filename without extension
        filename = archive_path.split("/")[-1]
        foldername = filename.split(".")[0]
        release_path = f"/data/web_static/releases/{foldername}"

        # Create the release directory
        run(f"mkdir -p {release_path}")

        # Uncompress the archive
        run(f"tar -xzf /tmp/{filename} -C {release_path}")

        # Remove the archive from /tmp/
        run(f"rm /tmp/{filename}")

        # Move contents to proper location
        run(f"mv {release_path}/web_static/* {release_path}")
        run(f"rm -rf {release_path}/web_static")

        # Update the symbolic link
        run("rm -rf /data/web_static/current")
        run(f"ln -s {release_path} /data/web_static/current")

        print("New version deployed successfully!")
        return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False