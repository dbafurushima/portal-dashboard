#!/usr/bin/env sh
#
# fast install:
# bash <(curl -Ss https://raw.githubusercontent.com/dbafurushima/portal-dashboard/master/scripts/mng-install.sh)
#
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8
# links externos
REPOSITORY="https://github.com/dbafurushima/portal-dashboard.git"
# ------------------------------------------------------------------------------------------------
HOME_PATH_INSTALL="$HOME/.portal-dashboard"
if [ -d $HOME_PATH_INSTALL ]; then
    echo "atualizando repostório..."
    cd $HOME_PATH_INSTALL
    git pull
fi
# ------------------------------------------------------------------------------------------------
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
    fatal "unsupported distribution"
fi
# ------------------------------------------------------------------------------------------------
# library functions copied from packaging/installer/functions.sh
setup_terminal() {
	TPUT_RESET=""
	TPUT_YELLOW=""
	TPUT_WHITE=""
	TPUT_BGRED=""
	TPUT_BGGREEN=""
	TPUT_BOLD=""
	TPUT_DIM=""
	# is stderr on the terminal? If not, then fail
	test -t 2 || return 1

	if command -v tput > /dev/null 2>&1; then
		if [ $(($(tput colors 2> /dev/null))) -ge 8 ]; then
			# Enable colors
			TPUT_RESET="$(tput sgr 0)"
			TPUT_YELLOW="$(tput setaf 3)"
			TPUT_WHITE="$(tput setaf 7)"
			TPUT_BGRED="$(tput setab 1)"
			TPUT_BGGREEN="$(tput setab 2)"
			TPUT_BOLD="$(tput bold)"
			TPUT_DIM="$(tput dim)"
		fi
	fi
	return 0
}
# call function with environment variables
setup_terminal || echo > /dev/null
# ------------------------------------------------------------------------------------------------
# váriaveis de ambiente
export VERSION="MNG.cli [1.0.0v]"
# ------------------------------------------------------------------------------------------------
# informações do sistema
systeminfo() {
    export SYSTEM="$(uname -s 2> /dev/null || uname -v)"
    export OS="$(uname -o 2> /dev/null || uname -rs)"
    export MACHINE="$(uname -m 2> /dev/null)"

    echo "${TPUT_BOLD}${TPUT_WHITE}System            ${TPUT_RESET}: ${SYSTEM}"
    echo "${TPUT_BOLD}${TPUT_WHITE}Operating System  ${TPUT_RESET}: ${OS}"
    echo "${TPUT_BOLD}${TPUT_WHITE}Machine           ${TPUT_RESET}: ${MACHINE}"

	if [ "${OS}" != "GNU/Linux" ] && [ "${SYSTEM}" != "Linux" ]; then
    	warning "script version does not work well for your ${SYSTEM} - ${OS} system."
	fi
}
# chamar função
echo $VERSION
systeminfo
# ------------------------------------------------------------------------------------------------
# erro crítico
fatal() {
	printf >&2 "${TPUT_BGRED}${TPUT_WHITE}${TPUT_BOLD} ABORTED ${TPUT_RESET} ${*} \n\n"
	exit 1
}
# ------------------------------------------------------------------------------------------------
# operação bem sucedida
run_ok() {
	printf >&2 " ${TPUT_BGGREEN}${TPUT_WHITE}${TPUT_BOLD} OK ${TPUT_RESET} \n\n"
}
ok_dependencie() {
    printf >&2 "${TPUT_BGGREEN}${TPUT_WHITE}${TPUT_BOLD} OK ${TPUT_RESET} ${*}\n"
}
# ------------------------------------------------------------------------------------------------
# falha na operação
run_failed() {
  printf >&2 "${TPUT_BGRED}${TPUT_WHITE}${TPUT_BOLD} FAILED ${TPUT_RESET} \n\n"
}
# ------------------------------------------------------------------------------------------------
# função para exibir barra de progresso
progress() {
    echo >&2 " --- ${TPUT_DIM}${TPUT_BOLD}${*}${TPUT_RESET} --- "
}
# ------------------------------------------------------------------------------------------------
# função para executar comando na máquina
ESCAPED_PRINT_METHOD=
if printf "%q " test > /dev/null 2>&1; then
    ESCAPED_PRINT_METHOD="printfq"
fi
# formatter output
escaped_print() {
    if [ "${ESCAPED_PRINT_METHOD}" = "printfq" ]; then
        printf "%q " "${@}"
    else
        printf "%s" "${*}"
    fi
    return 0
}
run_logfile="/dev/null"
run() {
    local user="${USER--}" dir="${PWD}" info info_console
    if [ "${UID}" = "0" ]; then
        info="[root ${dir}]# "
        info_console="[${TPUT_DIM}${dir}${TPUT_RESET}]# "
    else
        info="[${user} ${dir}]$ "
        info_console="[${TPUT_DIM}${dir}${TPUT_RESET}]$ "
    fi

    {
        printf "\n${info}"
        escaped_print "${@}"
        printf " ... "
    } >> "${run_logfile}"

    printf >&2 "${info_console}${TPUT_BOLD}${TPUT_YELLOW}"
    escaped_print >&2 "${@}"
    printf >&2 "${TPUT_RESET}"

    "${@}"
    
    local ret=$?
    if [ ${ret} -ne 0 ]; then
        run_failed
        printf >> "${run_logfile}" "FAILED with exit code ${ret}\n"
    else
        run_ok
        printf >> "${run_logfile}" "OK\n"
    fi

    return ${ret}
}
# ------------------------------------------------------------------------------------------------
# message warning anda install pendencies
warning() {
	printf >&2 "${TPUT_BGRED}${TPUT_WHITE}${TPUT_BOLD} WARNING ${TPUT_RESET} ${*} \n\n"
	if [ "${INTERACTIVE}" = "0" ]; then
		fatal "Stopping due to non-interactive mode. Fix the issue or retry installation in an interactive mode."
	else
		read -r -p "Press ENTER to attempt installation > " CMD
        run $CMD
		progress "OK, let's give it a try..."
	fi
}
# ------------------------------------------------------------------------------------------------
# função para baixar arquivos
download() {
	progress "download public key"
	url="${1}"
	dest="${2}"
	if command -v curl > /dev/null 2>&1; then
		run curl -sSL --connect-timeout 10 --retry 3 "${url}" > "${dest}" || fatal "cannot download ${url}"
	elif command -v wget > /dev/null 2>&1; then
		run wget -T 15 -O - "${url}" > "${dest}" || fatal "cannot download ${url}"
	else
        warning "$package_manager -y install curl"
		## fatal "i need curl or wget to proceed, but neither is available on this system."
	fi
}
# ------------------------------------------------------------------------------------------------
# init configurations
# RUN pip3 --quiet install -r /var/www/warn/requirements.txt
RUN_COLOR="${TPUT_BGGREEN}${TPUT_WHITE}${TPUT_BOLD} RUN ${TPUT_RESET} $package_manager"
progress "check system dependencies"
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
    warning "$RUN_COLOR install$packages_for_install -y $hidden_install"
fi
# ------------------------------------------------------------------------------------------------
progress "clone repository portal-dashboard"
run git clone $REPOSITORY "$HOME/.portal-dashboard" || fatal "you have no communication with repo"
cd "$HOME_PATH_INSTALL"
# ------------------------------------------------------------------------------------------------
progress "install pip requirements"
pip3 install -r scripts/mng-requirements.txt
# ------------------------------------------------------------------------------------------------
progress "create alias and set script permissions"
SCRIPT_ENTRY_POINT="$HOME_PATH_INSTALL/scripts/mngcli.py"
chmod 0744 $SCRIPT_ENTRY_POINT
alias mngcli=$SCRIPT_ENTRY_POINT
echo "echo \"alias mngcli=$SCRIPT_ENTRY_POINT\" >> ~/.bashrc"
echo "exec \"$SHELL\""
