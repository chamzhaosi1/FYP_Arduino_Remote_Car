from flask import Flask, render_template, request
import ssl, argparse
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
   parser = argparse.ArgumentParser(
      description="WebRTC audio / video / data-channels demo"
   )
   parser.add_argument("--cert-file", help="SSL certificate file (for HTTPS)")
   parser.add_argument("--key-file", help="SSL key file (for HTTPS)")
   args = parser.parse_args()

   ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
   ssl_context.load_cert_chain(args.cert_file, args.key_file)
   app.run(host='0.0.0.0',port=8080, debug=False, ssl_context=ssl_context)