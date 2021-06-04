# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['Co-Win Notifier v3.py'],
             pathex=['C:\\Users\\Ashwin\\Desktop\\Co-Win-Notifier v3 SIGNED'],
             binaries=[],
             datas=[
             ('data/**','data'),
             ('website/**','website')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Co-Win Notifier v3',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='data/icon.ico' )
