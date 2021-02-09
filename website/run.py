from app import create_app
from flask_pwa import PWA

app = create_app()

PWA(app)

app.run(debug=True, host="0.0.0.0", port="5000")