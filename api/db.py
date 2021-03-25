import os


def getDbName(basepath, username):
    HOME_DIR = os.path.join(basepath, 'users', username)
    data_dir = os.path.join(HOME_DIR, 'data')
    mtime = lambda f: os.stat(os.path.join(data_dir, f)).st_mtime
    filename = list(sorted(os.listdir(data_dir), key=mtime))[-1]
    name, ext = os.path.splitext(filename)
    name = os.path.split(name)[-1] + "_" + ext[1:]
    if type(name) == list:
        name = [n for n in name if not n.startswith('.')]
    db_name = username + '_' + name.replace(" ", "_")
    return db_name


