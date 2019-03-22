import os
import sys

basedir = os.path.abspath(os.path.dirname(__file__))

# Fleet Defines
FLEET_PROD = 'Prod'
FLEET_TEST = 'Test'
FLEET_DEVELOPMENT = "Development"


class Config:
    APPLICATION_ROOT = '/Users/zhaoye/Workspace/NoteWiki/'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class TestConfig(Config):
    # SQL Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/zhaoye/Workspace/NoteWiki/scripts/NoteWiki.db'


configs = {
    FLEET_TEST : TestConfig
}