#!/usr/bin/python3
"""
Fabric script that generates a tgz archive from the contents of the web_static
folder of the AirBnB Clone repo
"""

import os
from datetime import datetime
from fabric.api import local

def do_pack():
    """
    Generates a tgz archive from the contents of the web_static folder.
    
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
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    do_pack()
