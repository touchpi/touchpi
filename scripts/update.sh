#!/bin/bash
#######################################################################
# Title      :    update.sh
# Author     :    touchpi@bruu.eu / file issues in github touchpi/touchpi
# Date       :    2022-11-01
# Input      :    none
#######################################################################
# Description
#   update touchpi
# Note:
# - needs a proper git installation (best with ssh)
# - two types of updates: for production master branch or for development last commit in any branch
# - the update type depends on an environment variable ENV_FOR_DYNACONF
#######################################################################

TOUCHPI_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"/..
cd "$TOUCHPI_PATH"
if [ -e ./venv/bin/activate ]; then
  source ./venv/bin/activate
fi

echo "=========================================================================="
echo "Current path: $(pwd)"
echo "=========================================================================="
echo "user: $(whoami) "
echo "=========================================================================="
echo "checkout master"
echo "__________________________________________________________________________"
git checkout master

if [ "$ENV_FOR_DYNACONF" == "development" ]
then
    echo "=========================================================================="
    echo "delete unknown local branches"
    echo "__________________________________________________________________________"
    git fetch -p ; git branch -r | awk '{print $1}' | grep -E -v -f /dev/fd/0 <(git branch -vv | grep origin) | awk '{print $1}' | xargs git branch -D
    echo "=========================================================================="
    echo "track all new remote branches"
    echo "__________________________________________________________________________"
    for branch in $(git branch --all | grep '^\s*remotes' | grep -E --invert-match '(:?HEAD|master)$'); do
        git branch --track "${branch##*/}" "$branch"
    done
    echo "=========================================================================="
    echo "pull all"
    echo "__________________________________________________________________________"
    git pull --all
    echo "=========================================================================="
    echo "checkout last commit"
    echo "__________________________________________________________________________"
    echo "Last commit: $(git log --branches -1 --pretty=format:'%D')"
    # shellcheck disable=SC2046
    git checkout $(git log --branches -1 --pretty=format:'%D' | sed 's/.*, //g')
fi

git pull

echo "=========================================================================="
echo "install python requirements"
echo "__________________________________________________________________________"
pip3 install -r requirements.txt
echo "=========================================================================="

echo "git status"
echo "__________________________________________________________________________"
git status
echo "=========================================================================="
echo "finish update"
echo "if necessary copy <app>.toml to <app>.local.toml and change configuration."
echo "Main config file is located in app/_core/_core.toml"
echo "=========================================================================="
