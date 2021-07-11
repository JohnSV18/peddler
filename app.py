from app.extensions import app
from app.main.routes import main
from app.auth.auth_routes import auth

app.register_blueprint(main)
app.register_blueprint(auth)


if (__name__ == "__main__"):
    app.run(debug=True)
