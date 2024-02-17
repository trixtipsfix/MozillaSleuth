import platform
import os
import hashlib
import datetime

class general():
    def __init__(self):
        self.platform_name = platform.system().lower()
        self.user_home = os.path.expanduser("~")

    def set_profiles_path(self, path):
        self.profiles_path = path

    def validate_simple_date_format(self, date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y/%m/%d')
            return True
        except ValueError:
            return False
    
    def sha256sum(self, filepath):
        h  = hashlib.sha256()
        b  = bytearray(128*1024)
        mv = memoryview(b)
        with open(filepath, 'rb', buffering=0) as f:
            for n in iter(lambda : f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()

    def md5sum(self, filepath):
        BLOCKSIZE = 65536
        hasher = hashlib.md5()
        with open(filepath, 'rb') as source:
            buf = source.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = source.read(BLOCKSIZE)
        return hasher.hexdigest()

    def sha1sum(self, filepath):
        hasher = hashlib.sha1()
        with open(filepath, 'rb') as source:
            block = source.read(2**16)
            while len(block) != 0:
                hasher.update(block)
                block = source.read(2**16)
        return hasher.hexdigest()

    def file_fingerprint(self, filepath):
        output = {
            'md5' : self.md5sum(filepath),
            'sha1' : self.sha1sum(filepath),
            'sha256' : self.sha256sum(filepath)
        }
        return output

    def fingerprint(self, profile_path):
        output = {}
        for (name, filename) in self.config['files'].items():
            if os.path.isfile(os.path.join(profile_path, filename)):
                output[filename] = self.file_fingerprint(os.path.join(profile_path, filename))
        return output