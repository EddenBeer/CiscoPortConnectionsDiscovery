#from distutils.core import setup
from cx_Freeze import setup, Executable

setup(
    name='CiscoPortConnectionsDiscovery',
    version='0.1',
    packages=['/home/ed/PycharmProjects/CiscoPortConnectionsDiscovery/'],
    url='',
    license='',
    author='Ed den Beer',
    author_email='eddenbeer@gmail.com',
    description="Find out which ipadress is connected to a port."
)
