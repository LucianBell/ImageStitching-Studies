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

