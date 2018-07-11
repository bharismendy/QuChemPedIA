# this script is use to create the doc from the code to latex and html


import subprocess

if __name__ == '__main__':
    # create rst file with this shell command : sphinx-apidoc -o source/_module ../
    subprocess.Popen(["sphinx-apidoc", "-o", "source/_module", "../"])
    # create the html doc from rst files with this command : sphinx-build -b html  _module/ _build/html
    subprocess.Popen(["sphinx-build", "-b", "html", "source/_module/", "source/_build/html"])
    # create the latex doc from rst files with this command : sphinx-build -b latex  _module/ _build/latex
    subprocess.Popen(["sphinx-build", "-b", "latex", "source/_module/", "source/_build/latex"])
