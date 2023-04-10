import cv2
import argparse
import Utils.DataUtils as DataUtils
import Utils.FeatureUtils as FeatureUtils
from getInliers import Fundamental_Matrix
from extract_camera_pose import *
from LinearTriangulation import*
from IPython import embed

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--basePath', default='./Data/')
    
    args = parser.parse_args()

    data_utils = DataUtils(args.basePath)
    imgs, image_names = data_utils.import_images()
    print("Imported image files: ", len(image_names))

    K = data_utils.load_camera_instrinsics()
    print("Camera Intrinsics Matrix:")
    print(K)

    # Get saved matches
    feature_utils = FeatureUtils()
    fundamental_matrix = Fundamental_Matrix(args)

    matched_features = feature_utils.read_matching_files(args.basePath)

    # image_pair = list(matched_features.keys())[0]
    pairs = [(1,2)]
    
    for image_pair in pairs:
        # feature_utils.plot_matches(imgs[image_pair[0]], imgs[image_pair[1]], matched_features[image_pair], f'Matched Pairs - {image_pair}')

        inliers = fundamental_matrix.perform_ransac(image_pair)

        E = fundamental_matrix.get_essential_from_fundamental()

        # embed()
        # Test Fundamental Matrix
        # fundamental_matrix.show_epipolar_lines(inliers[image_pair], imgs[image_pair[0]], imgs[image_pair[1]])
        
        R,C = extract_cam_pose(E)
        R0 = np.eye(3)
        C0 = np.zeros((3,1))
        for Ri,Ci in zip(R,C):
            Xn = triangulation(R0,C0,Ri,Ci,inliers[image_pair],K)

        # feature_utils.plot_matches(imgs[image_pair[0]], imgs[image_pair[1]], inliers[image_pair], f'Inlier Pairs - {image_pair}')

    
        