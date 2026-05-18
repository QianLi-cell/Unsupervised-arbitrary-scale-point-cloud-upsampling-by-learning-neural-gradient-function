import os
import numpy as np
import open3d as o3d


def read_xyz(file_path):
    points = np.loadtxt(file_path, delimiter=' ')
    return points


def write_xyz(points, file_path):
    np.savetxt(file_path, points, delimiter=' ', fmt='%.6f')


def compute_bounding_box(points):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    aabb = pcd.get_axis_aligned_bounding_box()
    min_vals = aabb.min_bound
    max_vals = aabb.max_bound
    center = aabb.get_center()
    return min_vals, max_vals, center


def rescale_point_cloud(processed_points, original_min, original_max, processed_min, processed_max, original_center):
    # Avoid division by zero with a small epsilon value
    epsilon = 1e-6

    # Compute scale factors for each axis
    scale_factors = (original_max - original_min) / (processed_max - processed_min + epsilon)

    # Use the minimum scale factor to maintain the aspect ratio of the point cloud
    uniform_scale_factor = min(scale_factors)

    # Rescale the processed points
    rescaled_points = (processed_points - processed_min) * uniform_scale_factor + original_min

    # Adjust the center to match the original point cloud center
    rescaled_points_center = compute_bounding_box(rescaled_points)[2]
    translation = original_center - rescaled_points_center
    rescaled_points += translation

    return rescaled_points


def main():
   # Get directory paths from user input
    # result_shape
    original_dir = "/home/gaot/Experiments_now/find_best_density/data/test_pointcloud/input_2048_2X/gt_4096"
    # question shape
    processed_dir = "/home/gaot/Experiments_now/new/NX/2X/log/240919_140258_PCPNet/test_20000/pred_normal"
    output_dir = "/home/gaot/Experiments_now/new/NX/2X/2X_rescale"

    # Check if directories are valid
    if not os.path.isdir(original_dir) or not os.path.isdir(processed_dir) or not os.path.isdir(output_dir):
        print("One or more directories are invalid.")
        return

    # Get list of files in each directory
    original_files = {os.path.splitext(f)[0]: f for f in os.listdir(original_dir) if f.endswith('.xyz')}
    processed_files = {os.path.splitext(f)[0]: f for f in os.listdir(processed_dir) if f.endswith('.xyz')}

    # Process each file pair
    for name in original_files:
        if name in processed_files:
            original_file_path = os.path.join(original_dir, original_files[name])
            processed_file_path = os.path.join(processed_dir, processed_files[name])

            # Read the point clouds
            original_points = read_xyz(original_file_path)
            processed_points = read_xyz(processed_file_path)

            # Compute bounding boxes and center
            original_min, original_max, original_center = compute_bounding_box(original_points)
            processed_min, processed_max, _ = compute_bounding_box(processed_points)

            # Ensure the bounding boxes are valid for scaling
            if np.any(processed_max - processed_min < 1e-6):
                print(f"Skipping file {name}: Processed point cloud has too small a bounding box.")
                continue

            # Rescale the processed point cloud
            rescaled_points = rescale_point_cloud(processed_points, original_min, original_max, processed_min,
                                                  processed_max, original_center)

            # Save the rescaled point cloud
            output_file_path = os.path.join(output_dir, processed_files[name])
            write_xyz(rescaled_points, output_file_path)
            print(f"Rescaled point cloud saved to {output_file_path}")


if __name__ == "__main__":
    main()
