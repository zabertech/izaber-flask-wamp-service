from PyInstaller.utils.hooks import collect_glib_translations, get_gi_typelibs

def pre_safe_import_module(api):
    api.add_runtime_module('izaber_wamp_zerp')
    api.add_alias_module('izaber_wamp_zerp','izaber.wamp.zerp')


