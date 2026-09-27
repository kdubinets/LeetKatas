# Image Overlap

Given two binary `n x n` images, slide one by an integer number of rows and columns in either direction. Count positions containing `1` in both images after the slide, and return the greatest possible count. Translation moves every cell by the same offset, permits no rotation or reflection, and discards cells outside the image; nothing wraps around.

`1 <= n <= 30`. For example, a `1` at the upper-left corner of one image can be aligned with a `1` at the lower-right corner of the other by sliding diagonally.
