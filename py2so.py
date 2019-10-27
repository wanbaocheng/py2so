import getopt
import os
import sys


def transfer(dir_pref, is_clear=False):
    print(dir_pref)
    os.system('cython -2 %s.py;'
              'gcc -c -fPIC -I/usr/local/include/python3.%sm/ %s.c -o %s.o'
              % (dir_pref, p_subv, dir_pref, dir_pref))
    os.system('gcc -shared %s.o -o %s.so' % (dir_pref, dir_pref))
    if is_clear:
        os.system('rm -f %s.c %s.o %s.py' % (dir_pref, dir_pref, dir_pref))
    else:
        os.system('rm -f %s.c %s.o' % (dir_pref, dir_pref))


def is_subdir(abspath1, abspath2):
    return abspath1.find(abspath2) == 0


if __name__ == '__main__':
    help_show = '''
py2so is tool to change the .py to .so, you can use it to hide the source code of py
It can be called by the main func as "from module import * "
py2so needs the environment of python3

使用: python py2so.py [options] ...

选项:
  -v,  --version    显示py2so_py3版本
  -h,  --help       显示帮助菜单
  -p,  --py         Python的子版本号, 默认值为 6
                    例: -p 7  (比如你使用python3.7)
  -D,  --Directory  Python项目路径 (如果使用-D参数, 将加密整个Python项目)
  -d,  --directory  按首行是否有#py2so共六个字符作为标记进行加密，D优先于d
  -f,  --file       Python文件 (如果使用-f, 将加密单个Python文件)
  -c,  --clear      删除原文件（项目）
                    (警告: -c参数将会删除原文件, 但是为了避免损失，py2so_py3会自动备份原文件)
  -m,  --maintain   标记你不想加密的文件或文件夹路径
                    注意: 文件夹路径需要使用'[]'包起来, 并且需要和-d参数一起使用 
                    例: -m __init__.py,setup.py,[poc,resource,venv,interface]
示例：
  python py2so.py -f test_file.py
  python py2so.py -d test_dir -m __init__.py,setup.py,[poc/,resource/,venv/,interface/] -c
    '''
    is_clear = False
    p_subv = '6'
    root_names_D = ''
    root_names_d = ''
    file_name = ''
    m_list = ''
    try:
        options, args = getopt.getopt(sys.argv[1:], "vhp:Dd:f:cm:",
                                      ["version", "help", "py=", "Directory=", "directory=", "file=", "clear",
                                       "maintain=", 'nobackup'])
    except getopt.GetoptError:
        print('Get options Error')
        print(help_show)
        sys.exit(1)

    for key, value in options:
        print('(key,value): ', key, value)

    for key, value in options:
        if key in ['-h', '--help']:
            print(help_show)
        elif key in ['-v', '--version']:
            print('py2so version 0.0.1')
        elif key in ['-p', '--py']:
            p_subv = value
        elif key in ['-c', '--clear']:
            is_clear = True
        elif key in ['-D', '--Directory']:
            root_names_D = [os.path.abspath(val.strip()) for val in value.split(',') if val.strip() is not '']
            print(root_names_D)
        elif key in ['-d', '--directory']:
            root_names_d = [os.path.abspath(val.strip()) for val in value.split(',') if val.strip() is not '']
            print(root_names_d)
        elif key in ['-f', '--file']:
            file_name = value
        elif key in ['-m', '--maintain']:
            m_list = value
            file_flag = 0
            dir_flag = 0
            if m_list.find(',[') != -1:
                tmp = m_list.split(',[')
                file_list = tmp[0]
                dir_list = tmp[1:-1]
                file_flag = 1
                dir_flag = 1
            elif m_list.find('[') != -1:
                dir_list = m_list[1:-1]
                dir_flag = 1
            else:
                file_list = m_list.split(',')
                file_flag = 1
            if dir_flag == 1:
                dir_tmp = dir_list.split(',')
                dir_list = []
                for d in dir_tmp:
                    if d.startswith('./'):
                        dir_list.append(d[2:])
                    else:
                        dir_list.append(d)
    for root_name in root_names_D:
        if root_name != '':
            if not os.path.exists(root_name):
                print('No such Directory, please check or use the Absolute Path')
                sys.exit(1)
            try:
                for root, dirs, files in os.walk(root_name):
                    for file in files:
                        if m_list != '':
                            skip_flag = 0
                            if dir_flag == 1:
                                for dir in dir_list:
                                    if (root + '/').startswith(root_name + '/' + dir):
                                        skip_flag = 1
                                        break
                                if skip_flag:
                                    continue
                            if file_flag == 1:
                                if file in file_list:
                                    continue
                        pref = file.split('.')[0]
                        dir_pref = root + '/' + pref
                        if file.endswith('.pyc'):
                            os.system('rm -f %s' % dir_pref + '.pyc')
                        elif file.endswith('.so'):
                            pass
                        elif file.endswith('.py'):
                            transfer(dir_pref, is_clear)
            except Exception as err:
                print(err)
                if "Python.h" in str(err):
                    print(
                        "Please check out the Python version You use, and use option -p to specify the definite version")
    for root_name in root_names_d:
        if root_name != '':
            if not os.path.exists(root_name):
                print('No such Directory, please check or use the Absolute Path')
                sys.exit(1)
            try:
                for root, dirs, files in os.walk(root_name):
                    for file in files:
                        if m_list != '':
                            skip_flag = 0
                            if dir_flag == 1:
                                for dir in dir_list:
                                    if (root + '/').startswith(root_name + '/' + dir):
                                        skip_flag = 1
                                        break
                                if skip_flag:
                                    continue
                            if file_flag == 1:
                                if file in file_list:
                                    continue
                        pref = file.split('.')[0]
                        dir_pref = root + '/' + pref
                        if file.endswith('.pyc'):
                            os.system('rm -f %s' % dir_pref + '.pyc')
                        elif file.endswith('.so'):
                            pass
                        elif file.endswith('.py'):
                            dir_pref_base = os.path.dirname(dir_pref)
                            for root_name_D in root_names_D:
                                if is_subdir(dir_pref_base, root_name_D):
                                    break
                            else:
                                print('*: ', dir_pref)
                                with open(dir_pref + '.py', 'r') as f:
                                    if f.readline().find('#py2so') >= 0:
                                        transfer(dir_pref, is_clear)
            except Exception as err:
                print(err)
                if "Python.h" in str(err):
                    print(
                        "Please check out the Python version You use, and use option -p to specify the definite version")
    if file_name != '':
        try:
            dir_pref = file_name.split('.')[0]
            transfer(dir_pref, is_clear)
        except Exception as err:
            print(err)
