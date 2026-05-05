# Fundamentals

## What is Image Stitching

- Image stitching is a fascinating technique that combines multiple images to create a seamless panoramic image.
- This technique involves **aligning and blending** the images to create a seamless and high-resolution composite.

Key steps include:

1. Image Acquisition: Capture multiple images of the scene with overlapping areas. These images are usually taken with a **consistent orientation and similar exposure settings**.

2. Feature Detection: Identify distinctive features (like corners, edges, or specific patterns) in each image. Common algorithms for this task include **SIFT (Scale-Invariant Feature Transform), SURF (Speeded-Up Robust Features), and ORB (Oriented FAST and Rotated BRIEF)**.

3. Feature Matching: **Corresponding features between overlapping images are matched**. This step aligns the images by finding pairs of similar features.

4. Homography Estimation: Compute a transformation matrix (homography) that **aligns one image with the next**. This matrix describes how to warp one image to match the perspective of another.

5. Image Warping and Alignment: Apply the homography matrix to **warp images into a common coordinate frame** so that they overlap correctly.

6. Blending: Seamlessly **blend the overlapping areas** to reduce visible seams and ensure a smooth transition between images. Techniques like feathering, multi-band blending, and exposure compensation are often used.

7. Rendering: Combine the aligned and blended images into a single panoramic image. This may involve cropping to remove unwanted edges and adjusting the final image's exposure and color balance.

## Explaining Each Part

## SIFT (Scale-Invariant Feature Transform (SIFT))
> [!INFO] [video playlist here](https://www.youtube.com/watch?v=KgsHoJYJ4S8&list=PLlCkKK04bmVlvCs-S-2DnGf08MY2Hdd0n)

- This is an algorithm that **identifies distinctive keypoints** (step 2), often "blobs", that remain **robust and consistent across varying scales, rotations, and lighting conditions**
    - Uses include object recognition, robotic mapping and navigation, image stitching, 3D modeling, gesture recognition, video tracking, individual identification of wildlife and match moving.
- What is an interest point?
    - It is usally determined as a "blob" with a local appearence within it.
- A lot of the algorithm here is based in **blob detection theory.**
    - Methods used to identify such elements can detect the determined blobs over multiple scales, positions and magnification
- Basically, with this we can create a **SIFT Detector**
- With a SIFT detector, we can detect the points of interest. However, to match interest points in two images you need a signature that descriptes the local appearence, and that is when we need to have a **SIFT Descriptor**.

