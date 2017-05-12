from flask import Blueprint, request, session, redirect, current_app, jsonify
from .auth import login_required
import requests

api = Blueprint('api', __name__)
FILE_ATTRS = ('audio','photo','video')

def send_file_to_media_endpoint(f):
    if 'media-endpoint' in session.get('_micropub_config'):
        endpoint = session.get('_micropub_config')['media-endpoint']
    else:
        # no media endpoint configured
        return None
    files = {}
    if f.filename != '':
        files['file'] = (f.filename, f.stream, f.mimetype)
        headers = { 'Authorization': "Bearer %s" % session.get('_micropub_access_token') }
        current_app.logger.debug(['Media:', endpoint, headers, files])
        r = requests.post(endpoint, headers=headers, files=files)
        if (r.status_code == requests.codes.created) or (r.status_code == requests.codes.accepted):
            return r.headers.get('location')
        else:
            current_app.logger.error("Micropub endpoint did not return a Location. %s" % r.text)
    return None

@api.route('/publish/media', methods=['POST'])
@login_required
def publish_media():
    # pass along file upload, if present. otherwise fail!
    if 'file' in request.files:
        f = request.files['file']
        url = send_file_to_media_endpoint(f)
        if url is None:
            return jsonify({ 'error': "Error uploading to media endpoint." })
        return jsonify({
            'location': url
        })
    return jsonify({ 'error': "No file named 'file' was attached." })

@api.route('/publish', methods=['POST'])
@login_required
def publish():
    endpoint = session.get('_micropub_endpoint')

    # iterate over keys to allow multiple values from Flask multidict
    data = {}
    for k in request.form.keys():
      values = request.form.getlist(k)
      if values != ['']:
        data[k] = [v for v in values if v != '']

    # pass along file uploads, if present
    files = {}
    for file_key in FILE_ATTRS:
        if file_key in request.files:
            f = request.files[file_key]
            if f.filename != '':
                url = send_file_to_media_endpoint(f)
                if url is None:
                    # Missing or problem sending to media endpoint. Pass along the file.
                    files[file_key] = (f.filename, f.stream, f.mimetype)
                    return jsonify({ 'error': "Error uploading to media endpoint." })
                else:
                    data[file_key + '[]'] += [url]

    # TODO: data validation?

    headers = { 'Authorization': "Bearer %s" % session.get('_micropub_access_token') }

    current_app.logger.debug([endpoint, headers, data, files])

    # DEBUG: DISABLE FOR DEBUG TIMES
    r = requests.post(
      endpoint,
      data=data,
      headers=headers,
      files=files
    )
    # DEBUG ONLY
    #return "<pre>%s</pre><pre>%s</pre><pre>%s</pre><pre>%s</pre>" % (endpoint, headers, data, files)

    # check for a 201 or 202 and Location: header for success
    # redirect to Location!
    if (r.status_code == requests.codes.created) or (r.status_code == requests.codes.accepted):
      return redirect(r.headers.get('location'))
    else:
      return "Micropub endpoint did not return a Location. %s" % r.text
