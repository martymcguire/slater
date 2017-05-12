from flask import Blueprint, request, session, redirect, current_app, jsonify
from .auth import login_required
import requests

api = Blueprint('api', __name__)

@api.route('/publish/media', methods=['POST'])
@login_required
def publish_media():
    endpoint = session.get('_micropub_config')['media-endpoint']

    # pass along file upload, if present. otherwise fail!
    files = {}
    if 'file' in request.files:
        f = request.files['file']
        if f.filename != '':
            files['file'] = (f.filename, f.stream, f.mimetype)
            headers = { 'Authorization': "Bearer %s" % session.get('_micropub_access_token') }
            current_app.logger.debug(['Media:', endpoint, headers, files])
            r = requests.post(endpoint, headers=headers, files=files)
            if (r.status_code == requests.codes.created) or (r.status_code == requests.codes.accepted):
              return jsonify({
                'location': r.headers.get('location')
              })
            else:
              return jsonify({
                'error': "Micropub endpoint did not return a Location. %s" % r.text
              })
    return jsonify({ 'error': "No file named 'file' was attached." })

@api.route('/publish', methods=['POST'])
@login_required
def publish():
    endpoint = session.get('_micropub_endpoint')

    # pass along file uploads, if present
    files = {}
    for file_key in ['audio','photo']:
      if file_key in request.files:
        f = request.files[file_key]
        if f.filename != '':
          # TODO: if media endpoint, upload there and replace value w/ URL
          # otherwise, pass the file along to the micropub endpoint
          files[file_key] = (f.filename, f.stream, f.mimetype)

    # TODO: data validation?

    # iterate over keys to allow multiple values from Flask multidict
    data = {}
    for k in request.form.keys():
      values = request.form.getlist(k)
      if values != ['']:
        data[k] = [v for v in values if v != '']

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
