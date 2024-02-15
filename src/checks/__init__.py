from checks import check_env

def env():
    print('Checking Environment Variables')
    try:
        check_env.main()
    except ValueError as e:
        print(e)
        exit(1)

# Path: src/checks/__init__.py