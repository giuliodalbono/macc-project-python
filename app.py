from flask import Flask
import git

app = Flask(__name__)


@app.route('/git-update', methods=['POST'])
def git_update():
    repo = git.Repo("./macc-project-python")
    origin = repo.remotes.origin
    repo.create_head("main", origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return "", 200


@app.route('/')
def hello_world():  # put application's code here
    return 'Final test, githook works!'


if __name__ == '__main__':
    app.run()
