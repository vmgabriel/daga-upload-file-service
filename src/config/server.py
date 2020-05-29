# Develop Vmgabriel

import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

def mbToBytes(byte_data):
    return byte_data * 1048576

def get_public_path():
    return str(Path(__file__).resolve().parent.parent.parent)

print('carpeta publica - ', get_public_path())

configuration = {
    'host': '0.0.0.0',
    'port': 7201,

    'debug': True,

    'files_path_upload': get_public_path() + '/public/',
    'files_path_images_upload': get_public_path() + '/public/images/',
    'max_length_files': mbToBytes(5),

    'cookie_secret': os.getenv('COOKIE_SECRET'),
    'cookie_name': os.getenv('COOKIE_NAME'),

    'jwt_location': ['cookies'],
    'jwt_secret': os.getenv('JWT_SECRET'),

    'verify_ip': False, # True | False
}
