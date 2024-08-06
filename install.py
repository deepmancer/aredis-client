from setuptools.command.install import install
import subprocess
import sys

class InstallCommand(install):    
    def run(self):
        result = subprocess.run([sys.executable, '-m', 'pytest', '-v'], check=True)
        if result.returncode != 0:
            sys.exit(result.returncode)
        install.run(self)
