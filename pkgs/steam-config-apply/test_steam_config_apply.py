"""Tests for steam_config_apply. Run: python3 -m unittest test_steam_config_apply (in this directory)."""
import json, os, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import steam_config_apply as sca  # noqa: E402


class Env:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = os.path.join(self.tmp.name, 'home')
        self.root = os.path.join(self.home, '.local', 'share', 'Steam')
        os.makedirs(os.path.join(self.root, 'userdata', '123', 'config'))
        os.makedirs(os.path.join(self.home, '.steam'))

    def write(self, rel, text, binary=False):
        p = os.path.join(self.home, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'wb' if binary else 'w') as f:
            f.write(text)
        return p

    def read(self, rel, binary=False):
        with open(os.path.join(self.home, rel), 'rb' if binary else 'r') as f:
            return f.read()

    def run(self, cfg):
        p = os.path.join(self.tmp.name, 'cfg.json')
        with open(p, 'w') as f:
            json.dump(cfg, f)
        r = subprocess.run([sys.executable, os.path.join(HERE, 'steam_config_apply.py'), p],
                           env={**os.environ, 'HOME': self.home}, capture_output=True, text=True, check=True)
        return r.stderr


ROOT = '.local/share/Steam/'


class TextVdf(unittest.TestCase):
    def test_merge_case_insensitive_and_idempotent(self):
        e = Env()
        e.write(ROOT + 'userdata/123/config/localconfig.vdf',
                '"UserLocalConfigStore"\n{\n\t"System"\n\t{\n\t\t"EnableGameOverlay"\t\t"1"\n\t\t"K"\t\t"Shift\\tKEY_TAB"\n\t}\n}\n')
        cfg = {'settings': [{'store': 'local', 'key': 'system\\EnableGameOverlay', 'value': '0'},
                            {'store': 'registry', 'key': 'HKEY_CURRENT_USER\\Software\\Valve\\Steam\\SmallMode', 'value': '1'}]}
        self.assertIn('localconfig.vdf', e.run(cfg))
        txt = e.read(ROOT + 'userdata/123/config/localconfig.vdf')
        self.assertIn('"System"', txt)
        self.assertIn('"EnableGameOverlay"\t\t"0"', txt)
        self.assertIn('Shift\\tKEY_TAB', txt)
        self.assertIn('"SmallMode"\t\t"1"', e.read('.steam/registry.vdf'))
        self.assertEqual(e.run(cfg), '')  # second run is a no-op
        self.assertTrue(os.path.exists(os.path.join(e.root, 'userdata/123/config/localconfig.vdf.nixos-steam.bak')))

    def test_registry_paths(self):
        self.assertEqual(sca.registry_path('HKEY_CURRENT_USER\\Software\\Valve\\Steam\\X'), 'HKCU\\Software\\Valve\\Steam\\X')
        self.assertEqual(sca.registry_path('HKCU\\Software\\X'), 'HKCU\\Software\\X')
        self.assertEqual(sca.registry_path('Software\\X'), 'HKCU\\Software\\X')

    def test_skips_while_running(self):
        e = Env()
        e.write('.steam/steam.pid', str(os.getpid()))
        # our own pid is alive but its comm is not "steam": must still apply
        self.assertIn('config/config.vdf', e.run({'settings': [{'store': 'install', 'key': 'A\\B', 'value': '1'}]}))


class Shortcuts(unittest.TestCase):
    def entries(self, e):
        items, _ = sca.bkv_parse(e.read(ROOT + 'userdata/123/config/shortcuts.vdf', binary=True))
        return [dict((k, v) for k, v in en) for _, en in items[0][1]]

    def test_roundtrip_and_upsert(self):
        e = Env()
        existing = sca.bkv_dump([['shortcuts', [['0', [['appid', ('i32', 5)], ['AppName', 'Mine'], ['Exe', '"/bin/x"'],
                                                     ['LastPlayTime', ('i32', 7)], ['tags', []]]]]]])
        self.assertEqual(sca.bkv_dump(sca.bkv_parse(existing)[0]), existing)
        e.write(ROOT + 'userdata/123/config/shortcuts.vdf', existing, binary=True)
        cfg = {'shortcuts': [{'key': 'game', 'appName': 'Game', 'exe': '/opt/game/run', 'launchOptions': '-x', 'tags': ['nix']}]}
        e.run(cfg)
        en = self.entries(e)
        self.assertEqual([x['AppName'] for x in en], ['Mine', 'Game'])
        self.assertEqual(en[1]['appid'][1] & 0xFFFFFFFF, sca.shortcut_appid('"/opt/game/run"', 'Game'))
        self.assertEqual(en[1]['StartDir'], '"/opt/game"')
        self.assertEqual(e.run(cfg), '')  # idempotent

    def test_path_change_replaces_and_cleans_up(self):
        e = Env()
        art = os.path.join(e.tmp.name, 'hero.jpg')
        with open(art, 'wb') as f:
            f.write(b'img')

        def cfg(exe):
            return {'shortcuts': [{'key': 'ra', 'appName': 'RetroArch', 'exe': exe, 'compatTool': 'proton_9',
                                   'artwork': {'hero': art, 'grid': None}}]}
        e.run(cfg('/nix/store/aaa-retroarch/bin/retroarch'))
        old = sca.shortcut_appid('"/nix/store/aaa-retroarch/bin/retroarch"', 'RetroArch')
        grid = os.path.join(e.root, 'userdata/123/config/grid')
        self.assertTrue(os.path.exists(os.path.join(grid, f'{old}_hero.jpg')))
        conf = e.read(ROOT + 'config/config.vdf')
        self.assertIn(f'"{old}"', conf)
        self.assertIn('"proton_9"', conf)
        # store path changes on update: the entry is replaced, not duplicated
        e.run(cfg('/nix/store/bbb-retroarch/bin/retroarch'))
        new = sca.shortcut_appid('"/nix/store/bbb-retroarch/bin/retroarch"', 'RetroArch')
        en = self.entries(e)
        self.assertEqual([x['appid'][1] & 0xFFFFFFFF for x in en], [new])
        self.assertFalse(os.path.exists(os.path.join(grid, f'{old}_hero.jpg')))
        self.assertTrue(os.path.exists(os.path.join(grid, f'{new}_hero.jpg')))
        conf = e.read(ROOT + 'config/config.vdf')
        self.assertNotIn(f'"{old}"', conf)
        self.assertIn(f'"{new}"', conf)
        # removed from config: entry, mapping and artwork go away
        e.run({'shortcuts': []})
        self.assertEqual(self.entries(e), [])
        self.assertFalse(os.path.exists(os.path.join(grid, f'{new}_hero.jpg')))
        self.assertNotIn(f'"{new}"', e.read(ROOT + 'config/config.vdf'))
        self.assertFalse(os.path.exists(os.path.join(e.root, sca.STATE)))


class Libraries(unittest.TestCase):
    def test_add_folder_and_manifest(self):
        e = Env()
        lib = os.path.join(e.tmp.name, 'games')
        e.run({'libraryFolders': [{'path': lib, 'label': 'Games'}]})
        txt = e.read(ROOT + 'steamapps/libraryfolders.vdf')
        self.assertIn(f'"path"\t\t"{e.root}"', txt)
        self.assertIn(f'"path"\t\t"{lib}"', txt)
        self.assertTrue(os.path.exists(os.path.join(lib, 'libraryfolder.vdf')))
        self.assertEqual(e.run({'libraryFolders': [{'path': lib, 'label': 'Games'}]}), '')
        with open(os.path.join(lib, 'steamapps', 'appmanifest_570.acf'), 'w') as f:
            f.write('"AppState"\n{\n\t"appid"\t\t"570"\n\t"AutoUpdateBehavior"\t\t"0"\n}\n')
        e.run({'settings': [{'store': 'appmanifest:570', 'key': 'AutoUpdateBehavior', 'value': '1'},
                            {'store': 'appmanifest:999', 'key': 'AutoUpdateBehavior', 'value': '1'}]})
        with open(os.path.join(lib, 'steamapps', 'appmanifest_570.acf')) as f:
            self.assertIn('"AutoUpdateBehavior"\t\t"1"', f.read())
        self.assertFalse(os.path.exists(os.path.join(lib, 'steamapps', 'appmanifest_999.acf')))


class JsonInVdf(unittest.TestCase):
    def test_merge_json_blob_and_accountid(self):
        e = Env()
        e.write(ROOT + 'userdata/123/7/remote/sharedconfig.vdf',
                '"UserRoamingConfigStore"\n{\n\t"Software"\n\t{\n\t\t"Valve"\n\t\t{\n\t\t\t"Steam"\n\t\t\t{\n'
                '\t\t\t\t"FriendsUI"\n\t\t\t\t{\n\t\t\t\t\t"FriendsUIJSON"\t\t"{\\"bCompactFriendsList\\":true}"\n'
                '\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n}\n')
        cfg = {'settings': [
            {'store': 'json:roaming', 'container': 'Software\\Valve\\Steam\\FriendsUI\\FriendsUIJSON',
             'key': 'nChatFlashMode', 'json': '2'},
            {'store': 'json:local', 'container': 'WebStorage\\SteamVoiceSettings_<accountid>', 'key': 'inputGain', 'json': '0.5'},
            {'store': 'local', 'key': 'friends\\Note_<accountid>', 'value': 'x'}]}
        e.run(cfg)
        items = sca.parse(e.read(ROOT + 'userdata/123/7/remote/sharedconfig.vdf'))
        blob = sca.get_path(items[0][1], ['Software', 'Valve', 'Steam', 'FriendsUI', 'FriendsUIJSON'])
        self.assertEqual(json.loads(blob), {'bCompactFriendsList': True, 'nChatFlashMode': 2})
        local = sca.parse(e.read(ROOT + 'userdata/123/config/localconfig.vdf'))
        self.assertEqual(json.loads(sca.get_path(local[0][1], ['WebStorage', 'SteamVoiceSettings_123'])), {'inputGain': 0.5})
        self.assertEqual(sca.get_path(local[0][1], ['friends', 'Note_123']), 'x')
        self.assertEqual(e.run(cfg), '')


class UserFiles(unittest.TestCase):
    def test_copies_into_each_account(self):
        e = Env()
        src = os.path.join(e.tmp.name, 'hero.png')
        with open(src, 'wb') as f:
            f.write(b'\x89PNG')
        cfg = {'userFiles': {'config/grid/570_hero.png': src}}
        self.assertIn('570_hero.png', e.run(cfg))
        self.assertEqual(e.read(ROOT + 'userdata/123/config/grid/570_hero.png', binary=True), b'\x89PNG')
        self.assertEqual(e.run(cfg), '')


class Files(unittest.TestCase):
    def test_managed_files_lifecycle(self):
        e = Env()
        e.write(ROOT + 'steam_dev.cfg', 'user owned\n')
        e.run({'files': {'package/beta': 'publicbeta', '.cef-enable-remote-debugging': '', 'steam_dev.cfg': 'x'}})
        self.assertEqual(e.read(ROOT + 'package/beta'), 'publicbeta')
        self.assertEqual(e.read(ROOT + 'steam_dev.cfg'), 'user owned\n')  # unmanaged file is never overwritten
        e.run({'files': {}})
        self.assertFalse(os.path.exists(os.path.join(e.root, 'package/beta')))
        self.assertFalse(os.path.exists(os.path.join(e.root, '.cef-enable-remote-debugging')))
        self.assertTrue(os.path.exists(os.path.join(e.root, 'steam_dev.cfg')))


if __name__ == '__main__':
    unittest.main()
