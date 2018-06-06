from flask import Flask, url_for, redirect, session
import projectgiphy.configs

# Load configuration elements first based off of config of ENV
app = Flask(__name__)
app.debug = configs.DEBUG
app.secret_key = configs.SECRET_KEY
app.database = configs.DATABASE_URI
app.url_map.strict_slashes = False
app.config.update(GOOGLE_LOGIN_CLIENT_ID=configs.GOOGLE_LOGIN_CLIENT_ID,
                  GOOGLE_LOGIN_CLIENT_SECRET=configs.GOOGLE_LOGIN_CLIENT_SECRET,
                  GOOGLE_LOGIN_REDIRECT_URI=configs.GOOGLE_LOGIN_REDIRECT_URI,
                  GOOGLE_LOGIN_SCOPES=configs.GOOGLE_LOGIN_SCOPES,
                  GIPHY_KEY=configs.GIPHY_KEY)

# Initialize views
import projectgiphy.views


if __name__ == "__main__":
    app.run()