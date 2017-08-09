from configparser import ConfigParser
import os.path


def load(profile='default'):
    config = ConfigParser()

    for path in ['credentials', '~/.waggle/credentials']:
        try:
            config.read(os.path.expanduser(path))
            return dict(config[profile])
        except FileNotFoundError:
            continue

    raise RuntimeError('no credentials file found')
