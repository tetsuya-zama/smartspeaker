#!/bin/bash
if [ $# -ne 1 ]; then
  echo "Speaker名を指定して下さい"
  exit 1
fi

SPEAKER_NAME=$1
CLASS_NAME=${SPEAKER_NAME}Speaker
PKG_NAME=`echo ${CLASS_NAME} | tr '[A-Z]' '[a-z]'`

if [ -e src/speakers/${PKG_NAME}.py ]; then
  echo "既に${PKG_NAME}.pyが存在しています。"
else
  cat template/src/speakers/templatespeaker.py | sed -e "s/###CLASS_NAME###/${CLASS_NAME}/g" > src/speakers/${PKG_NAME}.py
fi

if [ -e test/speakers/test${PKG_NAME}.py ]; then
  echo "既にtest${PKG_NAME}.pyが存在しています。"
else
  cat template/test/speakers/testtemplatespeaker.py | sed -e "s/###CLASS_NAME###/${CLASS_NAME}/g" | sed -e "s/###PKG_NAME###/${PKG_NAME}/g" > test/speakers/test${PKG_NAME}.py
fi
