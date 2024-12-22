from core.app import create_app
import modal

# Define the Modal image
image = modal.Image.debian_slim(python_version="3.12").pip_install_from_requirements("core/requirements.txt")

# Create the stub (Modal equivalent of the app definition)
app = modal.App("linkedin-games-solver")

# Define the Modal function
@app.function(image=image)
@modal.wsgi_app()
def run_app():
    app = create_app()
    return app
