#!/usr/bin/env sh


export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8

# links externos
REPOSITORY="https://github.com/dbafurushima/portal-dashboard.git"

HOME_PATH_INSTALL="$HOME/.portal-dashboard"
if [ -d $HOME_PATH_INSTALL ]; then
    echo "[+] atualizando repostório..."
    cd $HOME_PATH_INSTALL
    git pull origin mng.v2
    exit 0
fi

# identify package manager
package_manager=
if [ ! -z $(command -v apt-get 2> /dev/null) ]; then
    package_manager="apt-get"
    hidden_install="-qq"
elif [ ! -z $(command -v dnf 2> /dev/null) ]; then
    package_manager="dnf"
    hidden_install="-q"
elif [ ! -z $(command -v yum 2> /dev/null) ]; then
    package_manager="yum"
    hidden_install="-q"
fi
if [ -z $package_manager ]; then
    echo "unsupported distribution"
    exit 1
fi

echo "check system dependencies"

packages_for_install=""
required_install=1
if [ -z $(command -v git --version 2> /dev/null) ]; then
    required_install=2
    packages_for_install+=" git"
fi
if [ -z $(command -v python3 -V 2> /dev/null) ]; then
    required_install=2
    packages_for_install+=" python3"
fi
if [ -z $(command -v pip3 2> /dev/null) ]; then
    required_install=2
    packages_for_install+=" python3-pip"
fi
if [ $required_install -eq 2 ]; then
    echo "$packages_for_install -y $hidden_install"
    exit 1
fi

echo "clone repository portal-dashboard"
git clone $REPOSITORY "$HOME/.portal-dashboard" || echo "error in clone repo"; exit 1

cd "$HOME/.portal-dashboard"
git pull origin mng.v2

echo "install pip requirements"
pip3 install -r mng-requirements.txt

ENTRY_POINT_MODULE="$HOME_PATH_INSTALL/mng"

# optional alias to put in the user's bashrc
echo "echo \"alias mng=python3 -m $ENTRY_POINT_MODULE\" >> ~/.bashrc"
echo "exec \"$SHELL\""