# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['logic.py'],
             pathex=['C:\\Users\\ASUS\\vscode\\some_games\\reactor'],
             binaries=[],
             datas=[('C:\\Users\\ASUS\\vscode\\some_games\\reactor\\*.png', '.'),('C:\\Users\\ASUS\\vscode\\some_games\\reactor\\imgs\\*.png', '.\\imgs'), ('C:\\Users\\ASUS\\vscode\\some_games\\freesansbold.ttf','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='racey',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='racey')
