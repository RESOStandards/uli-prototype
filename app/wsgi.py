from application import create_app
from application.config import *

app = create_app(config.DevConf)

if __name__ == "__main__":
    app.run(host='0.0.0.0')