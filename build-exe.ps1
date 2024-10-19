# Builds the PyNoteBook executable.
#
# This article was helpful:
# https://www.pythonguis.com/tutorials/packaging-pyside6-applications-windows-pyinstaller-installforge/
#
# In particular, if building fails, or if the resulting executable does not execute, ensure that PyInstaller is up to date:
# pip3 install --upgrade PyInstaller pyinstaller-hooks-contrib

$arguments = 'cli.py',
             '-w',
             '--noconfirm',
             '--clean',
             '--name',
             'pyNotebook',
             '--icon',
             'Resources/AppIcon.ico',
             '--add-data',
             './Resources;Resources',
             '--add-data',
             './*.ui;.'

pyinstaller $arguments 2>&1 > .\pyinstaller-build.log