# ddl-vector-http-app
Little Flask app that lets you change some settings in Vector.

## Usage

`git clone https://github.com/kercre123/ddl-vector-http-app.git`

`pip install -r ddl-vector-http-app/app/requirements.txt`

`py ddl-vector-http-app/app/web-api.py`

(If you have multiple robots, use `--serial`. Example: `py ddl-vector-http-app/app/web-api.py --serial 00e20145`)

(You may also run in docker and connect with `localhost:8013`)

This will bring up the app. This lets you change some settings inside of Vector. Anything in "Actions" or below do not work without custom dev robot firmware.

1.7 has taken out the extra TTS packages (I assume to save space), so changing the locale won't do much.

For optional features to work, do `pip install -r ddl-vector-http-app/app/opt_requirements.txt`
