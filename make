#!/usr/bin/env bash


Opt=$1
VenvActivate=$PWD/venv/bin/activate
Reqs=$PWD/requirements.txt


function InstallServer () {

    if ! [ -f $VenvActivate ]; then

        virtualenv venv

    fi

    if [[ -f $Reqs ]]; then

        source $VenvActivate && pip install -r $Reqs

    fi

}


function RunServer () {

    source $VenvActivate && python3 server.py

}


function RunApi () {

    cd ./api && bash make app

}


function RunSite () {

    cd $PWD/site && python3 -m run build

}


if [[ $Opt == "install" ]]; then

    (InstallApp)

elif [[ $Opt == "server" ]]; then

    (RunServer)

elif [[ $Opt == "site" ]]; then

    (RunSite)

elif [[ $Opt == "api" ]]; then

    (RunApi)
    
fi
