""" Main app """
from flask import Flask, jsonify, request, make_response

from src.infra.client.S3Client import S3Client
import uuid

app = Flask(__name__)

s3_client = S3Client()

@app.route('/health')
def get_health():
    """ Returns message to perform a system health check"""
    return "OK"


@app.route('/file', methods=['POST'])
def store_file():
    """ Receive and store a file """
    
    f = request.files['file']
    file_id = str(uuid.uuid4())

    s3_client.upload(f, file_id + '.pdf')

    return jsonify({'message': 'stored', 'fileName': file_id}), 201

@app.route('/file/<_id>', methods=['GET'])
def retrieve_file(_id: str):
    """ Retrieve a file from storage """
    
    binary_pdf = s3_client.download(_id + '.pdf')
    
    response = make_response(binary_pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
        'inline; filename=%s.pdf' % 'yourfilename'

    return response

@app.route('/file/<_id>', methods=['DELETE'])
def delete_file(_id: str):
    """ Remove a file from storage """
    
    s3_client.remove(_id + '.pdf')

    return jsonify({'message': 'stored', 'fileName': _id}), 200


print("Starting Files Service")
print("----------------------------------------------------")
