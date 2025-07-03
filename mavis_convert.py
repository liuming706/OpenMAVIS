import yaml
import numpy as np
import sys
import os

def to_matrix(list4x4):
    return np.array(list4x4, dtype=np.float64)

def load_yaml(filename):
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

def invert_transform(T):
    R = T[:3, :3]
    t = T[:3, 3]
    T_inv = np.eye(4)
    T_inv[:3, :3] = R.T
    T_inv[:3, 3] = -R.T @ t
    return T_inv

def print_matrix(name, mat):
    print(f"{name} =")
    print(np.array2string(mat, formatter={'float_kind':lambda x: f"{x: .6f}"}))
    print()

# === 处理命令行参数 ===
if len(sys.argv) != 2:
    print(f"Usage: python3 {os.path.basename(__file__)} config.yaml")
    sys.exit(1)

config_path = sys.argv[1]
config = load_yaml(config_path)

# === 主逻辑 ===
D_T_I = to_matrix(config['Imu']['D_T_I'])
I_T_D = invert_transform(D_T_I)

camera_dict = config['Camera']
camera_matrices = {}

for cam_key in camera_dict:
    if cam_key.startswith('camera'):
        D_T_C = to_matrix(camera_dict[cam_key]['D_T_C'])
        I_T_C = I_T_D @ D_T_C
        camera_matrices[cam_key] = {
            'D_T_C': D_T_C,
            'I_T_C': I_T_C
        }
        print_matrix(f"I_T_{cam_key}", I_T_C)

# === camera1 相对于 camera0 的变换 ===
D_T_C0 = camera_matrices['camera0']['D_T_C']
D_T_C1 = camera_matrices['camera1']['D_T_C']
C0_T_C1 = invert_transform(D_T_C0) @ D_T_C1

print_matrix("camera0_T_camera1", C0_T_C1)

