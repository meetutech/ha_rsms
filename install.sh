#! /bin/bash

[[ ! -d ${HOME}/.homeassistant ]] && {
    echo "Cannot find home assistant config folder"
    exit 1
}

NOW_PATH=$(pwd)

CONFIG_FOLDER=${HOME}/.homeassistant

[[ ! -d ${CONFIG_FOLDER}/custom_components/ha_rsms ]] && {
    mkdir -p ${CONFIG_FOLDER}/custom_components/ha_rsms
}

COM_FOLDER=${CONFIG_FOLDER}/custom_components/ha_rsms
C_FILES=('__init__.py' 'manifest.json' 'const.py')

# Download all files
echo "Prepare to download component files..."
for f in ${C_FILES[@]}; do 
    echo -n "downloading "${f}...
    curl -f -o ${COM_FOLDER}/${f} -L \
        "https://raw.githubusercontent.com/meetutech/ha_rsms/master/${f}" \
        >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "done"
    else
        echo "failed"
        exit 1
    fi
done

PLATFORM=`uname -s | tr '[:upper:]' '[:lower:]'`
ARCH=`uname -m`

echo "Host platform is "${PLATFORM}", arch is "${ARCH}

mkdir -p ${CONFIG_FOLDER}/rsms_bin
mkdir -p ${CONFIG_FOLDER}/rsms_bin/tmp
mkdir -p ${CONFIG_FOLDER}/rsms_bin/bin
mkdir -p ${CONFIG_FOLDER}/rsms_bin/lib

TEMP_DIR=${CONFIG_FOLDER}/rsms_bin/tmp
BIN_DIR=${CONFIG_FOLDER}/rsms_bin/bin
LIB_DIR=${CONFIG_FOLDER}/rsms_bin/lib

URL="https://rsms.meetutech.com/download/${PLATFORM}/${ARCH}/rsmsmgr.tgz"
echo "Prepare to download rsms bin files from ${URL}..."
curl -f -o ${TEMP_DIR}/rsmsmgr.tgz -L ${URL} >/dev/null 2>&1
[[ $? -ne 0 ]] && {
    echo "download failed, arch not supported"
    exit 1
}
cd ${TEMP_DIR}
tar xzvf ./rsmsmgr.tgz
# Copy all data
cp ./rsmsmgr/bin/rsmsmgr ${BIN_DIR}/
cp ./rsmsmgr/lib/* ${LIB_DIR}/
echo "Install Success!"
cd ${NOW} >/dev/null 2>&1
