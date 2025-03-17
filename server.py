import os

from app import app
if __name__ == "__main__":
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5502))
    # works = int(os.getenv('WORKERS', 8))

    # Gunicorn 실행 명령어
    # cmd = f"gunicorn --timeout=120 --bind {host}:{port} -w {works} --preload app.app:app"
    cmd = f"gunicorn --timeout=120 --bind {host}:{port} --preload app.app:app"

    os.system(cmd)
