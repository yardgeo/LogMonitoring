from setuptools import setup

setup(
    name='http_log_monitoring',
    version='1.0',
    packages=['dto', 'dto.stats', 'utils', 'hadnlers', 'hadnlers.stats', 'hadnlers.alerts', 'consumers', 'producers',
              'exceptions', 'generators', 'test_utils'],
    package_dir={'': 'http_log_monitoring'},
    url='',
    license='',
    author='gvyarduhin',
    author_email='',
    description=''
)
