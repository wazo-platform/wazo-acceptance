import os
import sys
from lettuce import world

ASSET_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "assets"
    )
)

def copy_asset_to_server(asset, serverpath):
    assetpath = os.path.join(ASSET_PATH, asset)
    world.ssh_client_xivo.send_files(assetpath, serverpath)

