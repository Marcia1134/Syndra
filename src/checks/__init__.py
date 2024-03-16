from checks import check_env, check_db, check_db_commands

def env():
    try:
        check_env.main()
    except ValueError as e:
        print(e)
        exit(1)

def db():
    try:
        check_db.main()
    except ValueError as e:
        print(e)
        exit(1)

def commands(commands):
    try:
        check_db_commands.main(commands=commands)
    except ValueError as e:
        print(e)
        exit(1)

# Path: src/checks/__init__.py