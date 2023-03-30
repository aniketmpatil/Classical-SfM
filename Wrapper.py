import cv2
import argparse
import Utils.DataUtils as DataUtils
import Utils.FeatureUtils as FeatureUtils
from getInliers import Fundamental_Matrix
from IPython import embed

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--basePath',default='./Data/')
    
    args = parser.parse_args()

    imgs, image_names = DataUtils.import_images(args.basePath)
    print("Imported image files: ", len(image_names))

    K = DataUtils.load_camera_instrinsics(args.basePath)
    print("Camera Intrinsics Matrix:")
    print(K)

    # Get saved matches
    feature_utils = FeatureUtils()
    fundamental_matrix = Fundamental_Matrix(args)

    matched_features = feature_utils.read_matching_files(args.basePath)

    # image_pair = list(matched_features.keys())[0]
    pairs = [(2, 3), (2, 4), (2, 5)]
    
    for image_pair in pairs:
        feature_utils.plot_matches(imgs[image_pair[0]], imgs[image_pair[1]], matched_features[image_pair], f'Matched Pairs - {image_pair}')

        inliers = fundamental_matrix.perform_ransac(image_pair)

        feature_utils.plot_matches(imgs[image_pair[0]], imgs[image_pair[1]], inliers[image_pair], f'Inlier Pairs - {image_pair}')