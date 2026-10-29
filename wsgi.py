"""WSGI entry point for hosted preview deployments."""
from app import create_app

app = create_app()
