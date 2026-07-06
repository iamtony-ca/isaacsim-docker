
# installation
https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/install_container.html


# cli
docker exec -it isaac-sim bash
mkdir -p /isaac-sim/exts/isaacsim.asset.browser/cache

## root connection
docker exec -u 0 -it isaac-sim bash

# launch
xhost +local:
docker run --name isaac-sim --entrypoint bash -it --gpus all -e "ACCEPT_EULA=Y" --rm --network=host \
    -e "PRIVACY_CONSENT=Y" \
    -v $HOME/.Xauthority:/isaac-sim/.Xauthority \
    -e DISPLAY \
    -v ~/docker/isaac-sim/cache/main:/isaac-sim/.cache:rw \
    -v ~/docker/isaac-sim/cache/computecache:/isaac-sim/.nv/ComputeCache:rw \
    -v ~/docker/isaac-sim/logs:/isaac-sim/.nvidia-omniverse/logs:rw \
    -v ~/docker/isaac-sim/config:/isaac-sim/.nvidia-omniverse/config:rw \
    -v ~/docker/isaac-sim/data:/isaac-sim/.local/share/ov/data:rw \
    -v ~/docker/isaac-sim/pkg:/isaac-sim/.local/share/ov/pkg:rw \
    -u 1234:1234 \
    nvcr.io/nvidia/isaac-sim:5.1.0


# launch from gemini
xhost +local:
docker run --name isaac-sim --entrypoint bash -it --gpus all --rm --network=host \
    --shm-size=32gb \
    -e "ACCEPT_EULA=Y" \
    -e "PRIVACY_CONSENT=Y" \
    -e "NVIDIA_DRIVER_CAPABILITIES=all" \
    -e DISPLAY \
    -v $HOME/.Xauthority:/isaac-sim/.Xauthority \
    -v ~/docker/isaac-sim/cache/main:/isaac-sim/.cache:rw \
    -v ~/docker/isaac-sim/cache/computecache:/isaac-sim/.nv/ComputeCache:rw \
    -v ~/docker/isaac-sim/logs:/isaac-sim/.nvidia-omniverse/logs:rw \
    -v ~/docker/isaac-sim/config:/isaac-sim/.nvidia-omniverse/config:rw \
    -v ~/docker/isaac-sim/data:/isaac-sim/.local/share/ov/data:rw \
    -v ~/docker/isaac-sim/pkg:/isaac-sim/.local/share/ov/pkg:rw \
    -u 1234:1234 \
    nvcr.io/nvidia/isaac-sim:5.1.0


xhost +local:
docker run --name isaac-sim --entrypoint bash -it --gpus all --rm --network=host \
    --shm-size=32gb \
    -e "ACCEPT_EULA=Y" \
    -e "PRIVACY_CONSENT=Y" \
    -e "NVIDIA_DRIVER_CAPABILITIES=all" \
    -e DISPLAY \
    -v $HOME/.Xauthority:/root/.Xauthority:rw \
    -v ~/docker/isaac-sim/cache/main:/root/.cache/ov:rw \
    -v ~/docker/isaac-sim/cache/computecache:/root/.nv/ComputeCache:rw \
    -v ~/docker/isaac-sim/logs:/root/.nvidia-omniverse/logs:rw \
    -v ~/docker/isaac-sim/config:/root/.nvidia-omniverse/config:rw \
    -v ~/docker/isaac-sim/data:/root/.local/share/ov/data:rw \
    -v ~/docker/isaac-sim/pkg:/root/.local/share/ov/pkg:rw \
    nvcr.io/nvidia/isaac-sim:5.1.0



xhost +local:
docker run --name isaac-sim --entrypoint bash -it --gpus all --network=host \
    --shm-size=32gb \
    -e "ACCEPT_EULA=Y" \
    -e "PRIVACY_CONSENT=Y" \
    -e "NVIDIA_DRIVER_CAPABILITIES=all" \
    -e DISPLAY \
    -v $HOME/.Xauthority:/root/.Xauthority:rw \
    -v ~/docker/isaac-sim/cache/main:/root/.cache/ov:rw \
    -v ~/docker/isaac-sim/cache/computecache:/root/.nv/ComputeCache:rw \
    -v ~/docker/isaac-sim/logs:/root/.nvidia-omniverse/logs:rw \
    -v ~/docker/isaac-sim/config:/root/.nvidia-omniverse/config:rw \
    -v ~/docker/isaac-sim/data:/root/.local/share/ov/data:rw \
    -v ~/docker/isaac-sim/pkg:/root/.local/share/ov/pkg:rw \
    nvcr.io/nvidia/isaac-sim:5.1.0


```
# 공식 docs 원본 디렉토리
mkdir -p ~/docker/isaac-sim-601/cache/main
mkdir -p ~/docker/isaac-sim-601/cache/computecache
mkdir -p ~/docker/isaac-sim-601/config
mkdir -p ~/docker/isaac-sim-601/data
mkdir -p ~/docker/isaac-sim-601/logs
mkdir -p ~/docker/isaac-sim-601/pkg
mkdir -p ~/.cache/ov/hub

# 공유 폴더 추가
mkdir -p ~/docker/isaac-sim-601/volume

sudo chown -R 1234:1234 ~/docker/isaac-sim-601 ~/.cache/ov/hub

# 공유 폴더: host(user)와 container(1234) 양방향 편집 가능하게 ACL
MYUID=$(id -u)   # host user = 1000
sudo setfacl -R    -m u:$MYUID:rwx -m u:1234:rwx -m m:rwx ~/docker/isaac-sim-601/volume
sudo setfacl -R -d -m u:$MYUID:rwx -m u:1234:rwx -m m:rwx ~/docker/isaac-sim-601/volume



# container 생성
xhost +local:
docker run --name isaac-sim-601 --entrypoint bash -it --gpus all -e "ACCEPT_EULA=Y" --network=host \
    -e "PRIVACY_CONSENT=Y" \
    -v $HOME/.Xauthority:/isaac-sim/.Xauthority \
    -e DISPLAY \
    -v ~/docker/isaac-sim-601/cache/main:/isaac-sim/.cache:rw \
    -v ~/docker/isaac-sim-601/cache/computecache:/isaac-sim/.nv/ComputeCache:rw \
    -v ~/docker/isaac-sim-601/logs:/isaac-sim/.nvidia-omniverse/logs:rw \
    -v ~/docker/isaac-sim-601/config:/isaac-sim/.nvidia-omniverse/config:rw \
    -v ~/docker/isaac-sim-601/data:/isaac-sim/.local/share/ov/data:rw \
    -v ~/docker/isaac-sim-601/pkg:/isaac-sim/.local/share/ov/pkg:rw \
    -v ~/docker/isaac-sim-601/volume:/isaac-sim/volume:rw \
    -v ~/.cache/ov/hub:/var/cache/hub:rw \
    -u 1234:1234 \
    nvcr.io/nvidia/isaac-sim:6.0.1


## root 진입
docker exec -it -u 0 isaac-sim bash

## root 셸에서 실행
export HOME=/opt/claude
mkdir -p /opt/claude
curl -fsSL https://claude.ai/install.sh | bash
chmod -R a+rX /opt/claude
ln -sf /opt/claude/.local/bin/claude /usr/local/bin/claude

## isaac-sim 계정에서 확인.
which claude      # /usr/local/bin/claude
claude --version

```


# root 권한 필요시.
docker exec -it -u 0 isaac-sim bash


# standalone python script 실행시 
./python.sh

./runapp.sh
