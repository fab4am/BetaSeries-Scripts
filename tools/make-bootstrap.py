import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import subprocess

def after_install(options, home_dir):
    cwd = os.getcwd()
    subprocess.call([join(cwd, home_dir, 'bin', 'python'),
                 "setup.py",
                 "develop",
                 "--prefix=%s" % (join(cwd, home_dir)),
                 ])
"""))
f = open('bootstrap.py', 'w').write(output)
