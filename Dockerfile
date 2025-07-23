FROM theocf/debian:bookworm as base

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        wget \
        apt-transport-https \
        unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO - https://packages.adoptium.net/artifactory/api/gpg/key/public \
    | gpg --dearmor \
    | tee /etc/apt/trusted.gpg.d/adoptium.gpg \
    > /dev/null \
    && echo "deb https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" \
    | tee /etc/apt/sources.list.d/adoptium.list

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        temurin-21-jdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 25565
WORKDIR /minecraft
CMD ["./start.sh"]

FROM base as ocfmc-1-21-8

COPY ocfmc-1-21-8/* eula.txt /minecraft/
ADD https://fill-data.papermc.io/v1/objects/e72a1c23c38683c32d8affa5c499c21e21524acb9bbeb38bdff8d8b6296f7d08/paper-1.21.8-10.jar paper.jar

RUN ln -s /data/world world \
    && ln -s /data/world_nether world_nether \
    && ln -s /data/world_the_end world_the_end \
    && ln -s /data/banned-ips.json banned-ips.json \
    && ln -s /data/banned-players.json banned-players.json \
    && ln -s /data/whitelist.json whitelist.json \
    && ln -s /data/usercache.json usercache.json

FROM base as gtnh

ADD https://downloads.gtnewhorizons.com/ServerPacks/GT_New_Horizons_2.7.4_Server_Java_17-21.zip gtnh.zip

RUN ln -s /data/World World \
    && ln -s /data/backups backups \
    && ln -s /data/banned-ips.json banned-ips.json \
    && ln -s /data/banned-players.json banned-players.json \
    && ln -s /data/whitelist.json whitelist.json \
    && ln -s /data/usercache.json usercache.json

COPY gtnh/* eula.txt /minecraft/

RUN unzip -n gtnh.zip
