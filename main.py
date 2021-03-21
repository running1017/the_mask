import re
from pathlib import Path

from mod import wear

# 必要データ
pathes = {
    'input':    Path('./image/input/'),
    'output':   Path('./image/output/'),
    'cascades': Path('./data/cascades/'),
    'mask':     Path('./data/mask/')
}
pathes['cascades_data'] = {
    'face': pathes['cascades'] / 'haarcascade_frontalface_alt.xml',
    'eyes': pathes['cascades'] / 'haarcascade_eye.xml',
    'nose': pathes['cascades'] / 'haarcascade_mcs_nose.xml'
}
pathes['mask_data'] = {
    'image': pathes['mask'] / 'mask.png',
    'parts': pathes['mask'] / 'mask_parts.json'
}

def main():
    check_dir()

    for input_image_path in get_input_images(pathes['input']):
        output_image_path = \
            pathes['output'] / (input_image_path.stem + "_weared" + input_image_path.suffix)
        print("wear on " + str(input_image_path))
        wear.main(input_image_path, output_image_path, pathes)

# ディレクトリ整合性チェック
def check_dir():
    for p in ['input', 'output', 'cascades', 'mask']:
        pathes[p].mkdir(parents=True, exist_ok=True)

# 読み込み可能な拡張子のファイル一覧取得
def get_input_images(input_dir):
    convertible_format = ['jpg', 'png']
    re_pattern = r'.*\.(' + '|'.join(convertible_format) + ')'
    files = [p for p in input_dir.glob('*') if re.search(re_pattern, str(p))]

    # generator化
    for img_path in files:
        yield img_path

if __name__=='__main__':
    main()
