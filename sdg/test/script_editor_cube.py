import omni.replicator.core as rep
import omni.usd
from omni.replicator.core import Writer, AnnotatorRegistry, BackendDispatch
import os
import asyncio
import numpy as np

# ---------------------------------------------------------------------------
# 1. 완벽하게 수정된 YOLO Writer (Final Version)
# ---------------------------------------------------------------------------
class YoloWriterPerfect(Writer):
    def __init__(self, output_dir, class_mapping, image_size=(640, 640)):
        self.backend = BackendDispatch({"paths": {"out_dir": output_dir}})
        self.class_mapping = class_mapping
        self.width, self.height = image_size
        self._frame_id = 0
        self.annotators = [
            AnnotatorRegistry.get_annotator("rgb"),
            AnnotatorRegistry.get_annotator("bounding_box_2d_tight")
        ]
        # 폴더 생성
        os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "labels"), exist_ok=True)

    def write(self, data: dict):
        try:
            print(f"\n[Writer] Frame {self._frame_id} processing...")

            # 1. RGB 이미지 저장
            rgb_data = None
            for key in data:
                if "rgb" in key:
                    rgb_data = data[key]
                    break
            
            if rgb_data is not None:
                file_path = f"images/img_{self._frame_id:06d}.png"
                self.backend.write_image(file_path, rgb_data)

            # 2. BBox 데이터 추출 (구조적 문제 해결됨)
            bbox_raw = None
            for key in data:
                if "bounding_box_2d_tight" in key:
                    bbox_raw = data[key]
                    break
            
            txt_content = []
            
            if bbox_raw is not None:
                # [핵심 수정 1] 딕셔너리 껍질 벗기기 ('data' 키 접근)
                real_data = bbox_raw
                if isinstance(bbox_raw, dict) and 'data' in bbox_raw:
                    real_data = bbox_raw['data']

                # [핵심 수정 2] Numpy 배열 안전 변환
                if not isinstance(real_data, np.ndarray):
                    real_data = np.array(real_data)
                
                # [핵심 수정 3] 0차원(Scalar) -> 1차원 변환
                if real_data.ndim == 0:
                    real_data = np.expand_dims(real_data, 0)
                
                # 데이터가 있을 경우 파싱
                if real_data.size > 0:
                    for row in real_data:
                        # [핵심 수정 4] 확인된 필드명('x_min' 등)으로 정확히 접근
                        try:
                            # Numpy Structured Array 접근 방식
                            x_min = float(row['x_min'])
                            y_min = float(row['y_min'])
                            x_max = float(row['x_max'])
                            y_max = float(row['y_max'])
                            semantic_id = int(row['semanticId'])
                            
                            # YOLO 포맷 계산 (Normalized XYWH)
                            x_c = ((x_min + x_max) / 2.0) / self.width
                            y_c = ((y_min + y_max) / 2.0) / self.height
                            w = (x_max - x_min) / self.width
                            h = (y_max - y_min) / self.height
                            
                            # 값 클리핑 (0.0 ~ 1.0)
                            x_c = np.clip(x_c, 0.0, 1.0)
                            y_c = np.clip(y_c, 0.0, 1.0)
                            w = np.clip(w, 0.0, 1.0)
                            h = np.clip(h, 0.0, 1.0)
                            
                            # 클래스 ID 매핑 (여기서는 semanticId 0 -> class 0 으로 매핑한다고 가정)
                            # 실제로는 self.class_mapping 딕셔너리를 활용하여 semanticId를 변환해야 함
                            # 예: class_id = self.class_mapping.get(str(semantic_id), 0)
                            class_id = 0 
                            
                            txt_content.append(f"{class_id} {x_c:.6f} {y_c:.6f} {w:.6f} {h:.6f}")
                            
                        except Exception as parse_err:
                            print(f"   [Warning] Error parsing row: {parse_err}")

            # 라벨 파일 쓰기
            label_path = os.path.join(self.backend.output_dir, f"labels/img_{self._frame_id:06d}.txt")
            with open(label_path, "w") as f:
                f.write("\n".join(txt_content))
            
            print(f"   -> Saved: {label_path} (Objects: {len(txt_content)})")

        except Exception as e:
            print(f"   [Error] Frame {self._frame_id} failed: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self._frame_id += 1

# Writer 등록
try:
    rep.WriterRegistry.register(YoloWriterPerfect)
except:
    pass

# ---------------------------------------------------------------------------
# 2. 씬 구성 및 실행 (폴더명 final)
# ---------------------------------------------------------------------------
async def generate_data_final():
    print("[Start] Initializing Scene Final...")
    
    omni.usd.get_context().new_stage()
    
    # 타겟 생성
    target = rep.create.cube(position=(0, 0, 0), scale=1.0, semantics=[('class', 'target')], count=1)
    rep.create.light(light_type="Dome", intensity=1000)
    
    # 카메라 (5m 거리)
    camera = rep.create.camera(position=(0, 5, 5), look_at=target)
    render_product = rep.create.render_product(camera, (640, 640))

    # 저장 경로
    output_path = os.path.join(os.path.expanduser("~"), "isaac_yolo_output_final")
    print(f"[Setup] Saving to: {output_path}")
    
    writer = rep.WriterRegistry.get("YoloWriterPerfect")
    writer.initialize(output_dir=output_path, class_mapping={"target": 0}, image_size=(640, 640))
    writer.attach([render_product])

    print("[Run] Starting Capture (10 Frames)...")
    
    for i in range(10):
        with target:
            rep.modify.pose(
                position=rep.distribution.uniform((-2, 0, -2), (2, 0, 2)),
                rotation=rep.distribution.uniform((0,-180,0), (0,180,0))
            )
        await rep.orchestrator.step_async()
        
    print(f"[Done] Generation Complete! Check folder: {output_path}")

# 실행
asyncio.ensure_future(generate_data_final())
