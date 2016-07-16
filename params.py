# This is robots parameters
#

G = 9.81
m1 = 0.1
m2 = 0.01
L1 = 0.08
L2 = 0.18
I1 = m1 * (L1**2) / 3 
I2 = m2 * (L2**2) / 12 

z0 = 0.02 # leverage of the leg's servo
z1 = 0.02 
z2 = 0.02
k1 = 300 # spring's coeffs
k2 = 300
dz = 0.05 # initial stretch of the springs

miu_a = 0.015
