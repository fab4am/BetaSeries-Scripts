
if __name__ == '__main__':
    from options import getOption
    from webapp import app
    app.run(host=getOption('flask.host'), debug=getOption('flask.debug'))