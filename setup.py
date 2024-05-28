from setuptools import setup, find_packages

setup(
    name='MyFirewall',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[
        'psutil==5.9.8',
        'PyQt5==5.15.10',
        'scapy==2.4.3',
        'setuptools==45.2.0'
    ],
    entry_points={
        'console_scripts': [
            'myfirewall = myfirewall.main:main',
        ],
    },
    author='Huang Zehua',
    author_email='huangzh84@outlook.com',
    description='Firewall application design and development',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/zh-huang/Firewall',
)
