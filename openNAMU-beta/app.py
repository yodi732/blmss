# Render safe defaults
try:
    server_set_val = globals().get('server_set_val', {})
except FileNotFoundError:
    print('[WARN] File not found, skipping:', server_set_val = globals().get('server_set_val')
try:
    server_set_val.setdefault('host', '0.0.0.0')
except FileNotFoundError:
    print('[WARN] File not found, skipping:', server_set_val.setdefault('host')
try:
    server_set_val.setdefault('port', 3000)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', server_set_val.setdefault('port')
try:
    server_set_val.setdefault('golangport', 3001)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', server_set_val.setdefault('golangport')

golang_process = None  # Golang disabled in this build (Render)

download_url = None  # Safe default to avoid NameError

# Init
import os
import signal
import atexit
import logging

from route.tool.func import *
from route import *

from hypercorn.asyncio import serve
from hypercorn.config import Config

from werkzeug.middleware.proxy_fix import ProxyFix

args = sys.argv
try:
    run_mode = ''
except FileNotFoundError:
    print('[WARN] File not found, skipping:', run_mode = '')
if len(args) > 1:
    run_mode = args[1]

    try:
        if not run_mode in ['dev']:
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', if not run_mode in ['dev']:)
        try:
            run_mode = ''
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', run_mode = '')


# --- Safe version.json loader ---
try:
    def load_version_info(path='version.json'):
except FileNotFoundError:
    print('[WARN] File not found, skipping:', def load_version_info(path='version.json'):)
    DEFAULTS = {
        "r_ver": "1.0.0",
        "c_ver": "1.0.0",
        "s_ver": "1.0.0",
        "bin_link": ""  # if empty, binary download will be skipped
    }

    try:
        if not os.path.exists(path):
            # create a minimal version.json with defaults
            try:
                try:
                    with open(path, 'w', encoding='utf8') as _vf:
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', path)
                    json.dump({ "r_ver": DEFAULTS["r_ver"], "c_ver": DEFAULTS["c_ver"], "s_ver": DEFAULTS["s_ver"] }, _vf, ensure_ascii=False, indent=2)
                print(f"[INFO] Default {path} created.")
            except Exception as _e:
                print(f"[WARN] Could not create default {path}: {_e}")
            return DEFAULTS.copy()
        try:
            with open(path, 'r', encoding='utf8') as file_data:
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', path)
            try:
                data = json.load(file_data)
            except Exception as _e:
                print(f"[WARN] Failed to parse {path}: {_e}. Using defaults.")
                data = {}
        out = DEFAULTS.copy()
        try:
            for k in ('r_ver','c_ver','s_ver','bin_link'):
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', for k in ('r_ver')
            if k in data and data[k] is not None:
                out[k] = str(data[k])
        return out
    except Exception as _e:
        print(f"[ERROR] load_version_info error: {_e}")
        return DEFAULTS.copy()
# --- end loader ---

version_list = load_version_info()

# Init-DB
data_db_set = class_check_json()
do_db_set(data_db_set)

with get_db_connect(init_mode = True) as conn:
    curs = conn.cursor()

    try:
        setup_tool = ''
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', setup_tool = '')
    try:
        try:
            curs.execute(db_change('select data from other where name = "ver"'))
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', curs.execute(db_change('select data from other where name = "ver"')))
    except:
        try:
            setup_tool = 'init'
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', setup_tool = 'init')

    try:
        if setup_tool != 'init':
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', if setup_tool != 'init':)
        ver_set_data = curs.fetchall()
        if ver_set_data:
            try:
                if int(version_list['c_ver']) > int(ver_set_data[0][0]):
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', if int(version_list['c_ver']) > int(ver_set_data[0][0]):)
                try:
                    setup_tool = 'update'
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', setup_tool = 'update')
            else:
                try:
                    setup_tool = 'normal'
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', setup_tool = 'normal')
        else:
            try:
                setup_tool = 'init'
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', setup_tool = 'init')

    try:
        if run_mode != 'dev':
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', if run_mode != 'dev':)
        file_name = linux_exe_chmod()
        local_file_path = os.path.join("route_go", "bin", file_name)

        if not (setup_tool == "normal" and os.path.exists(local_file_path)):
            if os.path.exists(local_file_path):
                try:
                    print('Remove Old Binary')
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', print('Remove Old Binary'))
                os.remove(local_file_path)

            try:
                bin_link = version_list.get('bin_link', '')
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', bin_link = version_list.get('bin_link')
            if not bin_link:
                try:
                    print('[WARN] bin_link not set in version.json. Skipping binary download.')
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', print('[WARN] bin_link not set in version.json. Skipping binary download.'))
            else:
                download_url = bin_link + file_name
                try:
                    print('Download New Binary File')
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', print('Download New Binary File'))
                try:
                    response = requests.get(download_url, stream=True, timeout=30)
                except Exception as _e:
                    try:
                        print(f'[WARN] Failed to download binary from {download_url}: {_e}')
                    except FileNotFoundError:
                        print('[WARN] File not found, skipping:', print(f'[WARN] Failed to download binary from {download_url}: {_e}'))
                else:
                    if response.status_code == 200:
                        try:
                            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                            try:
                                with open(local_file_path, 'wb') as file:
                            except FileNotFoundError:
                                print('[WARN] File not found, skipping:', local_file_path)
                                for chunk in response.iter_content(chunk_size=8192):
                                    if chunk:
                                        file.write(chunk)
                            try:
                                print('Complete Download')
                            except FileNotFoundError:
                                print('[WARN] File not found, skipping:', print('Complete Download'))
                        except Exception as _e:
                            try:
                                print(f'[WARN] Failed to write binary file: {_e}')
                            except FileNotFoundError:
                                print('[WARN] File not found, skipping:', print(f'[WARN] Failed to write binary file: {_e}'))
                    else:
                        try:
                            print(f'[WARN] Binary download failed with HTTP status {response.status_code}')
                        except FileNotFoundError:
                            print('[WARN] File not found, skipping:', print(f'[WARN] Binary download failed with HTTP status {response.status_code}'))

            # Skipping additional redundant download step (handled above).

    try:
        if data_db_set['type'] == 'mysql':
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', if data_db_set['type'] == 'mysql':)
        try:
            try:
                curs.execute(db_change('create database ' + data_db_set['name'] + ' default character set utf8mb4'))
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', curs.execute(db_change('create database ' + data_db_set['name'] + ' default character set utf8mb4')))
        except:
            try:
                try:
                    curs.execute(db_change('alter database ' + data_db_set['name'] + ' character set utf8mb4'))
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', curs.execute(db_change('alter database ' + data_db_set['name'] + ' character set utf8mb4')))
            except:
                pass

        try:
            conn.select_db(data_db_set['name'])
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', conn.select_db(data_db_set['name']))
    else:
        try:
            conn.execute('pragma journal_mode = WAL')
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', conn.execute('pragma journal_mode = WAL'))

    try:
        if setup_tool != 'normal':
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', if setup_tool != 'normal':)
        create_data = get_db_table_list()
        for create_table in create_data:
            try:
                for create in ['test'] + create_data[create_table]:
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', for create in ['test'] + create_data[create_table]:)
                db_pass = 0

                try:
                    try:
                        curs.execute(db_change('select ' + create + ' from ' + create_table + ' limit 1'))
                    except FileNotFoundError:
                        print('[WARN] File not found, skipping:', curs.execute(db_change('select ' + create + ' from ' + create_table + ' limit 1')))
                    db_pass = 1
                except:
                    pass

                try:
                    field_text = 'longtext' if data_db_set['type'] == 'mysql' else 'text'
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', field_text = 'longtext' if data_db_set['type'] == 'mysql' else 'text')

                if db_pass == 0:
                    try:
                        try:
                            curs.execute(db_change('create table ' + create_table + '(test ' + field_text + ' default (""))'))
                        except FileNotFoundError:
                            print('[WARN] File not found, skipping:', curs.execute(db_change('create table ' + create_table + '(test ' + field_text + ' default (""))')))
                        db_pass = 1
                    except Exception as e:
                        # print(e)
                        pass

                if db_pass == 0:
                    try:
                        try:
                            curs.execute(db_change('create table ' + create_table + '(test ' + field_text + ' default "")'))
                        except FileNotFoundError:
                            print('[WARN] File not found, skipping:', curs.execute(db_change('create table ' + create_table + '(test ' + field_text + ' default "")')))
                        db_pass = 1
                    except Exception as e:
                        # print(e)
                        pass

                if db_pass == 0:
                    try:
                        try:
                            curs.execute(db_change('create table ' + create_table + '(test ' + field_text + ')'))
                        except FileNotFoundError:
                            print('[WARN] File not found, skipping:', curs.execute(db_change('create table ' + create_table + '(test ' + field_text + ')')))
                        db_pass = 1
                    except Exception as e:
                        # print(e)
                        pass

                if db_pass == 0:
                    try:
                        try:
                            curs.execute(db_change("alter table " + create_table + " add column " + create + " " + field_text + " default ('')"))
                        except FileNotFoundError:
                            print('[WARN] File not found, skipping:', curs.execute(db_change("alter table " + create_table + " add column " + create + " " + field_text + " default ('')")))
                        db_pass = 1
                    except Exception as e:
                        # print(e)
                        pass

                if db_pass == 0:
                    try:
                        try:
                            curs.execute(db_change("alter table " + create_table + " add column " + create + " " + field_text + " default ''"))
                        except FileNotFoundError:
                            print('[WARN] File not found, skipping:', curs.execute(db_change("alter table " + create_table + " add column " + create + " " + field_text + " default ''")))
                        db_pass = 1
                    except Exception as e:
                        # print(e)
                        pass

                if db_pass == 0:
                    try:
                        curs.execute(db_change("alter table " + create_table + " add column " + create + " " + field_text))
                        db_pass = 1
                    except Exception as e:
                        # print(e)
                        pass

                if db_pass == 0:
                    raise
        try:
            curs.execute(db_change("create index history_index on history (title, ip)"))
        except:
            pass

        try:
            if setup_tool == 'update':
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', if setup_tool == 'update':)
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(update(conn, int(ver_set_data[0][0]), data_db_set))
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(update(conn, int(ver_set_data[0][0]), data_db_set))
        else:
            set_init(conn)

    try:
        set_init_always(conn, version_list['c_ver'], run_mode)
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', set_init_always(conn)

    # Init-Route
    class EverythingConverter(werkzeug.routing.PathConverter):
        def __init__(self, map):
            super(EverythingConverter, self).__init__(map)
            try:
                self.regex = r'.*?'
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', self.regex = r'.*?')

        def to_python(self, value):
            try:
                return re.sub(r'^\\\.', '.', value)
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', return re.sub(r'^\\\.')

    class RegexConverter(werkzeug.routing.BaseConverter):
        def __init__(self, url_map, *items):
            super(RegexConverter, self).__init__(url_map)
            self.regex = items[0]

    try:
        app = flask.Flask(__name__, template_folder = './')
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', app = flask.Flask(__name__)

    try:
        app.config['JSON_AS_ASCII'] = False
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', app.config['JSON_AS_ASCII'] = False)
    try:
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False)
    try:
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 3600
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 3600)
    try:
        if run_mode == 'dev':
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', if run_mode == 'dev':)
        try:
            app.config['TEMPLATES_AUTO_RELOAD'] = True
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', app.config['TEMPLATES_AUTO_RELOAD'] = True)
        try:
            app.config['DEBUG'] = True
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', app.config['DEBUG'] = True)
        try:
            app.config['ENV'] = 'development'
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', app.config['ENV'] = 'development')

    try:
        log = logging.getLogger('hypercorn')
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', log = logging.getLogger('hypercorn'))
    log.setLevel(logging.ERROR)

    try:
        app.jinja_env.filters['md5_replace'] = md5_replace
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', app.jinja_env.filters['md5_replace'] = md5_replace)
    try:
        app.jinja_env.filters['load_lang'] = load_lang
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', app.jinja_env.filters['load_lang'] = load_lang)
    try:
        app.jinja_env.filters['cut_100'] = cut_100
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', app.jinja_env.filters['cut_100'] = cut_100)

    try:
        app.url_map.converters['everything'] = EverythingConverter
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', app.url_map.converters['everything'] = EverythingConverter)
    try:
        app.url_map.converters['regex'] = RegexConverter
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', app.url_map.converters['regex'] = RegexConverter)

    try:
        curs.execute(db_change('select data from other where name = "key"'))
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', curs.execute(db_change('select data from other where name = "key"')))
    sql_data = curs.fetchall()
    app.secret_key = sql_data[0][0]

    # Init-DB_Data
    server_set = {}
    server_set_var = get_init_set_list()
    server_set_env = {
        try:
            'host' : os.getenv('NAMU_HOST'),
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', 'host' : os.getenv('NAMU_HOST'))
        try:
            'golang_port' : os.getenv('NAMU_GOLANGPORT'),
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', 'golang_port' : os.getenv('NAMU_GOLANGPORT'))
        try:
            'port' : os.getenv('NAMU_PORT'),
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', 'port' : os.getenv('NAMU_PORT'))
        try:
            'language' : os.getenv('NAMU_LANG'),
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', 'language' : os.getenv('NAMU_LANG'))
        try:
            'markup' : os.getenv('NAMU_MARKUP'),
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', 'markup' : os.getenv('NAMU_MARKUP'))
        try:
            'encode' : os.getenv('NAMU_ENCRYPT')
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', 'encode' : os.getenv('NAMU_ENCRYPT'))
    }
    for i in server_set_var:
        try:
            curs.execute(db_change('select data from other where name = ?'), [i])
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', curs.execute(db_change('select data from other where name = ?'))
        server_set_val = curs.fetchall()
        if server_set_val:
            server_set_val = server_set_val[0][0]
        elif server_set_env[i] != None:
            server_set_val = server_set_env[i]

            try:
                curs.execute(db_change('insert into other (name, data, coverage) values (?, ?, "")'), [i, server_set_env[i]])
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', curs.execute(db_change('insert into other (name)
        else:
            try:
                if 'list' in server_set_var[i]:
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', if 'list' in server_set_var[i]:)
                try:
                    print(server_set_var[i]['display'] + ' (' + server_set_var[i]['default'] + ') [' + ', '.join(server_set_var[i]['list']) + ']' + ' : ', end = '')
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', print(server_set_var[i]['display'] + ' (' + server_set_var[i]['default'] + ') [' + ')
            else:
                # Non-interactive: prefer environment variable NAMU_<KEY>, then existing DB value, then default
                try:
                    env_name = 'NAMU_' + i.upper()
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', env_name = 'NAMU_' + i.upper())
                env_val = os.getenv(env_name)
                if env_val is not None:
                    server_set_val = env_val
                else:
                    # fallback to default defined in server_set_var
                    try:
                        server_set_val = server_set_var[i]['default']
                    except FileNotFoundError:
                        print('[WARN] File not found, skipping:', server_set_val = server_set_var[i]['default'])
                # if select requirement, validate against list
                try:
                    if server_set_var[i].get('require') == 'select' and 'list' in server_set_var[i]:
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', if server_set_var[i].get('require') == 'select' and 'list' in server_set_var[i]:)
                    try:
                        if server_set_val not in server_set_var[i]['list']:
                    except FileNotFoundError:
                        print('[WARN] File not found, skipping:', if server_set_val not in server_set_var[i]['list']:)
                        try:
                            server_set_val = server_set_var[i]['default']
                        except FileNotFoundError:
                            print('[WARN] File not found, skipping:', server_set_val = server_set_var[i]['default'])
                try:
                    try:
                        curs.execute(db_change('insert into other (name, data, coverage) values (?, ?, "")'), [i, server_set_val])
                    except FileNotFoundError:
                        print('[WARN] File not found, skipping:', curs.execute(db_change('insert into other (name)
                except Exception:
                    # if insert fails (maybe row exists), try update
                    try:
                        try:
                            curs.execute(db_change('update other set data = ? where name = ?'), [server_set_val, i])
                        except FileNotFoundError:
                            print('[WARN] File not found, skipping:', curs.execute(db_change('update other set data = ? where name = ?'))
                    except Exception:
                        pass

try:
    print(f"{server_set_val.get('display', '')} : {server_set_val}")
except FileNotFoundError:
    print('[WARN] File not found, skipping:', print(f"{server_set_val.get('display')

server_set[i] = server_set_val

for for_a in server_set:
    try:
        global_some_set_do('setup_' + for_a, server_set[for_a])
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', global_some_set_do('setup_' + for_a)

###

try:
    if platform.system() == 'Linux':
except FileNotFoundError:
    print('[WARN] File not found, skipping:', if platform.system() == 'Linux':)
    if platform.machine() in ["AMD64", "x86_64"]:
        cmd = [os.path.join(".", "route_go", "bin", "main.amd64.bin")]
    else:
        cmd = [os.path.join(".", "route_go", "bin", "main.arm64.bin")]
try:
    elif platform.system() == 'Darwin':
except FileNotFoundError:
    print('[WARN] File not found, skipping:', elif platform.system() == 'Darwin':)
    cmd = [os.path.join(".", "route_go", "bin", "main.mac.arm64.bin")]
else:
    if platform.machine() in ["AMD64", "x86_64"]:
        cmd = [os.path.join(".", "route_go", "bin", "main.amd64.exe")]
    else:
        cmd = [os.path.join(".", "route_go", "bin", "main.arm64.exe")]

if not isinstance(server_set, dict):
    server_set = dict()
try:
    cmd += [server_set.get('golang_port', '3001')]
except FileNotFoundError:
    print('[WARN] File not found, skipping:', cmd += [server_set.get('golang_port')
try:
    if run_mode != '':
except FileNotFoundError:
    print('[WARN] File not found, skipping:', if run_mode != '':)
    cmd += [run_mode]

async def golang_process_check():
    while True:
        try:
            other_set_temp = {}
            for k in data_db_set:
                other_set_temp["db_" + k] = data_db_set[k]

            other_set = {
                "url" : "test",
                "data" : json_dumps(other_set_temp),
                "session" : "{}",
                "cookie" : "",
                "ip" : "127.0.0.1"
            }

            if not isinstance(server_set, dict):
                server_set = dict()
            try:
                response = requests.post('http://localhost:' + server_set.get('golang_port', '3001') + '/', data = json_dumps(other_set))
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', response = requests.post('http://localhost:' + server_set.get('golang_port')
            if response.status_code == 200:
                try:
                    print('Golang turn on')
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', print('Golang turn on'))
                break
        except requests.ConnectionError:
            try:
                print('Wait golang...')
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', print('Wait golang...'))
            time.sleep(1)

golang_process = None  # Golang disabled: subprocess call removed for Render deployment


try:
    loop = asyncio.get_running_loop()
    loop.create_task(golang_process_check())
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(golang_process_check())

###

def back_up(data_db_set):
    with get_db_connect() as conn:
        curs = conn.cursor()

        try:
            try:
                curs.execute(db_change('select data from other where name = "back_up"'))
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', curs.execute(db_change('select data from other where name = "back_up"')))
            back_time = curs.fetchall()
            try:
                back_time = float(number_check(back_time[0][0], True)) if back_time and back_time[0][0] != '' else 0
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', back_time = float(number_check(back_time[0][0])

            try:
                curs.execute(db_change('select data from other where name = "backup_count"'))
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', curs.execute(db_change('select data from other where name = "backup_count"')))
            back_up_count = curs.fetchall()
            try:
                back_up_count = int(number_check(back_up_count[0][0])) if back_up_count and back_up_count[0][0] != '' else 3
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', back_up_count = int(number_check(back_up_count[0][0])) if back_up_count and back_up_count[0][0] != '' else 3)

            if back_time != 0:
                try:
                    curs.execute(db_change('select data from other where name = "backup_where"'))
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', curs.execute(db_change('select data from other where name = "backup_where"')))
                back_up_where = curs.fetchall()
                try:
                    back_up_where = back_up_where[0][0] if back_up_where and back_up_where[0][0] != '' else data_db_set['name'] + '.db'
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', back_up_where = back_up_where[0][0] if back_up_where and back_up_where[0][0] != '' else data_db_set['name'] + '.db')

                try:
                    print('Back up state : ' + str(back_time) + ' hours')
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', print('Back up state : ' + str(back_time) + ' hours'))
                try:
                    print('Back up directory : ' + back_up_where)
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', print('Back up directory : ' + back_up_where))
                if back_up_count != 0:
                    try:
                        print('Back up max number : ' + str(back_up_count))
                    except FileNotFoundError:
                        print('[WARN] File not found, skipping:', print('Back up max number : ' + str(back_up_count)))

                    file_dir = os.path.split(back_up_where)[0]
                    try:
                        file_dir = '.' if file_dir == '' else file_dir
                    except FileNotFoundError:
                        print('[WARN] File not found, skipping:', file_dir = '.' if file_dir == '' else file_dir)

                    file_name = os.path.split(back_up_where)[1]
                    try:
                        file_name = re.sub(r'\.db$', '_[0-9]{14}.db', file_name)
                    except FileNotFoundError:
                        print('[WARN] File not found, skipping:', file_name = re.sub(r'\.db$')

                    try:
                        backup_file = [for_a for for_a in os.listdir(file_dir) if re.search('^' + file_name + '$', for_a)]
                    except FileNotFoundError:
                        print('[WARN] File not found, skipping:', backup_file = [for_a for for_a in os.listdir(file_dir) if re.search('^' + file_name + '$')
                    backup_file = sorted(backup_file)

                    if len(backup_file) >= back_up_count:
                        remove_dir = os.path.join(file_dir, backup_file[0])
                        os.remove(remove_dir)
                        try:
                            print('Back up : Remove (' + remove_dir + ')')
                        except FileNotFoundError:
                            print('[WARN] File not found, skipping:', print('Back up : Remove (' + remove_dir + ')'))

                try:
                    now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
                try:
                    new_file_name = re.sub(r'\.db$', '_' + now_time + '.db', back_up_where)
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', new_file_name = re.sub(r'\.db$')
                shutil.copyfile(
                    try:
                        data_db_set['name'] + '.db',
                    except FileNotFoundError:
                        print('[WARN] File not found, skipping:', data_db_set['name'] + '.db')
                    new_file_name
                )

                try:
                    print('Back up : OK (' + new_file_name + ')')
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', print('Back up : OK (' + new_file_name + ')'))
            else:
                try:
                    print('Back up state : Turn off')
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', print('Back up state : Turn off'))

                back_time = 1
        except Exception as e:
            try:
                print('Back up : Error')
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', print('Back up : Error'))
            print(e)

            back_time = 1

        threading.Timer(60 * 60 * back_time, back_up, [data_db_set]).start()

async def do_every_day():
    with get_db_connect() as conn:
        curs = conn.cursor()

        # 오늘의 날짜 불러오기
        time_today = get_time().split()[0]

        # vote 관리
        try:
            curs.execute(db_change('select id, type from vote where type = "open" or type = "n_open"'))
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', curs.execute(db_change('select id)
        for for_a in curs.fetchall():
            try:
                curs.execute(db_change('select data from vote where id = ? and name = "end_date" and type = "option"'), [for_a[0]])
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', curs.execute(db_change('select data from vote where id = ? and name = "end_date" and type = "option"'))
            db_data = curs.fetchall()
            if db_data:
                time_db = db_data[0][0].split()[0]
                if time_today > time_db:
                    try:
                        curs.execute(db_change("update vote set type = ? where user = '' and id = ? and type = ?"), ['close' if for_a[1] == 'open' else 'n_close', for_a[0], for_a[1]])
                    except FileNotFoundError:
                        print('[WARN] File not found, skipping:', curs.execute(db_change("update vote set type = ? where user = '' and id = ? and type = ?"))

        # ban 관리
        try:
            curs.execute(db_change("update rb set ongoing = '' where end < ? and end != '' and ongoing = '1'"), [get_time()])
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', curs.execute(db_change("update rb set ongoing = '' where end < ? and end != '' and ongoing = '1'"))

        # auth 관리
        try:
            curs.execute(db_change('select id, data from user_set where name = "auth_date"'))
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', curs.execute(db_change('select id)
        db_data = curs.fetchall()
        for for_a in db_data:
            time_db = for_a[1].split()[0]
            if time_today > time_db:
                try:
                    curs.execute(db_change("update user_set set data = 'user' where id = ? and name = 'acl'"), [for_a[0]])
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', curs.execute(db_change("update user_set set data = 'user' where id = ? and name = 'acl'"))
                try:
                    curs.execute(db_change('delete from user_set where name = "auth_date" and id = ?'), [for_a[0]])
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', curs.execute(db_change('delete from user_set where name = "auth_date" and id = ?'))

        # acl 관리
        try:
            curs.execute(db_change("select doc_name, doc_rev, set_data from data_set where set_name = 'acl_date'"))
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', curs.execute(db_change("select doc_name)
        db_data = curs.fetchall()
        for for_a in db_data:
            time_db = for_a[2].split()[0]
            if time_today > time_db:
                curs.execute(db_change("delete from acl where title = ? and type = ?"), [for_a[0], for_a[1]])
                try:
                    curs.execute(db_change("delete from data_set where doc_name = ? and doc_rev = ? and set_name = 'acl_date'"), [for_a[0], for_a[1]])
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', curs.execute(db_change("delete from data_set where doc_name = ? and doc_rev = ? and set_name = 'acl_date'"))

        # ua 관리
        try:
            curs.execute(db_change('select data from other where name = "ua_expiration_date"'))
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', curs.execute(db_change('select data from other where name = "ua_expiration_date"')))
        db_data = curs.fetchall()
        try:
            if db_data and db_data[0][0] != '':
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', if db_data and db_data[0][0] != '':)
            time_db = int(number_check(db_data[0][0]))

            time_calc = datetime.date.today() - datetime.timedelta(days = time_db)
            try:
                time_calc = time_calc.strftime('%Y-%m-%d %H:%M:%S')
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', time_calc = time_calc.strftime('%Y-%m-%d %H:%M:%S'))

            curs.execute(db_change("delete from ua_d where today < ?"), [time_calc])

        # auth history 관리
        try:
            curs.execute(db_change('select data from other where name = "auth_history_expiration_date"'))
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', curs.execute(db_change('select data from other where name = "auth_history_expiration_date"')))
        db_data = curs.fetchall()
        try:
            if db_data and db_data[0][0] != '':
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', if db_data and db_data[0][0] != '':)
            time_db = int(number_check(db_data[0][0]))

            time_calc = datetime.date.today() - datetime.timedelta(days = time_db)
            try:
                time_calc = time_calc.strftime('%Y-%m-%d %H:%M:%S')
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', time_calc = time_calc.strftime('%Y-%m-%d %H:%M:%S'))

            curs.execute(db_change("delete from re_admin where time < ?"), [time_calc])

        # 사이트맵 생성 관리
        try:
            curs.execute(db_change('select data from other where name = "sitemap_auto_make"'))
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', curs.execute(db_change('select data from other where name = "sitemap_auto_make"')))
        db_data = curs.fetchall()
        try:
            if db_data and db_data[0][0] != '':
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', if db_data and db_data[0][0] != '':)
            await main_setting_sitemap(1)

            try:
                print('Make sitemap')
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', print('Make sitemap'))

        # 칭호 관리
        try:
            curs.execute(db_change("select id from user_set where name = 'user_title' and data = '✅'"))
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', curs.execute(db_change("select id from user_set where name = 'user_title' and data = '✅'")))
        for for_a in curs.fetchall():
            try:
                if await acl_check('', 'all_admin_auth', '', for_a[0]) == 1:
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', if await acl_check('')
                try:
                    curs.execute(db_change("update user_set set data = '☑️' where name = 'user_title' and data = '✅' and id = ?"), [for_a[0]])
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', curs.execute(db_change("update user_set set data = '☑️' where name = 'user_title' and data = '✅' and id = ?"))

        threading.Timer(60 * 60 * 24, do_every_day).start()

def auto_do_something(data_db_set):
    try:
        if data_db_set['type'] == 'sqlite':
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', if data_db_set['type'] == 'sqlite':)
        back_up(data_db_set)

    try:
        loop = asyncio.get_running_loop()
        loop.create_task(do_every_day())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(do_every_day())

auto_do_something(data_db_set)

try:
    print('Now running... http://localhost:' + server_set['port'])
except FileNotFoundError:
    print('[WARN] File not found, skipping:', print('Now running... http://localhost:' + server_set['port']))

@app.before_request
def before_request_func():
    try:
        db_data = global_some_set_do('wiki_access_password')
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', db_data = global_some_set_do('wiki_access_password'))
    try:
        if db_data and db_data != '':
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', if db_data and db_data != '':)
        access_password = db_data
        try:
            input_password = flask.request.cookies.get('opennamu_wiki_access', ' ')
        except FileNotFoundError:
            print('[WARN] File not found, skipping:', input_password = flask.request.cookies.get('opennamu_wiki_access')
        if url_pas(access_password) != input_password:
            with get_db_connect() as conn:
                try:
                    return '''
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', return ''')
                    <script>
                        "use strict";
                        function opennamu_do_wiki_access() {
                            try:
                                let password = document.getElementById('wiki_access').value;
                            except FileNotFoundError:
                                print('[WARN] File not found, skipping:', let password = document.getElementById('wiki_access').value;)
                            try:
                                document.cookie = 'opennamu_wiki_access=' + encodeURIComponent(password) + '; path=/;';
                            except FileNotFoundError:
                                print('[WARN] File not found, skipping:', document.cookie = 'opennamu_wiki_access=' + encodeURIComponent(password) + '; path=/;';)
                            history.go(0);
                        }
                    </script>
                    try:
                        <h2>''' + get_lang(conn, 'error_password_require_for_wiki_access') + '''</h2>
                    except FileNotFoundError:
                        print('[WARN] File not found, skipping:', <h2>''' + get_lang(conn)
                    <input type="password" id="wiki_access">
                    <input type="submit" onclick="opennamu_do_wiki_access();">
                try:
                    '''
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', ''')

# Init-custom
try:
    if os.path.exists('custom.py'):
except FileNotFoundError:
    print('[WARN] File not found, skipping:', if os.path.exists('custom.py'):)
    from custom import custom_run
    try:
        custom_run('error', app)
    except FileNotFoundError:
        print('[WARN] File not found, skipping:', custom_run('error')

# Func
# Func-inter_wiki
try:
    app.route('/filter/inter_wiki', defaults = { 'tool' : 'inter_wiki' })(filter_all)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/inter_wiki')
try:
    app.route('/filter/inter_wiki/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'inter_wiki' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/inter_wiki/add')
try:
    app.route('/filter/inter_wiki/add/<everything:name>', methods = ['POST', 'GET'], defaults = { 'tool' : 'inter_wiki' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/inter_wiki/add/<everything:name>')
try:
    app.route('/filter/inter_wiki/del/<everything:name>', defaults = { 'tool' : 'inter_wiki' })(filter_all_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/inter_wiki/del/<everything:name>')

try:
    app.route('/filter/outer_link', defaults = { 'tool' : 'outer_link' })(filter_all)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/outer_link')
try:
    app.route('/filter/outer_link/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'outer_link' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/outer_link/add')
try:
    app.route('/filter/outer_link/add/<everything:name>', methods = ['POST', 'GET'], defaults = { 'tool' : 'outer_link' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/outer_link/add/<everything:name>')
try:
    app.route('/filter/outer_link/del/<everything:name>', defaults = { 'tool' : 'outer_link' })(filter_all_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/outer_link/del/<everything:name>')

try:
    app.route('/filter/document', defaults = { 'tool' : 'document' })(filter_all)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/document')
try:
    app.route('/filter/document/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'document' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/document/add')
try:
    app.route('/filter/document/add/<everything:name>', methods = ['POST', 'GET'], defaults = { 'tool' : 'document' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/document/add/<everything:name>')
try:
    app.route('/filter/document/del/<everything:name>', defaults = { 'tool' : 'document' })(filter_all_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/document/del/<everything:name>')

try:
    app.route('/filter/edit_top', defaults = { 'tool' : 'edit_top' })(filter_all)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/edit_top')
try:
    app.route('/filter/edit_top/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'edit_top' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/edit_top/add')
try:
    app.route('/filter/edit_top/add/<everything:name>', methods = ['POST', 'GET'], defaults = { 'tool' : 'edit_top' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/edit_top/add/<everything:name>')
try:
    app.route('/filter/edit_top/del/<everything:name>', defaults = { 'tool' : 'edit_top' })(filter_all_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/edit_top/del/<everything:name>')

try:
    app.route('/filter/image_license', defaults = { 'tool' : 'image_license' })(filter_all)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/image_license')
try:
    app.route('/filter/image_license/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'image_license' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/image_license/add')
try:
    app.route('/filter/image_license/del/<everything:name>', defaults = { 'tool' : 'image_license' })(filter_all_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/image_license/del/<everything:name>')

try:
    app.route('/filter/template', defaults = { 'tool' : 'template' })(filter_all)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/template')
try:
    app.route('/filter/template/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'template' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/template/add')
try:
    app.route('/filter/template/add/<everything:name>', methods = ['POST', 'GET'], defaults = { 'tool' : 'template' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/template/add/<everything:name>')
try:
    app.route('/filter/template/del/<everything:name>', defaults = { 'tool' : 'template' })(filter_all_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/template/del/<everything:name>')

try:
    app.route('/filter/edit_filter', defaults = { 'tool' : 'edit_filter' })(filter_all)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/edit_filter')
try:
    app.route('/filter/edit_filter/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'edit_filter' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/edit_filter/add')
try:
    app.route('/filter/edit_filter/add/<everything:name>', methods = ['POST', 'GET'], defaults = { 'tool' : 'edit_filter' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/edit_filter/add/<everything:name>')
try:
    app.route('/filter/edit_filter/del/<everything:name>', defaults = { 'tool' : 'edit_filter' })(filter_all_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/edit_filter/del/<everything:name>')

try:
    app.route('/filter/email_filter', defaults = { 'tool' : 'email_filter' })(filter_all)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/email_filter')
try:
    app.route('/filter/email_filter/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'email_filter' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/email_filter/add')
try:
    app.route('/filter/email_filter/del/<everything:name>', defaults = { 'tool' : 'email_filter' })(filter_all_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/email_filter/del/<everything:name>')

try:
    app.route('/filter/file_filter', defaults = { 'tool' : 'file_filter' })(filter_all)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/file_filter')
try:
    app.route('/filter/file_filter/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'file_filter' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/file_filter/add')
try:
    app.route('/filter/file_filter/del/<everything:name>', defaults = { 'tool' : 'file_filter' })(filter_all_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/file_filter/del/<everything:name>')

try:
    app.route('/filter/name_filter', defaults = { 'tool' : 'name_filter' })(filter_all)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/name_filter')
try:
    app.route('/filter/name_filter/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'name_filter' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/name_filter/add')
try:
    app.route('/filter/name_filter/del/<everything:name>', defaults = { 'tool' : 'name_filter' })(filter_all_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/name_filter/del/<everything:name>')

try:
    app.route('/filter/extension_filter', defaults = { 'tool' : 'extension_filter' })(filter_all)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/extension_filter')
try:
    app.route('/filter/extension_filter/add', methods = ['POST', 'GET'], defaults = { 'tool' : 'extension_filter' })(filter_all_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/extension_filter/add')
try:
    app.route('/filter/extension_filter/del/<everything:name>', defaults = { 'tool' : 'extension_filter' })(filter_all_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/filter/extension_filter/del/<everything:name>')

# Func-list
try:
    app.route('/list/document/old', defaults = { 'set_type' : 'old' })(list_old_page)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/old')
try:
    app.route('/list/document/old/<int:num>', defaults = { 'set_type' : 'old' })(list_old_page)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/old/<int:num>')

try:
    app.route('/list/document/new', defaults = { 'set_type' : 'new' })(list_old_page)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/new')
try:
    app.route('/list/document/new/<int:num>', defaults = { 'set_type' : 'new' })(list_old_page)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/new/<int:num>')

try:
    app.route('/list/document/no_link')(list_no_link)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/no_link')(list_no_link))
try:
    app.route('/list/document/no_link/<int:num>')(list_no_link)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/no_link/<int:num>')(list_no_link))

try:
    app.route('/list/document/acl')(list_acl)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/acl')(list_acl))
try:
    app.route('/list/document/acl/<int:arg_num>')(list_acl)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/acl/<int:arg_num>')(list_acl))

try:
    app.route('/list/document/need')(list_please)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/need')(list_please))
try:
    app.route('/list/document/need/<int:arg_num>')(list_please)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/need/<int:arg_num>')(list_please))

try:
    app.route('/list/document/all')(list_title_index)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/all')(list_title_index))
try:
    app.route('/list/document/all/<int:num>')(list_title_index)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/all/<int:num>')(list_title_index))

try:
    app.route('/list/document/long')(list_long_page)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/long')(list_long_page))
try:
    app.route('/list/document/long/<int:arg_num>')(list_long_page)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/long/<int:arg_num>')(list_long_page))

try:
    app.route('/list/document/short', defaults = { 'tool' : 'short_page' })(list_long_page)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/short')
try:
    app.route('/list/document/short/<int:arg_num>', defaults = { 'tool' : 'short_page' })(list_long_page)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/document/short/<int:arg_num>')

try:
    app.route('/list/file')(list_image_file)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/file')(list_image_file))
try:
    app.route('/list/file/<int:arg_num>')(list_image_file)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/file/<int:arg_num>')(list_image_file))
try:
    app.route('/list/image', defaults = { 'do_type' : 1 })(list_image_file)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/image')
try:
    app.route('/list/image/<int:arg_num>', defaults = { 'do_type' : 1 })(list_image_file)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/image/<int:arg_num>')

try:
    app.route('/list/admin')(list_admin)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/admin')(list_admin))

try:
    app.route('/list/admin/auth_use', methods = ['POST', 'GET'])(list_admin_auth_use)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/admin/auth_use')
try:
    app.route('/list/admin/auth_use_page/<int:arg_num>/<everything:arg_search>', methods = ['POST', 'GET'])(list_admin_auth_use)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/admin/auth_use_page/<int:arg_num>/<everything:arg_search>')

try:
    app.route('/list/user')(list_user)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/user')(list_user))
try:
    app.route('/list/user/<int:arg_num>')(list_user)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/user/<int:arg_num>')(list_user))

try:
    app.route('/list/user/check_submit/<name>')(list_user_check_submit)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/user/check_submit/<name>')(list_user_check_submit))
try:
    app.route('/list/user/check/<name>')(list_user_check)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/user/check/<name>')(list_user_check))
try:
    app.route('/list/user/check/<name>/<do_type>')(list_user_check)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/user/check/<name>/<do_type>')(list_user_check))
try:
    app.route('/list/user/check/<name>/<do_type>/<int:arg_num>')(list_user_check)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/user/check/<name>/<do_type>/<int:arg_num>')(list_user_check))
try:
    app.route('/list/user/check/<name>/<do_type>/<int:arg_num>/<plus_name>')(list_user_check)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/user/check/<name>/<do_type>/<int:arg_num>/<plus_name>')(list_user_check))
try:
    app.route('/list/user/check/delete/<name>/<ip>/<time>/<do_type>', methods = ['POST', 'GET'])(list_user_check_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/list/user/check/delete/<name>/<ip>/<time>/<do_type>')

# Func-auth
try:
    app.route('/auth/give', methods = ['POST', 'GET'])(give_auth)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/auth/give')
try:
    app.route('/auth/give_total', methods = ['POST', 'GET'])(give_auth)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/auth/give_total')
try:
    app.route('/auth/give/<user_name>', methods = ['POST', 'GET'])(give_auth)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/auth/give/<user_name>')

try:
    app.route('/auth/ban', methods = ['POST', 'GET'])(give_user_ban)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/auth/ban')
try:
    app.route('/auth/ban/multiple', methods = ['POST', 'GET'], defaults = { 'ban_type' : 'multiple' })(give_user_ban)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/auth/ban/multiple')
try:
    app.route('/auth/ban/<everything:name>', methods = ['POST', 'GET'])(give_user_ban)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/auth/ban/<everything:name>')
try:
    app.route('/auth/ban_cidr/<everything:name>', methods = ['POST', 'GET'], defaults = { 'ban_type' : 'cidr' })(give_user_ban)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/auth/ban_cidr/<everything:name>')
try:
    app.route('/auth/ban_regex/<everything:name>', methods = ['POST', 'GET'], defaults = { 'ban_type' : 'regex' })(give_user_ban)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/auth/ban_regex/<everything:name>')

# /auth/list
# /auth/list/add/<name>
# /auth/list/delete/<name>
try:
    app.route('/auth/list')(list_admin_group)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/auth/list')(list_admin_group))
try:
    app.route('/auth/list/add/<name>', methods = ['POST', 'GET'])(give_admin_groups)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/auth/list/add/<name>')
try:
    app.route('/auth/list/delete/<name>', methods = ['POST', 'GET'])(give_delete_admin_group)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/auth/list/delete/<name>')

try:
    app.route('/auth/give/fix/<user_name>', methods = ['POST', 'GET'])(give_user_fix)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/auth/give/fix/<user_name>')

try:
    app.route('/app_submit', methods = ['POST', 'GET'])(recent_app_submit)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/app_submit')

# /auth/history
try:
    app.route('/recent_block')(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block')(list_recent_block))
try:
    app.route('/recent_block/all')(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block/all')(list_recent_block))
try:
    app.route('/recent_block/all/<int:num>')(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block/all/<int:num>')(list_recent_block))
try:
    app.route('/recent_block/all/<int:num>/<everything:why>')(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block/all/<int:num>/<everything:why>')(list_recent_block))
try:
    app.route('/recent_block/user/<user_name>', defaults = { 'tool' : 'user' })(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block/user/<user_name>')
try:
    app.route('/recent_block/user/<user_name>/<int:num>', defaults = { 'tool' : 'user' })(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block/user/<user_name>/<int:num>')
try:
    app.route('/recent_block/admin/<user_name>', defaults = { 'tool' : 'admin' })(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block/admin/<user_name>')
try:
    app.route('/recent_block/admin/<user_name>/<int:num>', defaults = { 'tool' : 'admin' })(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block/admin/<user_name>/<int:num>')
try:
    app.route('/recent_block/regex', defaults = { 'tool' : 'regex' })(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block/regex')
try:
    app.route('/recent_block/regex/<int:num>', defaults = { 'tool' : 'regex' })(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block/regex/<int:num>')
try:
    app.route('/recent_block/cidr', defaults = { 'tool' : 'cidr' })(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block/cidr')
try:
    app.route('/recent_block/cidr/<int:num>', defaults = { 'tool' : 'cidr' })(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block/cidr/<int:num>')
try:
    app.route('/recent_block/private', defaults = { 'tool' : 'private' })(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block/private')
try:
    app.route('/recent_block/private/<int:num>', defaults = { 'tool' : 'private' })(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block/private/<int:num>')
try:
    app.route('/recent_block/ongoing', defaults = { 'tool' : 'ongoing' })(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block/ongoing')
try:
    app.route('/recent_block/ongoing/<int:num>', defaults = { 'tool' : 'ongoing' })(list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_block/ongoing/<int:num>')

try:
    app.route('/recent_change', defaults = { 'tool' : 'recent_change' })(list_history)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_change')
try:
    app.route('/recent_changes', defaults = { 'tool' : 'recent_change' })(list_history)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_changes')
try:
    app.route('/recent_change/<int:num>/<set_type>', defaults = { 'tool' : 'recent_change' })(list_history)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_change/<int:num>/<set_type>')

try:
    app.route('/recent_discuss', defaults = { 'tool' : 'normal' })(list_recent_discuss)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_discuss')
try:
    app.route('/recent_discuss/<int:num>/<tool>')(list_recent_discuss)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_discuss/<int:num>/<tool>')(list_recent_discuss))

# Func-history
try:
    app.route('/recent_edit_request')(recent_edit_request)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/recent_edit_request')(recent_edit_request))

try:
    app.route('/record/<name>', defaults = { 'tool' : 'record' })(recent_change)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/record/<name>')
try:
    app.route('/record/<int:num>/<set_type>/<name>', defaults = { 'tool' : 'record' })(recent_change)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/record/<int:num>/<set_type>/<name>')

try:
    app.route('/record/reset/<name>', methods = ['POST', 'GET'])(recent_record_reset)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/record/reset/<name>')
try:
    app.route('/record/topic/<name>')(recent_record_topic)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/record/topic/<name>')(recent_record_topic))

try:
    app.route('/record/bbs/<name>', defaults = { 'tool' : 'record' })(bbs_w)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/record/bbs/<name>')
try:
    app.route('/record/bbs_comment/<name>', defaults = { 'tool' : 'comment_record' })(bbs_w)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/record/bbs_comment/<name>')

try:
    app.route('/history/<everything:doc_name>', methods = ['POST', 'GET'])(list_history)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/history/<everything:doc_name>')
try:
    app.route('/history_page/<int:num>/<set_type>/<everything:doc_name>', methods = ['POST', 'GET'])(list_history)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/history_page/<int:num>/<set_type>/<everything:doc_name>')

try:
    app.route('/history_tool/<int(signed = True):rev>/<everything:name>')(recent_history_tool)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/history_tool/<int(signed = True):rev>/<everything:name>')(recent_history_tool))
try:
    app.route('/history_delete/<int(signed = True):rev>/<everything:name>', methods = ['POST', 'GET'])(recent_history_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/history_delete/<int(signed = True):rev>/<everything:name>')
try:
    app.route('/history_hidden/<int(signed = True):rev>/<everything:name>')(recent_history_hidden)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/history_hidden/<int(signed = True):rev>/<everything:name>')(recent_history_hidden))
try:
    app.route('/history_send/<int(signed = True):rev>/<everything:name>', methods = ['POST', 'GET'])(recent_history_send)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/history_send/<int(signed = True):rev>/<everything:name>')
try:
    app.route('/history_reset/<everything:name>', methods = ['POST', 'GET'])(recent_history_reset)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/history_reset/<everything:name>')
try:
    app.route('/history_add/<everything:name>', methods = ['POST', 'GET'])(recent_history_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/history_add/<everything:name>')

# Func-view
try:
    app.route('/xref/<everything:name>')(view_xref)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/xref/<everything:name>')(view_xref))
try:
    app.route('/xref_page/<int:num>/<everything:name>')(view_xref)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/xref_page/<int:num>/<everything:name>')(view_xref))
try:
    app.route('/xref_this/<everything:name>', defaults = { 'xref_type' : 2 })(view_xref)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/xref_this/<everything:name>')
try:
    app.route('/xref_this_page/<int:num>/<everything:name>', defaults = { 'xref_type' : 2 })(view_xref)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/xref_this_page/<int:num>/<everything:name>')

try:
    app.route('/doc_watch_list/<int:num>/<everything:name>')(w_watch_list)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/doc_watch_list/<int:num>/<everything:name>')(w_watch_list))
try:
    app.route('/doc_star_doc/<int:num>/<everything:name>', defaults = { 'do_type' : 'star_doc' })(w_watch_list)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/doc_star_doc/<int:num>/<everything:name>')

try:
    app.route('/raw/<everything:name>')(view_w_raw)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/raw/<everything:name>')(view_w_raw))
try:
    app.route('/raw_acl/<everything:name>', defaults = { 'doc_acl' : 'on' })(view_w_raw)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/raw_acl/<everything:name>')
try:
    app.route('/raw_rev/<int(signed = True):rev>/<everything:name>')(view_w_raw)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/raw_rev/<int(signed = True):rev>/<everything:name>')(view_w_raw))

try:
    app.route('/diff/<int(signed = True):num_a>/<int(signed = True):num_b>/<everything:name>')(view_diff)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/diff/<int(signed = True):num_a>/<int(signed = True):num_b>/<everything:name>')(view_diff))

try:
    app.route('/down/<everything:name>')(view_down)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/down/<everything:name>')(view_down))

try:
    app.route('/acl_multiple', defaults = { 'multiple' : True }, methods = ['POST', 'GET'])(view_set)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/acl_multiple')
try:
    app.route('/acl/<everything:name>', methods = ['POST', 'GET'])(view_set)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/acl/<everything:name>')

try:
    app.route('/w_from/<everything:name>', defaults = { 'do_type' : 'from' })(view_w)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/w_from/<everything:name>')
try:
    app.route('/w/<everything:name>')(view_w)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/w/<everything:name>')(view_w))

try:
    app.route('/random')(view_random)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/random')(view_random))

# Func-edit
try:
    app.route('/edit/<everything:name>', methods = ['POST', 'GET'])(edit)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/edit/<everything:name>')
try:
    app.route('/edit_from/<everything:name>', methods = ['POST', 'GET'], defaults = { 'do_type' : 'load' })(edit)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/edit_from/<everything:name>')
try:
    app.route('/edit_section/<int:section>/<everything:name>', methods = ['POST', 'GET'])(edit)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/edit_section/<int:section>/<everything:name>')

try:
    app.route('/edit_request/<everything:name>', methods = ['POST', 'GET'])(edit_request)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/edit_request/<everything:name>')
try:
    app.route('/edit_request_from/<everything:name>', defaults = { 'do_type' : 'from' }, methods = ['POST', 'GET'])(edit_request)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/edit_request_from/<everything:name>')

try:
    # app.route('/edit_request_rev/<int:rev>/<everything:name>', methods = ['POST', 'GET'])(edit_request)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', # app.route('/edit_request_rev/<int:rev>/<everything:name>')

try:
    app.route('/upload', methods = ['POST', 'GET'])(edit_upload)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/upload')

# 개편 예정
try:
    app.route('/xref_reset/<everything:name>')(edit_backlink_reset)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/xref_reset/<everything:name>')(edit_backlink_reset))

try:
    app.route('/delete/<everything:name>', methods = ['POST', 'GET'])(edit_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/delete/<everything:name>')
try:
    app.route('/delete_file/<everything:name>', methods = ['POST', 'GET'])(edit_delete_file)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/delete_file/<everything:name>')
try:
    app.route('/delete_multiple', methods = ['POST', 'GET'])(edit_delete_multiple)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/delete_multiple')

try:
    app.route('/revert/<int:num>/<everything:name>', methods = ['POST', 'GET'])(edit_revert)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/revert/<int:num>/<everything:name>')

try:
    app.route('/move/<everything:name>', methods = ['POST', 'GET'])(edit_move)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/move/<everything:name>')
try:
    app.route('/move_all')(edit_move_all)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/move_all')(edit_move_all))

# Func-topic
try:
    app.route('/topic/<everything:name>', methods = ['POST', 'GET'])(topic_list)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/topic/<everything:name>')
try:
    app.route('/topic_page/<int:page>/<everything:name>', methods = ['POST', 'GET'])(topic_list)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/topic_page/<int:page>/<everything:name>')

try:
    app.route('/thread/<int:topic_num>', methods = ['POST', 'GET'])(topic)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/thread/<int:topic_num>')
try:
    app.route('/thread/0/<everything:doc_name>', defaults = { 'topic_num' : '0' }, methods = ['POST', 'GET'])(topic)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/thread/0/<everything:doc_name>')

try:
    app.route('/thread/<int:topic_num>/tool')(topic_tool)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/thread/<int:topic_num>/tool')(topic_tool))
try:
    app.route('/thread/<int:topic_num>/setting', methods = ['POST', 'GET'])(topic_tool_setting)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/thread/<int:topic_num>/setting')
try:
    app.route('/thread/<int:topic_num>/acl', methods = ['POST', 'GET'])(topic_tool_acl)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/thread/<int:topic_num>/acl')
try:
    app.route('/thread/<int:topic_num>/delete', methods = ['POST', 'GET'])(topic_tool_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/thread/<int:topic_num>/delete')
try:
    app.route('/thread/<int:topic_num>/change', methods = ['POST', 'GET'])(topic_tool_change)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/thread/<int:topic_num>/change')

try:
    app.route('/thread/<int:topic_num>/comment/<int:num>/tool')(topic_comment_tool)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/thread/<int:topic_num>/comment/<int:num>/tool')(topic_comment_tool))
try:
    app.route('/thread/<int:topic_num>/comment/<int:num>/notice')(topic_comment_notice)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/thread/<int:topic_num>/comment/<int:num>/notice')(topic_comment_notice))
try:
    app.route('/thread/<int:topic_num>/comment/<int:num>/blind')(topic_comment_blind)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/thread/<int:topic_num>/comment/<int:num>/blind')(topic_comment_blind))
try:
    app.route('/thread/<int:topic_num>/comment/<int:num>/raw')(view_raw)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/thread/<int:topic_num>/comment/<int:num>/raw')(view_raw))
try:
    app.route('/thread/<int:topic_num>/comment/<int:num>/delete', methods = ['POST', 'GET'])(topic_comment_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/thread/<int:topic_num>/comment/<int:num>/delete')

# Func-user
try:
    app.route('/change', methods = ['POST', 'GET'])(user_setting)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/change')
try:
    app.route('/change/key')(user_setting_key)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/change/key')(user_setting_key))
try:
    app.route('/change/key/delete')(user_setting_key_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/change/key/delete')(user_setting_key_delete))
try:
    app.route('/change/pw', methods = ['POST', 'GET'])(user_setting_pw)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/change/pw')
try:
    app.route('/change/head', methods = ['GET', 'POST'], defaults = { 'skin_name' : '' })(user_setting_head)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/change/head')
try:
    app.route('/change/head/<skin_name>', methods = ['GET', 'POST'])(user_setting_head)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/change/head/<skin_name>')
try:
    app.route('/change/head_reset', methods = ['GET', 'POST'])(user_setting_head_reset)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/change/head_reset')
try:
    app.route('/change/skin_set')(user_setting_skin_set)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/change/skin_set')(user_setting_skin_set))
try:
    app.route('/change/top_menu', methods = ['GET', 'POST'])(user_setting_top_menu)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/change/top_menu')
try:
    app.route('/change/user_name', methods = ['GET', 'POST'])(user_setting_user_name)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/change/user_name')
try:
    app.route('/change/user_name/<user_name>', methods = ['GET', 'POST'])(user_setting_user_name)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/change/user_name/<user_name>')
# 하위 호환용 S
try:
    app.route('/skin_set')(user_setting_skin_set)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/skin_set')(user_setting_skin_set))
# 하위 호환용 E
try:
    app.route('/change/skin_set/main', methods = ['POST', 'GET'])(user_setting_skin_set_main)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/change/skin_set/main')

try:
    app.route('/user')(user_info)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/user')(user_info))
try:
    app.route('/user/<name>')(user_info)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/user/<name>')(user_info))

try:
    app.route('/challenge', methods = ['GET', 'POST'])(user_challenge)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/challenge')

try:
    app.route('/edit_filter/<name>', methods = ['GET', 'POST'])(user_edit_filter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/edit_filter/<name>')

try:
    app.route('/count')(user_count)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/count')(user_count))
try:
    app.route('/count/<name>')(user_count)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/count/<name>')(user_count))

try:
    app.route('/alarm')(user_alarm)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/alarm')(user_alarm))
try:
    app.route('/alarm/delete')(user_alarm_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/alarm/delete')(user_alarm_delete))
try:
    app.route('/alarm/delete/<int:id>')(user_alarm_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/alarm/delete/<int:id>')(user_alarm_delete))

try:
    app.route('/watch_list', defaults = { 'tool' : 'watch_list' })(user_watch_list)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/watch_list')
try:
    app.route('/watch_list/<everything:name>', defaults = { 'tool' : 'watch_list' })(user_watch_list_name)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/watch_list/<everything:name>')
try:
    app.route('/watch_list_from/<everything:name>', defaults = { 'tool' : 'watch_list_from' })(user_watch_list_name)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/watch_list_from/<everything:name>')

try:
    app.route('/star_doc', defaults = { 'tool' : 'star_doc' })(user_watch_list)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/star_doc')
try:
    app.route('/star_doc/<everything:name>', defaults = { 'tool' : 'star_doc' })(user_watch_list_name)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/star_doc/<everything:name>')
try:
    app.route('/star_doc_from/<everything:name>', defaults = { 'tool' : 'star_doc_from' })(user_watch_list_name)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/star_doc_from/<everything:name>')

# 개편 보류중 S
try:
    app.route('/change/email', methods = ['POST', 'GET'])(user_setting_email)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/change/email')
try:
    app.route('/change/email/delete')(user_setting_email_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/change/email/delete')(user_setting_email_delete))
try:
    app.route('/change/email/check', methods = ['POST', 'GET'])(user_setting_email_check)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/change/email/check')
# 개편 보류중 E

# Func-login
# 개편 예정

# login -> login/2fa -> login/2fa/email with login_id
# register -> register/email -> regiter/email/check with reg_id
# pass_find -> pass_find/email with find_id

try:
    app.route('/login', methods = ['POST', 'GET'])(login_login)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/login')
try:
    app.route('/login/2fa', methods = ['POST', 'GET'])(login_login_2fa)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/login/2fa')
try:
    app.route('/register', methods = ['POST', 'GET'])(login_register)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/register')
try:
    app.route('/register/email', methods = ['POST', 'GET'])(login_register_email)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/register/email')
try:
    app.route('/register/email/check', methods = ['POST', 'GET'])(login_register_email_check)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/register/email/check')
try:
    app.route('/register/submit', methods = ['POST', 'GET'])(login_register_submit)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/register/submit')

try:
    app.route('/login/find')(login_find)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/login/find')(login_find))
try:
    app.route('/login/find/key', methods = ['POST', 'GET'])(login_find_key)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/login/find/key')
try:
    app.route('/login/find/email', methods = ['POST', 'GET'], defaults = { 'tool' : 'pass_find' })(login_find_email)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/login/find/email')
try:
    app.route('/login/find/email/check', methods = ['POST', 'GET'], defaults = { 'tool' : 'check_key' })(login_find_email_check)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/login/find/email/check')
try:
    app.route('/logout')(login_logout)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/logout')(login_logout))

# Func-vote
try:
    app.route('/vote/<int:num>', methods = ['POST', 'GET'])(vote_select)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/vote/<int:num>')
try:
    app.route('/vote/end/<int:num>')(vote_end)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/vote/end/<int:num>')(vote_end))
try:
    app.route('/vote/close/<int:num>')(vote_close)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/vote/close/<int:num>')(vote_close))
try:
    app.route('/vote', defaults = { 'list_type' : 'normal' })(vote_list)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/vote')
try:
    app.route('/vote/list', defaults = { 'list_type' : 'normal' })(vote_list)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/vote/list')
try:
    app.route('/vote/list/<int:num>', defaults = { 'list_type' : 'normal' })(vote_list)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/vote/list/<int:num>')
try:
    app.route('/vote/list/close', defaults = { 'list_type' : 'close' })(vote_list)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/vote/list/close')
try:
    app.route('/vote/list/close/<int:num>', defaults = { 'list_type' : 'close' })(vote_list)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/vote/list/close/<int:num>')
try:
    app.route('/vote/add', methods = ['POST', 'GET'])(vote_add)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/vote/add')

# Func-bbs
try:
    app.route('/bbs/main')(bbs_main)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/main')(bbs_main))
try:
    app.route('/bbs/make', methods = ['POST', 'GET'])(bbs_make)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/make')
try:
    app.route('/bbs/in/<int:bbs_num>')(bbs_in)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/in/<int:bbs_num>')(bbs_in))
try:
    app.route('/bbs/in/<int:bbs_num>/<int:page>')(bbs_in)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/in/<int:bbs_num>/<int:page>')(bbs_in))
try:
    # app.route('/bbs/blind/<int:bbs_num>', methods = ['POST', 'GET'])(bbs_hide)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', # app.route('/bbs/blind/<int:bbs_num>')
try:
    app.route('/bbs/delete/<int:bbs_num>', methods = ['POST', 'GET'])(bbs_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/delete/<int:bbs_num>')
try:
    app.route('/bbs/set/<int:bbs_num>', methods = ['POST', 'GET'])(bbs_w_set)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/set/<int:bbs_num>')
try:
    app.route('/bbs/edit/<int:bbs_num>', methods = ['POST', 'GET'])(bbs_w_edit)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/edit/<int:bbs_num>')
try:
    app.route('/bbs/w/<int:bbs_num>/<int:post_num>', methods = ['POST', 'GET'])(bbs_w_post)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/w/<int:bbs_num>/<int:post_num>')
try:
    # app.route('/bbs/blind/<int:bbs_num>/<int:post_num>', methods = ['POST', 'GET'])(bbs_w_hide)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', # app.route('/bbs/blind/<int:bbs_num>/<int:post_num>')
try:
    app.route('/bbs/pinned/<int:bbs_num>/<int:post_num>', methods = ['POST', 'GET'])(bbs_w_pinned)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/pinned/<int:bbs_num>/<int:post_num>')
try:
    app.route('/bbs/delete/<int:bbs_num>/<int:post_num>', methods = ['POST', 'GET'])(bbs_w_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/delete/<int:bbs_num>/<int:post_num>')
try:
    app.route('/bbs/raw/<int:bbs_num>/<int:post_num>')(view_raw)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/raw/<int:bbs_num>/<int:post_num>')(view_raw))
try:
    app.route('/bbs/tool/<int:bbs_num>/<int:post_num>')(bbs_w_tool)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/tool/<int:bbs_num>/<int:post_num>')(bbs_w_tool))
try:
    app.route('/bbs/edit/<int:bbs_num>/<int:post_num>', methods = ['POST', 'GET'])(bbs_w_edit)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/edit/<int:bbs_num>/<int:post_num>')
try:
    app.route('/bbs/tool/<int:bbs_num>/<int:post_num>/<comment_num>')(bbs_w_comment_tool)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/tool/<int:bbs_num>/<int:post_num>/<comment_num>')(bbs_w_comment_tool))
try:
    app.route('/bbs/raw/<int:bbs_num>/<int:post_num>/<comment_num>')(view_raw)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/raw/<int:bbs_num>/<int:post_num>/<comment_num>')(view_raw))
try:
    app.route('/bbs/edit/<int:bbs_num>/<int:post_num>/<comment_num>', methods = ['POST', 'GET'])(bbs_w_edit)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/edit/<int:bbs_num>/<int:post_num>/<comment_num>')
try:
    app.route('/bbs/delete/<int:bbs_num>/<int:post_num>/<comment_num>', methods = ['POST', 'GET'])(bbs_w_delete)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/bbs/delete/<int:bbs_num>/<int:post_num>/<comment_num>')

# Func-api
## v1 API
try:
    app.route('/api/render', methods = ['POST'])(api_w_render_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/render')
try:
    app.route('/api/render/<tool>', methods = ['POST'])(api_w_render_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/render/<tool>')

try:
    app.route('/api/raw_exist/<everything:name>', defaults = { 'exist_check' : 'on' })(api_w_raw)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/raw_exist/<everything:name>')
try:
    app.route('/api/raw_rev/<int(signed = True):rev>/<everything:name>')(api_w_raw)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/raw_rev/<int(signed = True):rev>/<everything:name>')(api_w_raw))
try:
    app.route('/api/raw/<everything:name>')(api_w_raw)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/raw/<everything:name>')(api_w_raw))

try:
    app.route('/api/xref/<int:page>/<everything:name>')(api_w_xref)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/xref/<int:page>/<everything:name>')(api_w_xref))
try:
    app.route('/api/xref_this/<int:page>/<everything:name>', defaults = { 'xref_type' : '2' })(api_w_xref)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/xref_this/<int:page>/<everything:name>')

try:
    app.route('/api/random')(api_w_random)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/random')(api_w_random))

try:
    app.route('/api/bbs/w/<sub_code>')(api_bbs_w)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/bbs/w/<sub_code>')(api_bbs_w))
try:
    app.route('/api/bbs/w/comment/<sub_code>')(api_bbs_w_comment_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/bbs/w/comment/<sub_code>')(api_bbs_w_comment_exter))
try:
    app.route('/api/bbs/w/comment_one/<sub_code>')(api_bbs_w_comment_one_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/bbs/w/comment_one/<sub_code>')(api_bbs_w_comment_one_exter))

try:
    app.route('/api/version', defaults = { 'version_list' : version_list })(api_version)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/version')
try:
    app.route('/api/skin_info')(api_skin_info)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/skin_info')(api_skin_info))
try:
    app.route('/api/skin_info/<name>')(api_skin_info)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/skin_info/<name>')(api_skin_info))
try:
    app.route('/api/user_info/<user_name>')(api_user_info)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/user_info/<user_name>')(api_user_info))

try:
    app.route('/api/thread/<int:topic_num>/<int:s_num>/<int:e_num>')(api_topic)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/thread/<int:topic_num>/<int:s_num>/<int:e_num>')(api_topic))
try:
    app.route('/api/thread/<int:topic_num>/<tool>')(api_topic)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/thread/<int:topic_num>/<tool>')(api_topic))
try:
    app.route('/api/thread/<int:topic_num>')(api_topic)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/thread/<int:topic_num>')(api_topic))

try:
    app.route('/api/search/<everything:name>')(api_func_search_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/search/<everything:name>')(api_func_search_exter))
try:
    app.route('/api/search_page/<int:num>/<everything:name>')(api_func_search_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/search_page/<int:num>/<everything:name>')(api_func_search_exter))
try:
    app.route('/api/search_data/<everything:name>', defaults = { 'search_type' : 'data' })(api_func_search_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/search_data/<everything:name>')
try:
    app.route('/api/search_data_page/<int:num>/<everything:name>', defaults = { 'search_type' : 'data' })(api_func_search_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/search_data_page/<int:num>/<everything:name>')

try:
    app.route('/api/recent_change')(api_list_recent_change_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/recent_change')(api_list_recent_change_exter))
try:
    app.route('/api/recent_changes')(api_list_recent_change_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/recent_changes')(api_list_recent_change_exter))
try:
    app.route('/api/recent_change/<int:limit>')(api_list_recent_change_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/recent_change/<int:limit>')(api_list_recent_change_exter))
try:
    app.route('/api/recent_change/<int:limit>/<set_type>/<int:num>')(api_list_recent_change_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/recent_change/<int:limit>/<set_type>/<int:num>')(api_list_recent_change_exter))

try:
    app.route('/api/recent_edit_request')(api_list_recent_edit_request_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/recent_edit_request')(api_list_recent_edit_request_exter))
try:
    app.route('/api/recent_edit_request/<int:limit>/<set_type>/<int:num>')(api_list_recent_edit_request_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/recent_edit_request/<int:limit>/<set_type>/<int:num>')(api_list_recent_edit_request_exter))

try:
    app.route('/api/recent_discuss/<set_type>/<int:limit>')(api_list_recent_discuss)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/recent_discuss/<set_type>/<int:limit>')(api_list_recent_discuss))
try:
    app.route('/api/recent_discuss/<int:limit>')(api_list_recent_discuss)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/recent_discuss/<int:limit>')(api_list_recent_discuss))
try:
    app.route('/api/recent_discuss')(api_list_recent_discuss)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/recent_discuss')(api_list_recent_discuss))

try:
    app.route('/api/lang', methods = ['POST'])(api_func_language)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/lang')
try:
    app.route('/api/lang/<data>')(api_func_language)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/lang/<data>')(api_func_language))
try:
    app.route('/api/sha224/<everything:data>')(api_func_sha224)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/sha224/<everything:data>')(api_func_sha224))
try:
    app.route('/api/ip/<everything:data>')(api_func_ip)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/ip/<everything:data>')(api_func_ip))

try:
    app.route('/api/image/<everything:name>')(api_image_view)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/image/<everything:name>')(api_image_view))

## v2 API
try:
    app.route('/api/v2/recent_edit_request/<set_type>/<int:num>', defaults = { 'limit' : 50 })(api_list_recent_edit_request)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/recent_edit_request/<set_type>/<int:num>')
try:
    app.route('/api/v2/recent_change/<set_type>/<int:num>', defaults = { 'legacy' : '', 'limit' : 50 })(api_list_recent_change_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/recent_change/<set_type>/<int:num>')
try:
    app.route('/api/v2/recent_discuss/<set_type>/<int:num>', defaults = { 'legacy' : '', 'limit' : 50 })(api_list_recent_discuss)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/recent_discuss/<set_type>/<int:num>')
try:
    app.route('/api/v2/recent_block/<set_type>/<int:num>')(api_list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/recent_block/<set_type>/<int:num>')(api_list_recent_block))
try:
    app.route('/api/v2/recent_block/<set_type>/<int:num>/<everything:why>')(api_list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/recent_block/<set_type>/<int:num>/<everything:why>')(api_list_recent_block))
try:
    app.route('/api/v2/recent_block_user/<set_type>/<int:num>/<user_name>')(api_list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/recent_block_user/<set_type>/<int:num>/<user_name>')(api_list_recent_block))
try:
    app.route('/api/v2/recent_block_user/<set_type>/<int:num>/<user_name>/<everything:why>')(api_list_recent_block)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/recent_block_user/<set_type>/<int:num>/<user_name>/<everything:why>')(api_list_recent_block))
try:
    app.route('/api/v2/list/document/old/<int:num>', defaults = { 'set_type' : 'old' })(api_list_old_page_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/list/document/old/<int:num>')
try:
    app.route('/api/v2/list/document/new/<int:num>', defaults = { 'set_type' : 'new' })(api_list_old_page_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/list/document/new/<int:num>')
try:
    app.route('/api/v2/list/document/<int:num>')(api_list_title_index)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/list/document/<int:num>')(api_list_title_index))
try:
    app.route('/api/v2/list/auth')(api_list_auth)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/list/auth')(api_list_auth))
try:
    app.route('/api/v2/list/markup')(api_list_markup)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/list/markup')(api_list_markup))
try:
    app.route('/api/v2/list/acl/<data_type>')(api_list_acl)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/list/acl/<data_type>')(api_list_acl))
try:
    app.route('/api/v2/history/<int:num>/<set_type>/<everything:doc_name>')(api_list_history_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/history/<int:num>/<set_type>/<everything:doc_name>')(api_list_history_exter))

try:
    app.route('/api/v2/topic/<int:num>/<set_type>/<everything:name>')(api_topic_list)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/topic/<int:num>/<set_type>/<everything:name>')(api_topic_list))

try:
    app.route('/api/v2/bbs')(api_bbs_list)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/bbs')(api_bbs_list))
try:
    app.route('/api/v2/bbs/main')(api_bbs)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/bbs/main')(api_bbs))
try:
    app.route('/api/v2/bbs/set/<int:bbs_num>/<name>', methods = ['GET', 'PUT'])(api_bbs_w_set)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/bbs/set/<int:bbs_num>/<name>')
try:
    app.route('/api/v2/bbs/in/<int:bbs_num>/<int:page>')(api_bbs)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/bbs/in/<int:bbs_num>/<int:page>')(api_bbs))
try:
    app.route('/api/v2/bbs/w/<sub_code>', defaults = { 'legacy' : '' })(api_bbs_w)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/bbs/w/<sub_code>')
try:
    app.route('/api/v2/bbs/w/tabom/<sub_code>', methods = ['GET', 'POST'])(api_bbs_w_tabom)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/bbs/w/tabom/<sub_code>')
try:
    app.route('/api/v2/bbs/w/comment/<sub_code>/<tool>', defaults = { 'legacy' : '' })(api_bbs_w_comment_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/bbs/w/comment/<sub_code>/<tool>')
try:
    app.route('/api/v2/bbs/w/comment_one/<sub_code>/<tool>', defaults = { 'legacy' : '' })(api_bbs_w_comment_one_exter)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/bbs/w/comment_one/<sub_code>/<tool>')

try:
    app.route('/api/v2/doc_star_doc/<int:num>/<everything:name>', defaults = { 'do_type' : 'star_doc' })(api_w_watch_list)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/doc_star_doc/<int:num>/<everything:name>')
try:
    app.route('/api/v2/doc_watch_list/<int:num>/<everything:name>')(api_w_watch_list)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/doc_watch_list/<int:num>/<everything:name>')(api_w_watch_list))
try:
    app.route('/api/v2/set_reset/<everything:name>')(api_w_set_reset)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/set_reset/<everything:name>')(api_w_set_reset))
try:
    app.route('/api/v2/page_view/<everything:name>')(api_w_page_view)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/page_view/<everything:name>')(api_w_page_view))

try:
    app.route('/api/v2/setting/<name>', methods = ['GET', 'PUT'])(api_setting)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/setting/<name>')

try:
    app.route('/api/v2/auth')(api_func_auth)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/auth')(api_func_auth))
try:
    app.route('/api/v2/auth/<user_name>')(api_func_auth)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/auth/<user_name>')(api_func_auth))
try:
    app.route('/api/v2/auth/give', methods = ['PATCH'])(api_give_auth)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/auth/give')

try:
    app.route('/api/v2/user/rankup', methods = ['GET', 'PATCH'])(api_user_rankup)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/user/rankup')
try:
    app.route('/api/v2/user/setting/editor', methods = ['GET', 'POST', 'DELETE'])(api_user_setting_editor)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/user/setting/editor')

try:
    app.route('/api/v2/ip/<everything:data>', methods = ['GET', 'POST'])(api_func_ip)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/ip/<everything:data>')
try:
    app.route('/api/v2/ip_menu/<everything:ip>', defaults = { 'option' : 'user' }, methods = ['GET', 'POST'])(api_func_ip_menu)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/ip_menu/<everything:ip>')
try:
    app.route('/api/v2/user_menu/<everything:ip>')(api_func_ip_menu)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/user_menu/<everything:ip>')(api_func_ip_menu))
try:
    app.route('/api/v2/lang', defaults = { 'legacy' : '' }, methods = ['POST'])(api_func_language)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/api/v2/lang')

# Func-main
# 여기도 전반적인 조정 시행 예정
try:
    app.route('/other')(main_tool_other)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/other')(main_tool_other))
try:
    app.route('/manager', methods = ['POST', 'GET'])(main_tool_admin)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/manager')
try:
    app.route('/manager/<int:num>', methods = ['POST', 'GET'])(main_tool_redirect)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/manager/<int:num>')
try:
    app.route('/manager/<int:num>/<everything:add_2>', methods = ['POST', 'GET'])(main_tool_redirect)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/manager/<int:num>/<everything:add_2>')

try:
    app.route('/search', methods=['POST'])(main_search)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/search')
try:
    app.route('/search/<everything:name>', methods = ['POST', 'GET'])(main_search_deep)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/search/<everything:name>')
try:
    app.route('/search_page/<int:num>/<everything:name>', methods = ['POST', 'GET'])(main_search_deep)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/search_page/<int:num>/<everything:name>')
try:
    app.route('/search_data/<everything:name>', defaults = { 'search_type' : 'data' }, methods = ['POST', 'GET'])(main_search_deep)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/search_data/<everything:name>')
try:
    app.route('/search_data_page/<int:num>/<everything:name>', defaults = { 'search_type' : 'data' }, methods = ['POST', 'GET'])(main_search_deep)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/search_data_page/<int:num>/<everything:name>')
try:
    app.route('/goto', methods=['POST'])(main_search_goto)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/goto')
try:
    app.route('/goto/<everything:name>', methods=['GET', 'POST'])(main_search_goto)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/goto/<everything:name>')

try:
    app.route('/setting')(main_setting)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting')(main_setting))
try:
    app.route('/setting/main', methods = ['POST', 'GET'])(main_setting_main)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting/main')
try:
    app.route('/setting/main/logo', methods = ['POST', 'GET'])(main_setting_main_logo)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting/main/logo')
try:
    app.route('/setting/top_menu', methods = ['POST', 'GET'])(main_setting_top_menu)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting/top_menu')
try:
    app.route('/setting/phrase', methods = ['POST', 'GET'])(main_setting_phrase)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting/phrase')
try:
    app.route('/setting/head', defaults = { 'num' : 3 }, methods = ['POST', 'GET'])(main_setting_head)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting/head')
try:
    app.route('/setting/head/<skin_name>', defaults = { 'num' : 3 }, methods = ['POST', 'GET'])(main_setting_head)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting/head/<skin_name>')
try:
    app.route('/setting/body/top', defaults = { 'num' : 4 }, methods = ['POST', 'GET'])(main_setting_head)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting/body/top')
try:
    app.route('/setting_preview/body/top', defaults = { 'num' : 4, 'set_preview' : 1 }, methods = ['POST'])(main_setting_head)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting_preview/body/top')
try:
    app.route('/setting/body/bottom', defaults = { 'num' : 7 }, methods = ['POST', 'GET'])(main_setting_head)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting/body/bottom')
try:
    app.route('/setting_preview/body/bottom', defaults = { 'num' : 7, 'set_preview' : 1 }, methods = ['POST'])(main_setting_head)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting_preview/body/bottom')
try:
    app.route('/setting/robot', methods = ['POST', 'GET'])(main_setting_robot)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting/robot')
try:
    app.route('/setting/external', methods = ['POST', 'GET'])(main_setting_external)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting/external')
try:
    app.route('/setting/sitemap', methods = ['POST', 'GET'])(main_setting_sitemap)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting/sitemap')
try:
    app.route('/setting/sitemap_set', methods = ['POST', 'GET'])(main_setting_sitemap_set)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting/sitemap_set')
try:
    app.route('/setting/skin_set', methods = ['POST', 'GET'])(main_setting_skin_set)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting/skin_set')
try:
    app.route('/setting/404_page', methods = ['POST', 'GET'])(setting_404_page)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting/404_page')
try:
    app.route('/setting/email_test', methods = ['POST', 'GET'])(main_setting_email_test)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/setting/email_test')

try:
    app.route('/easter_egg')(main_func_easter_egg)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/easter_egg')(main_func_easter_egg))

# views -> view
try:
    app.route('/view/<path:name>')(main_view)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/view/<path:name>')(main_view))
try:
    app.route('/views/<path:name>')(main_view)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/views/<path:name>')(main_view))
try:
    app.route('/image/<path:name>')(main_view_image)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/image/<path:name>')(main_view_image))
# 조정 계획 중
try:
    app.route('/<regex("[^.]+\\.(?:txt|xml|ico)"):data>')(main_view_file)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/<regex("[^.]+\\.(?:txt|xml|ico)"):data>')(main_view_file))

try:
    app.route('/shutdown', methods = ['POST', 'GET'])(main_sys_shutdown)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/shutdown')
try:
    app.route('/restart', defaults = { 'golang_process' : golang_process }, methods = ['POST', 'GET'])(main_sys_restart)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/restart')
try:
    app.route('/update', defaults = { 'golang_process' : golang_process }, methods = ['POST', 'GET'])(main_sys_update)
except FileNotFoundError:
    print('[WARN] File not found, skipping:', app.route('/update')

app.errorhandler(404)(main_func_error_404)

def terminate_golang():
    global golang_process
    # Golang disabled in this deployment; nothing to terminate.
    try:
        if golang_process is None:
            return
    except NameError:
        return

def signal_handler(signal, frame):
    terminate_golang()
    os._exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

atexit.register(terminate_golang)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for = 1, x_proto = 1)

try:
    if __name__ == '__main__':
except FileNotFoundError:
    print('[WARN] File not found, skipping:', if __name__ == '__main__':)
    import time
    import traceback

    restart_delay = 1      # 처음 재시작 대기 시간(초)
    max_delay = 60         # 최대 대기 시간(초)

    while True:
        try:
            try:
                if run_mode in ['dev']:
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', if run_mode in ['dev']:)
                try:
                    print('[INFO] Flask 개발 서버 시작...')
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', print('[INFO] Flask 개발 서버 시작...'))
                try:
                    app.run(host=server_set['host'], port=int(server_set['port']), use_reloader=False)
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', app.run(host=server_set['host'])
            else:
                try:
                    print('[INFO] Hypercorn 프로덕션 서버 시작...')
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', print('[INFO] Hypercorn 프로덕션 서버 시작...'))
                config = Config()
                try:
                    config.bind = [f"{server_set['host']}:{server_set['port']}"]
                except FileNotFoundError:
                    print('[WARN] File not found, skipping:', config.bind = [f"{server_set['host']}:{server_set['port']}"])
                asyncio.run(serve(app, config))

            try:
                print('[INFO] 서버가 정상적으로 종료되었습니다.')
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', print('[INFO] 서버가 정상적으로 종료되었습니다.'))
            break

        except KeyboardInterrupt:
            try:
                print('[INFO] 강제 종료 요청(Ctrl+C) — 서버 종료 중...')
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', print('[INFO] 강제 종료 요청(Ctrl+C) — 서버 종료 중...'))
            terminate_golang()
            break

        except Exception:
            try:
                print('[ERROR] 서버 실행 중 예외 발생:')
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', print('[ERROR] 서버 실행 중 예외 발생:'))
            traceback.print_exc()
            terminate_golang()
            try:
                print(f'[INFO] {restart_delay}초 후 재시작합니다...')
            except FileNotFoundError:
                print('[WARN] File not found, skipping:', print(f'[INFO] {restart_delay}초 후 재시작합니다...'))
            time.sleep(restart_delay)
            restart_delay = min(max_delay, restart_delay * 2)

    terminate_golang()
