from website import create_app

app = create_app()

#if ran from this file
if __name__ == '__main__':
    #run the web server and rerun on changes (debug)
    app.run(debug=True)
    