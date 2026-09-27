# Wiggle Subsequence

A wiggle sequence has successive differences that strictly alternate between positive and negative; either sign may come first. A single element is a wiggle sequence, and equal consecutive chosen values do not form a valid difference. Given an array of up to 1,000 integers in `[0,1000]`, return the length of its longest **subsequence** with this property. A subsequence may skip entries but keeps their original order.

For `[1,2,3,4]`, the answer is 2: any increasing pair works, but no longer subsequence alternates.
