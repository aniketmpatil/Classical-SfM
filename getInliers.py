from IPython import embed
import argparse
import random
import Utils.FeatureUtils as FeatureUtils
import numpy as np

class Fundamental_Matrix:
    def __init__(self, args):
        self.epsilon = 0.5                # epsilon
        self.num_iters = 500              # M
        # self.num_points_ransac = 300    # N
        self.num_inliers = 0
        self.iter_inliers = {}
        self.final_inliers = {}
        self.F = np.zeros((3, 3))
        
        self.feature_utils = FeatureUtils()
        self.matched_features = self.feature_utils.read_matching_files(args.basePath)
        random.seed(40)

    def estimate_fundamental(self, eight_points):
        A = []
        for point in eight_points:
            a,b = point[1]
            c,d = point[0]
            row = [a*c,c*b,c,d*a,d*b,d,a,b,1]
            A.append(row)
        A = np.array(A)

        u, s, vh = np.linalg.svd(A, full_matrices=True)

        F = vh[:][8]
        F = F.reshape((3,3))
        return F

    def perform_ransac(self, image_pair):
        count_inliers = 0
        self.num_inliers = 0
        for i in range(self.num_iters):
            self.iter_inliers.clear()

            point_pairs_8 = random.sample(self.matched_features[image_pair], 8)
            F = self.estimate_fundamental(point_pairs_8)

            point_pairs = self.matched_features[image_pair]
            # random.sample(self.matched_features[image_pair], self.num_points_ransac)
            
            for point_pair in point_pairs:
                point1 = point_pair[0]
                point2 = point_pair[1]
                point1 = np.expand_dims(np.array([point1[0], point1[1], 1]), axis=1)
                point2 = np.expand_dims(np.array([point2[0], point2[1], 1]), axis=1)

                product = abs(np.matmul(np.matmul(point2.T, F), point1))
                # embed()
                if product < self.epsilon:
                    count_inliers += 1
                    self.update_inliers(image_pair, point_pair)
                    # self.feature_utils.add_inliers(image_pair, point_pair)
                    

            if (self.num_inliers < count_inliers):
                self.num_inliers = count_inliers
                self.final_inliers[image_pair] = self.iter_inliers[image_pair]
                self.F = F
                # embed()

        return self.final_inliers
    
    def update_inliers(self, img_idxs, point_pair):
        image_i_idx, image_j_idx = img_idxs
        image_i_u, image_i_v = point_pair[0]
        image_j_u, image_j_v = point_pair[1]
        if self.iter_inliers.get((image_i_idx, image_j_idx)) is not None:
            self.iter_inliers[(image_i_idx, image_j_idx)].append([(image_i_u, image_i_v), (image_j_u, image_j_v)])
        else:
            self.iter_inliers[(image_i_idx, image_j_idx)] = [[(image_i_u, image_i_v), (image_j_u, image_j_v)]]

    def get_F(self):
        return self.F


# parser = argparse.ArgumentParser()
# parser.add_argument('--basePath',default='./Data/')

# args = parser.parse_args()
# fundamental_matrix = Fundamental_Matrix()
# fundamental_matrix.perform_ransac()