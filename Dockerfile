FROM theocf/debian:bookworm

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        wget \
        apt-transport-https \
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

WORKDIR /minecraft
COPY start.sh eula.txt server.properties ops.json /minecraft/
COPY ./plugins/ /minecraft/plugins
RUN curl -sSL "https://fill-data.papermc.io/v1/objects/e72a1c23c38683c32d8affa5c499c21e21524acb9bbeb38bdff8d8b6296f7d08/paper-1.21.8-10.jar" -o paper.jar

RUN ln -s /data/world world \
    && ln -s /data/world_nether world_nether \
    && ln -s /data/world_the_end world_the_end \
    && ln -s /data/banned-ips.json banned-ips.json \
    && ln -s /data/banned-players.json banned-players.json \
    && ln -s /data/whitelist.json whitelist.json


EXPOSE 25565
CMD ["./start.sh"]