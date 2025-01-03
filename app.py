from api import chat, user
from db import config, db
from flask import Flask
import git


app = Flask(__name__)

app.config.from_object(config.Config)

db.db.init_app(app)

app.register_blueprint(chat.chat_route, url_prefix='/chat')
app.register_blueprint(user.user_route, url_prefix='/user')


@app.route('/git-update', methods=['POST'])
def git_update():
    repo = git.Repo("./macc-project-python")
    origin = repo.remotes.origin
    repo.create_head("main", origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return "", 200


@app.route('/')
def hello_world():
    return 'Hello world!'


if __name__ == '__main__':
    app.run(port=8000, debug=True)
