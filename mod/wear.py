import json

import cv2
import numpy as np
from PIL import Image


def main(input_path, output_path, pathes):
    # カスケード分類器のdict
    classifiers = {
        name:cv2.CascadeClassifier(str(pathes['cascades_data'][name])) for name in pathes['cascades_data']
    }

    # マスクのパーツ座標
    with pathes['mask_data']['parts'].open() as f:
        source_parts = json.load(f)

    # 画像読み込み
    mask_image = cv2.imread(str(pathes['mask_data']['image']), -1) # 透過合成するためRGBAで取り込み
    input_image = cv2.imread(str(input_path), -1)
    input_gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    input_image_PIL = Image.open(input_path)

    # 画像内から顔をカスケード分類器で検出
    faces = classifiers['face'].detectMultiScale(input_gray, 1.05, 10)

    # 検出した顔ごとにマスクを重ねる処理を行う
    for (x,y,w,h) in faces:
        # パーツ認識用のグレースケールROI領域
        roi_gray = input_gray[y:y+h, x:x+w]

        # 顔の中からパーツを検出してROI内の相対座標を取得
        dest_parts = get_dest_parts(roi_gray, classifiers)

        # 検出できた（==座標がNoneでない）パーツ名を取得
        exist_parts = [p for p in dest_parts if dest_parts[p] is not None]

        # 幾何変換の起点と終点
        source_points = np.array([source_parts[part] for part in exist_parts], dtype=np.float32)
        dest_points = np.array([dest_parts[part] for part in exist_parts], dtype=np.float32)

        # 幾何変換行列作成
        mat = make_hom(source_points, dest_points)

        # マスク画像を幾何変換して顔に合わせる
        perspective_mask_image = cv2.warpPerspective(mask_image, mat, (2*w,2*h))

        # Pillowで透過合成
        perspective_mask_image_PIL = cv2pil(perspective_mask_image)
        input_image_PIL.paste(perspective_mask_image_PIL, (x, y), perspective_mask_image_PIL)

    # 画像保存
    input_image_PIL.save(str(output_path))

# 認識した顔からパーツの座標を取得
# 見つからなかった場合はNone
def get_dest_parts(roi, classifiers):
    w, h = roi.shape
    
    # 両目のみ同時に検出する
    eyes = eyes_centers(roi, classifiers['eyes'])
    eyes_exist = eyes[0] is not None

    # 両目の傾きで上下左右を補正
    eye_grad = (eyes[1][1]-eyes[0][1])/(eyes[1][0]-eyes[0][0]) if eyes_exist else 0

    return {
        'right_eye':  eyes[0],                                  # 右目（向かって左）
        'left_eye':   eyes[1],                                  # 左目（向かって右）
        'nose':       parts_centers('nose', roi, classifiers),  # 鼻
        'jaw':        [int(w/2 - eye_grad*h/2), h],             # アゴ先
        'right_side': [0, int(h/2 - eye_grad*w/2)],             # 右耳（向かって左端）
        'left_side':  [w, int(h/2 + eye_grad*w/2)],             # 左耳（向かって右端）
        'head_top':   [int(w/2 + eye_grad*h/2), 0]              # おでこの上端
    }

# 検出した領域の中心座標を返す
# 複数個見つかった場合はリスト順で0番目
def parts_centers(name, roi, classifiers):
    areas = classifiers[name].detectMultiScale(roi, 1.05, 10)
    
    if len(areas)==0:
        return None

    return [[ex+int(ew/2), ey+int(eh/2)] for ex, ey, ew, eh in areas][0]

# 両目が判定できているときのみそれぞれの中心座標を返す
# 返り値:(right_eye, left_eye) or (None, None)
def eyes_centers(roi, classifiers):
    areas = classifiers.detectMultiScale(roi, 1.05, 10)
    
    if len(areas)==2:
        points = [[ex+int(ew/2), ey+int(eh/2)] for ex, ey, ew, eh in areas]
        # x座標が最も小さいのが右目、最も大きいのが左目
        right_index = np.argmin(points, axis=0)[0]
        left_index = np.argmax(points, axis=0)[0]
        return (points[right_index], points[left_index])

    return (None, None)

# OpenCV型 -> PIL型の変換
def cv2pil(image):
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image

# ホモグラフィー行列を最小二乗法で作成
def make_hom(source_points, dest_points):
    A = np.zeros((source_points.shape[0]*2, 9))

    for i, (src, dst) in enumerate(zip(source_points, dest_points)):
        A[i*2] = np.array([
            src[0], src[1], 1, 0, 0, 0, -dst[0]*src[0], -dst[0]*src[1], -dst[0]])
        A[i*2 + 1] = np.array([
            0, 0, 0, src[0], src[1], 1, -dst[1]*src[0], -dst[1]*src[1], -dst[1]])
    
    _U, _s, V = np.linalg.svd(A, full_matrices=True)
    min_eigen = 8

    Hest = V[min_eigen].reshape((3,3))
    return Hest/Hest[2,2]
