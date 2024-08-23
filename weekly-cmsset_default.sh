XARCH=$(echo $1 | cut -d_ -f2)
[ "${XARCH}" != "amd64" ] || XARCH=x86_64
IB_WEEK_ENV=$(ls -d /cvmfs/cms-ib.cern.ch/sw/$XARCH/nweek-*/cmsset_default.sh | tail -1)
source ${IB_WEEK_ENV} || true
which git-cms-addpkg

