#!/bin/bash -e
INSTALL_DIR=$(/bin/pwd)
SET_CURRENT=false
RUCIO_VERSION="latest"
PIP_PKG=rucio-clients
DEPS=""

while [ $# -gt 0 ]; do
  case $1 in
    -i|--install-dir )      INSTALL_DIR="$2"      ; shift; shift;;
    -c|--current )          SET_CURRENT=true      ;        shift;;
    -v|--rucio-version )    RUCIO_VERSION="$2"    ; shift; shift;;
    -d|--dependency)        DEPS="$2"             ; shift; shift;;
    -h|--help )
      echo "
Usage: ${PIP_PKG}-$(basename $0)
  -i|--install-dir <path>       Install ${PIP_PKG} under <path>.
                                Default is currect working directory
  -v|--rucio-version <version>  ${PIP_PKG} version to install
                                Default is latest available version
  -d|--dependency               Install extra dependencies e.g. urllib3==1.25 requests=1.0
  -c|--current                  Make this version the default version
  -h|-help                      Show this help message

  It will install ${PIP_PKG} version under ${INSTALL_DIR} and will
  create a symlink 'current' pointing to this version. Run setup.sh
  script to set the ${PIP_PKG} environment e.g
      source ${INSTALL_DIR}/setup.sh
      source ${INSTALL_DIR}/setup.sh <version>"
      exit 0 ;;
    * ) echo "Error: Unknown arg '$1'"; exit 1;;
  esac
done

if [ ! -e ${INSTALL_DIR}/current ] ; then SET_CURRENT=true ; fi

if [ "${RUCIO_VERSION}" = "latest" ] ; then
  RUCIO_VERSION=$(pip search --disable-pip-version-check rucio-clients 2>&1 | grep '^rucio-clients ' | sed 's|).*||;s|.*(||')
fi

export PYTHONUSERBASE="${INSTALL_DIR}/${RUCIO_VERSION}"
mkdir -p "${PYTHONUSERBASE}" "${INSTALL_DIR}/tmp"
export TMPDIR="${INSTALL_DIR}/tmp"
if [ $(which python | grep '^/usr/bin/' | wc -l) -gt 0 ] ; then
  pip install --upgrade --user pip
  export PATH=${PYTHONUSERBASE}/bin:$PATH
  [ "$DEPS" ] && pip install --upgrade --user $DEPS
  pip install --upgrade --user setuptools
fi
pip install --disable-pip-version-check --user ${PIP_PKG}==${RUCIO_VERSION}
rm -f ${INSTALL_DIR}/rucio.cfg
cp $(dirname $0)/rucio.cfg ${INSTALL_DIR}/rucio.cfg
rm -f ${PYTHONUSERBASE}/etc/rucio.cfg
ln -s ../../rucio.cfg ${PYTHONUSERBASE}/etc/rucio.cfg
rm -rf ${TMPDIR}

cp -r $(dirname $0)/setup.sh ${INSTALL_DIR}/setup.sh
chmod 0644 ${INSTALL_DIR}/setup.sh
touch ${PYTHONUSERBASE}/.cvmfscatalog

[ ! -e ${INSTALL_DIR}/current ] && SET_CURRENT=true
if $SET_CURRENT ; then
  rm -f ${INSTALL_DIR}/current
  ln -s ${RUCIO_VERSION} ${INSTALL_DIR}/current
  echo "source ${INSTALL_DIR}/setup.sh"
  /bin/bash ${INSTALL_DIR}/setup.sh
else
  echo "source ${INSTALL_DIR}/setup.sh ${RUCIO_VERSION}"
  /bin/bash ${INSTALL_DIR}/setup.sh ${RUCIO_VERSION}
fi
