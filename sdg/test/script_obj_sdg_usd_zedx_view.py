import omni.replicator.core as rep
import omni.usd
from omni.replicator.core import Writer, AnnotatorRegistry, BackendDispatch
import os
import asyncio
import numpy as np
import random
import math

# ---------------------------------------------------------------------------
# [설정]
# ---------------------------------------------------------------------------
RESOLUTION = (960, 600)
FOCAL_LENGTH = 5.0 
HORIZONTAL_APERTURE = 10.0
ENV_URL = "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/2023.1.1/Isaac/Environments/Simple_Warehouse/warehouse.usd"
TARGET_URL = "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/5.1/Isaac/Props/Shapes/torus.usd" 

# ---------------------------------------------------------------------------
# 1. Writer (필터링 기능 추가)
# ---------------------------------------------------------------------------
class YoloWriterZEDFinal(Writer):
    def __init__(self, output_dir, class_mapping, image_size):
        self.backend = BackendDispatch({"paths": {"out_dir": output_dir}})
        self.class_mapping = class_mapping
        self.width, self.height = image_size
        self._frame_id = 0
        self._save_count = 0
        self.annotators = [
            AnnotatorRegistry.get_annotator("rgb"),
            # [핵심 수정 1] Annotator에게 'target_class' 태그가 붙은 물체만 찾으라고 명령
            AnnotatorRegistry.get_annotator("bounding_box_2d_tight", init_params={"semanticTypes": ["target_class"]})
        ]
        os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "labels"), exist_ok=True)

    def write(self, data: dict):
        if self._frame_id == 0: 
            self._frame_id += 1
            return 

        try:
            rgb_data = None
            for key in data:
                if "rgb" in key:
                    rgb_data = data[key]
                    break
            
            filename = f"img_{self._save_count:06d}"
            if rgb_data is not None:
                self.backend.write_image(f"images/{filename}.png", rgb_data)
                
            bbox_raw = None
            for key in data:
                if "bounding_box_2d_tight" in key:
                    bbox_raw = data[key]
                    break
            
            txt_content = []
            if bbox_raw is not None:
                real_data = bbox_raw
                if isinstance(bbox_raw, dict) and 'data' in bbox_raw:
                    real_data = bbox_raw['data']
                if not isinstance(real_data, np.ndarray):
                    real_data = np.array(real_data)
                if real_data.ndim == 0:
                    real_data = np.expand_dims(real_data, 0)
                
                if real_data.size > 0:
                    for row in real_data:
                        try:
                            # 이제 여기 들어오는 데이터는 오직 '도넛' 뿐입니다.
                            x_min, y_min, x_max, y_max = float(row[1]), float(row[2]), float(row[3]), float(row[4])
                            x_c = ((x_min + x_max) / 2.0) / self.width
                            y_c = ((y_min + y_max) / 2.0) / self.height
                            w = (x_max - x_min) / self.width
                            h = (y_max - y_min) / self.height
                            
                            # 좌표 클리핑
                            x_c = np.clip(x_c, 0.0, 1.0)
                            y_c = np.clip(y_c, 0.0, 1.0)
                            w = np.clip(w, 0.0, 1.0)
                            h = np.clip(h, 0.0, 1.0)
                            
                            # 클래스 ID는 0 (도넛)으로 고정
                            txt_content.append(f"0 {x_c:.6f} {y_c:.6f} {w:.6f} {h:.6f}")
                        except:
                            pass

            label_path = os.path.join(self.backend.output_dir, f"labels/{filename}.txt")
            with open(label_path, "w") as f:
                f.write("\n".join(txt_content))
            
            print(f"[Writer] Frame {self._frame_id} -> Saved {filename}. (Box Count: {len(txt_content)})")
            self._save_count += 1

        except Exception as e:
            print(f"[Writer Error] {e}")
        finally:
            self._frame_id += 1

try:
    rep.WriterRegistry.register(YoloWriterZEDFinal)
except:
    pass

# ---------------------------------------------------------------------------
# 2. 씬 구성 및 실행
# ---------------------------------------------------------------------------
async def generate_data_zed_v38_clean_labels():
    print(f"\n[Start] Initializing V38 (Clean Labels Only)...")
    
    omni.usd.get_context().new_stage()
    
    # 1. 환경
    env = rep.create.from_usd(ENV_URL)
    
    # 안전 바닥
    safety_floor = rep.create.plane(position=(0, -0.05, 0), scale=100, visible=True)
    with safety_floor:
        rep.modify.material(rep.create.material_omnipbr(diffuse=(0.15, 0.15, 0.18), roughness=0.9))

    # 2. 도넛 (타겟)
    target = rep.create.from_usd(TARGET_URL, position=(0, 0.4, 0), scale=0.8, count=1)
    target_mat = rep.create.material_omnipbr(diffuse=(0.9, 0.1, 0.1), roughness=0.3)
    with target:
        # [핵심 수정 2] 일반 'class'가 아닌 'target_class'라는 특수 태그 부여
        # 이렇게 하면 창고의 다른 물건들(class='shelf' 등)과 섞이지 않음
        rep.modify.semantics([('target_class', 'donut')])
        rep.modify.material(target_mat)

    # 3. 조명
    dome_light = rep.create.light(light_type="Dome", intensity=1000)

    # 4. 방해물
    distractors = rep.create.group([
        rep.create.cube(scale=0.3),
        rep.create.cone(scale=0.3),
        rep.create.cylinder(scale=0.3)
    ])
    with distractors:
        # 방해물에는 semantics를 주지 않거나 기본값으로 둠 -> 라벨링 안 됨 (Good!)
        rep.randomizer.color(colors=rep.distribution.uniform((0,0,0), (1,1,1)))

    # [사용자 확정] Golden View Camera
    camera = rep.create.camera(
        position=(5.0, 0.0, 0.3), 
        rotation=(0, 0, 0),       
        focal_length=FOCAL_LENGTH,             
        horizontal_aperture=HORIZONTAL_APERTURE,
        focus_distance=400,
        clipping_range=(0.01, 1000000)
    )
    with camera:
        rep.create.light(light_type="Distant", intensity=3000, rotation=(0,0,0))

    render_product = rep.create.render_product(camera, RESOLUTION)

    output_path = os.path.join(os.path.expanduser("~"), "isaac_yolo_output_v38_clean")
    print(f"[Setup] Saving to: {output_path}")
    
    writer = rep.WriterRegistry.get("YoloWriterZEDFinal")
    writer.initialize(output_dir=output_path, class_mapping={'donut': 0}, image_size=RESOLUTION)
    
    # -----------------------------------------------------------------------
    # 랜덤화 로직
    # -----------------------------------------------------------------------
    def randomize_scene():
        # 도넛 이동
        with target:
            rep.modify.pose(
                position=rep.distribution.uniform((-0.5, -0.7, 0.3), (0.5, 0.7, 2.0)),
                rotation=rep.distribution.uniform((0, -180, 0), (0, 180, 0))
            )
        
        # 방해물 이동
        with distractors:
            rep.modify.pose(
                position=rep.distribution.uniform((-2.0, 0.25, -2.0), (2.0, 0.25, 2.0)),
                rotation=rep.distribution.uniform((0,-180,0), (0,180,0))
            )
            rep.randomizer.color(colors=rep.distribution.uniform((0.1,0.1,0.1), (0.9,0.9,0.9)))

        # 조명
        with dome_light:
            rep.modify.attribute("color", rep.distribution.uniform((0.8, 0.8, 0.8), (1.0, 0.9, 0.9)))

    # -----------------------------------------------------------------------
    # 실행
    # -----------------------------------------------------------------------
    print("[Warm-up] Initializing...")
    randomize_scene()
    for _ in range(20):
        await rep.orchestrator.step_async()

    print("[System] Attaching Writer...")
    writer.attach([render_product])
    await rep.orchestrator.step_async() 

    # [최종 양산] 50장 생성
    print("[Run] Generating 50 Clean Frames...")
    for i in range(5):
        randomize_scene()
        await rep.orchestrator.step_async()
        if i % 10 == 0:
            print(f"   -> Captured Frame {i+1}/50")
        
    print(f"[Done] Check folder: {output_path}")

import asyncio
asyncio.ensure_future(generate_data_zed_v38_clean_labels())
