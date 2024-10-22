from dracan.core.app_factory import create_app

app = create_app()

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)