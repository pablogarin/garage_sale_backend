create_script="from api.api import create_flask_app; from api.db.database import db; app = create_flask_app(); app.app_context().push(); db.create_all()"

python -c "$create_script"
