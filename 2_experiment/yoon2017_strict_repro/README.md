# Yoon2017 Strict Reproduction

Independent reconstruction of:

Yoon, Lee, Jung, and Shim, "Spline-based RRT* Using Piecewise Continuous Collision-checking Algorithm for Car-like Vehicles," Journal of Intelligent & Robotic Systems, 2017.

This package keeps the paper-level SS-RRT* structure separate from the local UGV benchmark code. It implements the Fig. 7 two-cubic-Bezier primitive with per-edge `gamma`, dominant trajectories, transition-rectangle collision checks, straight-segment rectangle checks, and RRT* rewiring. The original MATLAB code and exact simulation maps are not public in the paper bundle, so scene outputs in this folder are reconstructed smoke tests, not Table/Figure reproduction claims.
