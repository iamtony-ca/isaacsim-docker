
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
# 6.0.1
# 1) 6.0.1 전용 볼륨 마운트 디렉토리 (5.1.0과 분리)
mkdir -p ~/docker/isaac-sim-6.0.1/cache/main
mkdir -p ~/docker/isaac-sim-6.0.1/cache/computecache
mkdir -p ~/docker/isaac-sim-6.0.1/config
mkdir -p ~/docker/isaac-sim-6.0.1/data
mkdir -p ~/docker/isaac-sim-6.0.1/logs
mkdir -p ~/docker/isaac-sim-6.0.1/pkg
mkdir -p ~/docker/isaac-sim-6.0.1/volume
mkdir -p ~/.cache/ov/hub-6.0.1
sudo chown -R 1234:1234 ~/docker/isaac-sim-6.0.1 ~/.cache/ov/hub-6.0.1




# 
BASE=~/docker/isaac-sim-6.0.1
MYUID=$(id -u)          # tony, 아마 1000
# 기존 파일: tony 접근 허용
sudo setfacl -R -m u:$MYUID:rwx $BASE ~/.cache/ov/hub-6.0.1

# 앞으로 생길 파일: 양방향 상속(default ACL)
#  - 컨테이너(1234)가 만든 파일 → tony가 편집 가능
#  - tony가 만든 파일 → 컨테이너(1234)가 편집 가능
sudo setfacl -R -d -m u:$MYUID:rwx -m u:1234:rwx $BASE ~/.cache/ov/hub-6.0.1


BASE=~/docker/isaac-sim-6.0.1
MYUID=$(id -u)

# 기존 파일: tony + 1234 둘 다 rwx, 그리고 mask를 rwx로 (effective 깎임 방지)
sudo setfacl -R -m u:$MYUID:rwx -m u:1234:rwx -m m:rwx $BASE/volume

# 미래 파일: default ACL도 동일하게 + default mask rwx
sudo setfacl -R -d -m u:$MYUID:rwx -m u:1234:rwx -m m:rwx $BASE/volume



# 2) headless + livestream 실행
docker run --name isaac-sim-601 --entrypoint bash -it --gpus all -e "ACCEPT_EULA=Y" --rm --network=host \
    -e "PRIVACY_CONSENT=Y" \
    -v ~/docker/isaac-sim-6.0.1/cache/main:/isaac-sim/.cache:rw \
    -v ~/docker/isaac-sim-6.0.1/cache/computecache:/isaac-sim/.nv/ComputeCache:rw \
    -v ~/docker/isaac-sim-6.0.1/logs:/isaac-sim/.nvidia-omniverse/logs:rw \
    -v ~/docker/isaac-sim-6.0.1/config:/isaac-sim/.nvidia-omniverse/config:rw \
    -v ~/docker/isaac-sim-6.0.1/data:/isaac-sim/.local/share/ov/data:rw \
    -v ~/docker/isaac-sim-6.0.1/pkg:/isaac-sim/.local/share/ov/pkg:rw \
    -v ~/docker/isaac-sim-6.0.1/volume:/isaac-sim/volume:rw \
    -v ~/.cache/ov/hub-6.0.1:/var/cache/hub:rw \
    -u 1234:1234 \
    nvcr.io/nvidia/isaac-sim:6.0.1

```


# root 권한 필요시.
docker exec -it -u 0 isaac-sim bash


# standalone python script 실행시 
./python.sh

./runapp.sh
