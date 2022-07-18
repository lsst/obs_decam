install()
{
    mkdir -p "$PREFIX"
    cp -a ./bin ./config ./doc ./pipelines ./python ./setup.cfg "$PREFIX"
    install_ups
}
