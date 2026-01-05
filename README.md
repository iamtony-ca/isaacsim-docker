# isaacsim-docker


# installation
https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/install_container.html


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




./runapp.sh