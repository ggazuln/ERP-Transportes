import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Lucianoga18.'
    SQLALCHEMY_DATABASE_URI = 'postgresql://devuser:123qweasd.@localhost:5432/bd_transportes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Configuración de Email para reseteo de contraseña ---
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'gabriel.gazuln@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'fphk arko fukn kkke ' # ¡CUIDADO! Es mejor usar siempre variables de entorno para contraseñas.
    MAIL_DEFAULT_SENDER = ('Admin Transportes', MAIL_USERNAME)
