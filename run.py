from app import create_app

app = create_app()
web: gunicorn run:app

if __name__ == '__main__':
    app.run(debug=True)