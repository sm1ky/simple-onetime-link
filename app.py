from src import web
from src.config import PORT

if __name__ == '__main__':
    web.run(host='0.0.0.0', port=PORT)