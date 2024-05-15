from app import create_app
from app.config import TestConfig

testApp = create_app(TestConfig)