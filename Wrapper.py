import cv2
import argparse
import Utils.DataUtils as DataUtils

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--basePath',default='./Data/')
    
    args = parser.parse_args()

    imgs, image_names = DataUtils.import_images(args.basePath)
    print("Imported image files: ", len(image_names))

    K = DataUtils.load_camera_instrinsics(args.basePath)
    print("Camera Intrinsics Matrix:")
    print(K)