from setuptools import setup

setup(
        name='dojo-tool',
        version='1.0.0',
        python_requires='>=3.6.*',
        install_requires=['click',
                          'pyserial'],
        scripts=['main.py',
                 'eeprom.py',
                 'database.py'],
        entry_points={'console_scripts': ['maketicket=main:make_ticket']}
)
