import ikpy.chain
import ikpy.utils.plot as plot_utils
from math import degrees
import numpy as np

mychain = ikpy.chain.Chain.from_urdf_file('Scavbot.urdf')

target_position = [ 0, 0,0.58]

target_orientation = [-1, 0, 0]

ik = mychain.inverse_kinematics(target_position, target_orientation, orientation_mode='Y')
print("The angles of each joints are : ", list(map(lambda r:degrees(r),ik.tolist())))

computed_position = mychain.forward_kinematics(ik)
print("Computed position: %s, original position : %s" % (computed_position[:3, 3], target_position))
print("Computed position (readable) : %s" % [ '%.2f' % elem for elem in computed_position[:3, 3] ])

def doIK():
    global ik
    old_position= ik.copy()
    ik = mychain.inverse_kinematics(target_position, target_orientation, orientation_mode="Z", initial_position=old_position)

# def updatePlot():
#     ax.clear()
#     mychain.plot(ik, ax, target=target_position)
#     plt.xlim(-0.5, 0.5)
#     plt.ylim(-0.5, 0.5)
#     ax.set_zlim(0, 0.6)
#     fig.canvas.draw()
#     fig.canvas.flush_events()
    
def move(x,y,z):
    global target_position
    target_position = [x,y,z]
    doIK()
    # updatePlot()

    sendCommand(ik[1].item(),ik[2].item(),ik[3].item(),ik[4].item(),1)

    
def sendCommand(a,b,c,d): #e,f,move_time):
    # command = '0{:.2f} 1{:.2f} 2{:.2f} 3{:.2f} 4{:.2f} 5{:.2f} t{:.2f}\n'.format(degrees(a),degrees(b),degrees(c),degrees(d),degrees(e),degrees(f),move_time)
    # ser.write(command.encode('ASCII'))
    Drake.goTo(degrees(a))
    Kendrick.goTo(degrees(b))
    Jermaine.goTo(degrees(c))
    Metro.goTo(degrees(d))