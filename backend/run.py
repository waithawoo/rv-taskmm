# This is just to run the app with `python run.py` for development purpose without using docker.
from uvicorn import run

if __name__ == '__main__':
    app_import_string = 'src.main:app'

    run(
        app=app_import_string,
        host='127.0.0.1',
        port=8000,
        reload=True,
    )
