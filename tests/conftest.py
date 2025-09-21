import os

def pytest_configure():
    os.environ.setdefault("ENV", "test")