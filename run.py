from views import main
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8000/')
        make_server('', 8000, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')
