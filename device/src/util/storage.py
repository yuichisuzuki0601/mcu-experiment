class Storage:
    _FILENAME = '.storage'

    def __init__(self):
        self._data = {}
        try:
            with open(Storage._FILENAME, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, val = line.strip().split('=', 1)
                        self._data[key] = val
        except OSError:
            pass

    def _save(self, prefix, key, value):
        self._data[f'{prefix}.{key}'] = str(value)
        with open(Storage._FILENAME, 'w') as f:
            for k, v in self._data.items():
                f.write(f'{k}={v}\n')

    def get_config(self, key):
        return self._data.get(f'config.{key}')

    def set_config(self, key, val):
        self._save('config', key, val)

    def get_state(self, key):
        return self._data.get(f'state.{key}')

    def set_state(self, key, val):
        self._save('state', key, val)
