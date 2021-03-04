from app import create_app
from flask_pwa import PWA
from flask_session import Session
from flask_wtf.csrf import CsrfProtect
app = create_app()

Session(app)
PWA(app)
CsrfProtect(app)

app.run(debug=True, host="0.0.0.0", port="5000")