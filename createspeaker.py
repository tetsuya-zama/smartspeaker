# -*- coding: utf-8 -*-
import os
import sys
from string import Template


def create_speaker_file(class_name,pkg_name):
    template_file = "template/src/speakers/templatespeaker.tpl"
    target_file = "src/speakers/" + pkg_name + ".py"
    create_file(template_file, target_file, class_name, pkg_name)


def create_testspeaker_file(class_name,pkg_name):
    template_file = "template/test/speakers/testtemplatespeaker.tpl"
    target_file = "test/speakers/test" + pkg_name + ".py"
    create_file(template_file, target_file, class_name, pkg_name)


def create_file(template_file,target_file,class_name,pkg_name):
    if os.path.isfile(target_file):
        print "既に" + target_file + "が存在しています。"
        return
    else:
        with open(template_file) as f:
            t = Template(f.read())
            t.substitute(CLASS_NAME=class_name,PKG_NAME=pkg_name)

            with open(target_file,'w') as result:
                result.write(t.substitute(CLASS_NAME=class_name,PKG_NAME=pkg_name))
        return

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Speaker名を指定して下さい。"
        exit(1)

    speaker_name = sys.argv[1]
    class_name = speaker_name + "Speaker"
    pkg_name = class_name.lower()

    create_speaker_file(class_name,pkg_name)
    create_testspeaker_file(class_name,pkg_name)
