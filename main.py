from api.api import create_flask_app


"""
Development runner. For production use Dockerfile or run
python -m gunicorn -c gunicorn.config.py "api.api:create_flask_app()"
"""
if __name__ == "__main__":
    app = create_flask_app()
    app.config["DEBUG"] = True
    app.run(port=5013)
