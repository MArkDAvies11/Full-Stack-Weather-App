import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host='127.0.0.1')