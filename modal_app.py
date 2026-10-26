import modal

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir("app", remote_path="/root/app")
)

app = modal.App("rcra-dot-compliance")

@app.function(
    image=image,
    secrets=[
        modal.Secret.from_name("meta-model-api"),
        modal.Secret.from_name("inference-keys"),
    ],
    timeout=300,
)
@modal.asgi_app()
def fastapi_app():
    from app.main import app as web_app
    return web_app
