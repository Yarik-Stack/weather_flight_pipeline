from sqlalchemy import create_engine
from utils import load_env_vars


#----------------------------- CONNECTING TO THE DATABASE ----------------------
def database_connection():
    env = load_env_vars()
    connection_string = (f"mysql+pymysql://{env['DB_USER']}:{env['DB_PASSWORD']}@{env['DB_HOST']}:{env['DB_PORT']}/{env['DB_NAME']}")
    engine = create_engine(connection_string)
    return {
        'connection_string': connection_string,
        'engine': engine
    }