import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import cmath
import math
import sys

T = 6
T_animation = T*1000*(0.01/2)*0.81

a, b, c, d = 100, 250, 300, 200
assert(b + c >= d + a)


Angle = 40
Angle_cg = Angle - 20

Len = 1
Len_cg = 0.7

ROTATION = ''
MODE = 'negative'
pen_pos = 'coupler'

step = 0.01
runtime = 6
if ROTATION == 'cw':
    th_a = np.arange(runtime*np.pi, 0, -step*np.pi)
else:
    th_a = np.arange(0, runtime*np.pi, step*np.pi)

th_a_d = th_a * 180/np.pi


# Freudenstein equation
K1 = d/a
K2 = d/c
K3 = (a**2-b**2+c**2+d**2)/(2*a*c)
A = np.cos(th_a) - K1 - K2*np.cos(th_a) + K3
B = -2*np.sin(th_a)
C = K1 - (K2+1)*np.cos(th_a) + K3

# Grashoff condition
disc = (B**2)-4*A*C

# Checks if the four_bar linkage is grashoff
if np.greater_equal(disc, 0).all() == False:
    print("not grashoff!!")
    assert(0)

if MODE == 'negative':
    th_c = 2*np.arctan((-B - np.sqrt(disc))/(2*A))
else:
    th_c = 2*np.arctan((-B + np.sqrt(disc))/(2*A))

# Degrees, used for drawing arcs
th_c_d = th_c * 180/np.pi

# the other point of ground
th_d = -np.pi*np.ones(len(th_c))

# polar to cartesian
phase1 = [cmath.exp(1j*i) for i in th_a]
phase3 = [cmath.exp(1j*i) for i in th_c]
phase4 = [cmath.exp(1j*i) for i in th_d]

R1 = a*np.array(phase1)
R3 = c*np.array(phase3)
R4 = -d*np.array(phase4)

x1, y1 = np.zeros(len(R1)), np.zeros(len(R1))
x2, y2 = np.real(R1), np.imag(R1)
x3, y3 = np.real(R3+R4), np.imag(R3+R4)
x4, y4 = np.real(R4), np.imag(R4)

th_b = np.arctan2((y3-y2), (x3-x2))

phase2 = [cmath.exp(1j*i) for i in th_b]
R2 = b*np.array(phase2)

f_d = Angle*np.pi/180*np.ones(len(th_a))
f_d += th_b

f_dCG = Angle_cg*np.pi/180*np.ones(len(th_a))
f_dCG += th_b
f = Len*b
fCG = Len_cg*b

# Phase of follower
phasef = [cmath.exp(1j*i) for i in f_d]
Rf = R1 + f*(np.array(phasef))
xf, yf = np.real(Rf), np.imag(Rf)

# Phase of follower centre of gravity
xfg_list, yfg_list = [], []
phasef_CG = [cmath.exp(1j*i) for i in f_dCG]
if pen_pos == 'center':
    Rf_CG = R1 + fCG*(np.array(phasef_CG))
    xfg, yfg = np.real(Rf_CG), np.imag(Rf_CG)
elif pen_pos == 'coupler':
    fCG = [i*b for i in [0.5]]
    Rf_CG = R1 + 0.5*b*(np.array(phase2))
    xfg, yfg = np.real(Rf_CG), np.imag(Rf_CG)
    for eachpos in fCG:
        Rf_CG = R1 + eachpos*(np.array(phase2))
        xfg_list.append(np.real(Rf_CG))
        yfg_list.append(np.imag(Rf_CG))

temp = x1, x2, x3, x4
xmin = np.amin([np.amin(mini) for mini in temp])
xmax = np.amax([np.amax(mini) for mini in temp])
temp = y1, y2, y3, y4
ymin = np.amin([np.amin(mini) for mini in temp])
ymax = np.amax([np.amax(mini) for mini in temp])

fig = plt.figure()
fig.set_size_inches(6, 6, True)
plt.axis('off')
y_ticks = np.arange(0, 301, 50)
bord = 100 

ax = fig.add_subplot(221, autoscale_on=False, xlim=(xmin-bord, xmax+bord), ylim=(ymin-bord, ymax+bord))
ax1 = fig.add_subplot(222, autoscale_on=False,xlim=(xmin-bord, xmax+bord), ylim=(ymin-bord, ymax+bord), sharex=ax, sharey=ax)

speedfig = fig.add_subplot(223, autoscale_on=True)
accefig = fig.add_subplot(224, autoscale_on=True)

ax.grid()
ax.set_ylabel('y_position')

for i in range(len(xfg_list)):
    ax1.plot(xfg_list[i], yfg_list[i], label=str(fCG[i]))

ax1.set_title('pen location', fontsize=12)
ax1.legend(loc="upper right")

speedlist, totalspeed = [], []

t_step = T*0.01/2
x_t = np.arange(0, 3*T-t_step, t_step)
for i in range(len(xfg_list)):
    speedlist = []
    for j in range(len(xfg_list[i])-1):
        distance = math.sqrt(((xfg_list[i][j] - xfg_list[i][j+1])**2 + (yfg_list[i][j] - yfg_list[i][j+1])**2))
        speedlist.append(distance/t_step)
    speedlist = np.array(speedlist)
    totalspeed.append(speedlist)
    speedfig.plot(x_t, speedlist, label=str(fCG[i]))
speedfig.set_xlabel('time (s)')
speedfig.set_title('speed for pen location', fontsize=12)
speedfig.set_ylabel('speed(cm/s)')
speedfig.legend(loc='upper right')

accelist = []
x_t = np.arange(0, 3*T-2*t_step-0.001, t_step)
for i in range(len(totalspeed)):
    accelist = []
    for j in range(len(totalspeed[i])-1):
        delta_v = (totalspeed[i][j+1] - totalspeed[i][j])
        accelist.append(delta_v/t_step)
    accelist = np.array(accelist)
    accefig.plot(x_t, accelist, label=str(fCG[i]))
accefig.set_xlabel('time (s)')
accefig.set_title('acceleration for pen location', fontsize=12)
accefig.set_ylabel('acceleration(cm/s**2)')
accefig.legend(loc='upper right')

line, = ax.plot([], [], marker='o', c='k', lw=6, ms=10)
if pen_pos == 'center':
    line2, = ax.plot([], [], marker='o', c='b', lw=6, ms=4)
line3, = ax.plot([], [], marker='x', c='g', lw=5, ms=20)
_ = ax.plot(xfg, yfg)

def init():
    line.set_data([], [])
    if pen_pos == 'center':
        line2.set_data([], [])
    line3.set_data([], [])

    if pen_pos == 'center':
        return line, line2, line3,
    return line, line3,

def animate(i):
    thisx = [x1[i], x2[i], x3[i], x4[i]]
    thisy = [y1[i], y2[i], y3[i], y4[i]]
    line.set_data(thisx, thisy)
    if pen_pos == 'center':
        thisx = [x2[i], xf[i], x3[i]]
        thisy = [y2[i], yf[i], y3[i]]
        line2.set_data(thisx, thisy)
    thisx = [x2[i], xfg[i]]
    thisy = [y2[i], yfg[i]]
    line3.set_data(thisx, thisy)
    if pen_pos == 'center':
        return line, line2, line3,
    return line, line3,

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y2)), interval=T_animation, blit=True, init_func=init)

plt.show()


