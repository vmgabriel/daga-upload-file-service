# Develop vmgabriel

# Libraries
import os
from flask import Blueprint, jsonify, request, send_file, send_from_directory, safe_join, abort
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from werkzeug.utils import secure_filename

from src.config.server import configuration

from src.utils.middlewares.validation_handler import verify_cookie

mod = Blueprint('api/uploads', __name__);

def spacesToDataValid(data):
    return '_'.join(data.split(' '))


def allowed_image_filesize(filesize):
    return int(filesize) <= configuration['max_length_files']


def allowed_file_extension(filename):
    allowed_extensions = set(['jpg', 'jpeg', 'gif', 'png'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions


@mod.route('/files/<filename>', methods=['GET'])
def send_file(filename):
    cookie_validation = verify_cookie(
        request.cookies,
        request.remote_addr,
        'upload_file',
        'show'
    )
    if cookie_validation:
        return cookie_validation

    try:
        print('rute - {}{}'.format(configuration['files_path_upload'], filename))
        return send_from_directory(
            './.' + configuration['files_path_upload'],
            filename,
            as_attachment=True
        )
    except FileNotFoundError:
        abort(404)


@mod.route('/files/me/<filename>', methods=['GET'])
def send_image_me(filename):
    cookie_validation = verify_cookie(
        request.cookies,
        request.remote_addr,
        'upload_file',
        'show me'
    )

    if cookie_validation and type (cookie_validation) != 'string':
        return cookie_validation

    try:
        return send_from_directory(
            configuration['files_path_images_upload'],
            filename,
            as_attachment=True
        )
    except FileNotFoundError:
        abort(404)


# Define Route for Upload of Files
@mod.route('/files', methods=['POST'])
def upload_files():
    cookie_validation = verify_cookie(
        request.cookies,
        request.remote_addr,
        'upload_file',
        'create'
    )
    if cookie_validation:
        return cookie_validation

    if request.files:
        if not allowed_image_filesize(request.headers['Content-Length']):
            print("Filesize exceeded maximum limit")
            return jsonify({
                'code': 400,
                'message': 'you have exceeded the maximum file size limit.'
            }), 400

        files = request.files.getlist('files')
        for file in files:
            print(file)
            filename = secure_filename(spacesToDataValid(file.filename))
            file.save(os.path.join(configuration['files_path_upload'], filename))

        return jsonify({ 'code': 201, 'message': 'File Upload Successfully' }), 201
    else:
        return jsonify({ 'code': 400, 'message': 'Not files' }), 400


# Define Route Base
@mod.route('/image/me', methods=['POST'])
def upload_image():
    cookie_validation = verify_cookie(
        request.cookies,
        request.remote_addr,
        'upload_file',
        'create me'
    )

    if cookie_validation and type (cookie_validation) != 'string':
        return cookie_validation

    if request.files:
        if not allowed_image_filesize(request.headers['Content-Length']):
            print("Filesize exceeded maximum limit")
            return jsonify({
                'code': 400,
                'message': 'you have exceeded the maximum file size limit.'
            }), 400

        image = request.files('image')
        if not allowed_file_extension(image.filename):
            return jsonify({ 'code': 400, 'message': 'Extension not valid' }), 400

        filename = secure_filename(spacesToDataValid(image.filename))
        file.save(os.path.join(configuration['files_path_images_upload'], cookie_validation))

        return jsonify({ 'code': 201, 'message': 'File Upload Successfully' }), 201
    else:
        return jsonify({ 'code': 400, 'message': 'Not files' }), 400
