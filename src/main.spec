# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['gcode_viewer\\main.py'],
             pathex=['C:\\Users\\Johannes\\iCloudDrive\\Uni\\CSE\\Year 3\\Advanced Prototyping\\APP\\3D print, use, disolve, repeat\\GCode Viewer\\src'],
             binaries=[],
             datas=[('gcode_viewer/resources/icons/*', 'gcode_viewer/resources/icons'), ('gcode_viewer/resources/fonts/*', 'gcode_viewer/resources/fonts'), ('gcode_viewer/resources/settings/*', 'gcode_viewer/resources/settings')],
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
          name='main',
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
               name='main')
