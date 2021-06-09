class Routes(object):
    def __init__(self, app, request, db):
        self.set_routes(app, request, db)

    def set_routes(self, app, db):
        @app.route("/category", methods=["GET", "POST"])
        @app.route("/category/<category_id>", methods=["GET", "PUT", "DELETE"])
        def category(category_id=None):
            resource = CategoryResource(db)
            return resource.process_request(request, category_id=category_id)
        def category_route(app):
  