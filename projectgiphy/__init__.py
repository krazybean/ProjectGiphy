from flask import Flask
import projectgiphy.configs

# Load configuration elements first based off of config of ENV
app = Flask(__name__)
app.debug = configs.DEBUG
app.secret_key = configs.SECRET_KEY
app.database = configs.DATABASE_URI

# Initialize views
import projectgiphy.views


if __name__ == "__main__":
    app.run()