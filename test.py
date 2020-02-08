import matplotlib.pyplot as plt
import math
import cmath

# d1 = int(input("Enter length of frame : "))
# d2 = int(input("Enter length of coupler : "))
# d3 = int(input("Enter length of crank : "))
# d4 = int(input("Enter length of follower : "))
d1, d2, d3, d4 = 205, 200, 50, 150

list1 = [d1, d2, d3, d4]
list1.sort()
s, l, p, q = list1[0], list1[3], list1[1], list1[2]

# if (s+l) <= (p+q):
#     if d1 == d2 and d3 == d4:
#         print("Parallel-crank mechanism")
#     elif d1 == list1[0]:
#         print("Drag-link mechanism")
#     elif d3 == list1[0] or d4 == list1[0]:
#         print("Crank-rocker mechanism")
# elif (s+l) > (p+q):
#     print("Double-rocker mechanism")
# else:
#     print("Rocker-crank mechanism")

def main():
    d1, d2, d3, d4 = 205, 200, 50, 150
    if (s+l) <= (p+q) and (d3 == list1[0] or d4 == list1[0]):
        # crank_velocity = int(input("Enter angular velocity of the crank: "))
        # crank_acceleration = int(input("Enter angular acceleration of the crank: "))

        # vector loop equation method
        # the four bar linkage is on an x-y frame with the frame on the x-axis and the crank on the y-axis
        # frame angle is therefore zero
        # d3*cos(crank_angle) + d2*cos(coupler_angle) - d4*(follower_angle) - d1 = 0
        # d3*sin(crank_angle) + d2*sin(coupler_angle) - d4*sin(follower_angle) = 0
        crank_angle = []
        follower_angle = []
        follower_angle2 = []
        coupler_angle = []
        for angle in range(0, 365, 5):
            crank_angle.append(angle)
            
            k1 = d1/d3
            k2 = d1/d4
            k3 = ((d3**2) - (d2**2) + (d1**2) + (d4**4)) / (2*d2*d4)
            A = (1 - k2)*(math.cos(angle)) - k1 + k3
            B = -2*math.sin(angle)
            C = k1 - (1 + k2)*math.cos(angle) - k3

            #calculating follower angles
            follower_angle.append(math.degrees(2 * (math.atan((-B + math.sqrt(B**2 - 4*A*C) / (2*A))))))
            follower_angle2.append(math.degrees(2 * (math.atan((-B - math.sqrt(B**2 - 4*A*C) / (2*A))))))
            
            #calculating coupler angle
            coupler_angle.append(math.degrees(math.asin((d4*math.sin(follower_angle) - d3*math.sin(crank_angle)) / d2)))
            print(coupler_angle)

        plt.title("Angular displacement variations")
        plt.xlabel("crank displacement")
        plt.ylabel("follower displacement")
        plt.plot(crank_angle, follower_angle)
        plt.plot(crank_angle, follower_angle2)

        # plt.plot(crank_angle, coupler_angle)

        plt.show()
        
if __name__ == "__main__":
    main()
