from ast import literal_eval
from struct import *
import numpy as np
import matplotlib.pyplot as plt
from pylab import *


mff_voids, mff_sheets, mff_fils, mff_knots = [], [], [], []

def read_CIC_scalar(filename):
    f = open(filename, "rb")
    dumb = f.read(38)

    dumb = f.read(4)
    n_x = f.read(4)
    n_y = f.read(4)
    n_z = f.read(4)
    nodes = f.read(8)
    x0 = f.read(4)
    y0 = f.read(4)
    z0 = f.read(4)
    dx = f.read(4)
    dy = f.read(4)
    dz = f.read(4)
    dumb = f.read(4)

    n_x = (unpack('i', n_x))[0]
    n_y = (unpack('i', n_y))[0]
    n_z = (unpack('i', n_z))[0]
    nodes = (unpack('q', nodes))[0]
    dx = (unpack('f', dx))[0]
    dy = (unpack('f', dy))[0]
    dz = (unpack('f', dz))[0]
    x0 = (unpack('f', x0))[0]
    y0 = (unpack('f', y0))[0]
    z0 = (unpack('f', z0))[0]
    print n_x, n_y, n_z, nodes, dx, dy, dz

    total_nodes = n_x * n_y *n_z
    dumb = f.read(4)
    array_data = f.read(total_nodes*4)
    dumb = f.read(4)
    format_s = str(total_nodes)+'f'
    array_data = unpack(format_s, array_data)
    f.close()
    array_data  = np.array(array_data)
    array_data.resize(n_z,n_y,n_x)
    array_data = array_data.transpose()
    return array_data

def classify(file1, file2, file3, lambda_th):

    eigenval1  = read_CIC_scalar(file1)
    eigenval2  = read_CIC_scalar(file2)
    eigenval3  = read_CIC_scalar(file3)

    rho = eigenval1 + eigenval2 + eigenval3 + np.ones(np.shape(eigenval1))

    val1 = eigenval1 >= lambda_th*np.ones(np.shape(eigenval1))
    val2 = eigenval2 >= lambda_th*np.ones(np.shape(eigenval2))
    val3 = eigenval3 >= lambda_th*np.ones(np.shape(eigenval3))
    
    chespirito = val1.astype(int) + val2.astype(int) + val3.astype(int)

    void = np.where(chespirito == 0)
    sheet = np.where(chespirito == 1)
    fil = np.where(chespirito == 2)
    knot = np.where(chespirito == 3)
    
    m_void = sum(rho[void])*(np.shape(void)[1]/128.0**3)
    m_sheet = sum(rho[sheet])*(np.shape(sheet)[1]/128.0**3)
    m_fil = sum(rho[fil])*(np.shape(fil)[1]/128.0**3)
    m_knot = sum(rho[knot])*(np.shape(knot)[1]/128.0**3)
    m_tot = m_void + m_sheet + m_fil + m_knot

#    print rho_void

#    print void

    mff_voids.append(m_void/m_tot)
    mff_sheets.append(m_sheet/m_tot)
    mff_fils.append(m_fil/m_tot)
    mff_knots.append(m_knot/m_tot)
    

#filein="/store/04/bolshoi/V-web/clues/256/snap_190.CIC.s8.00.eigen_1"
#eigen_1 = read_CIC_scalar(filein)

t = [0.090909091]
for i in range(30):
    t.append(t[i]*1.083211069549)

a = np.array(t)
z = 1/a - 1

for i in range(0,31,1):
    if (i<10):
        file1="/hpcfs/home/ciencias/fisica/pregrado/js.perez20/Gadget-2.0.7/512_150k/bolshoi_128/snapshot_00{0}.eigen_1".format(i)
        print file1
        file2="/hpcfs/home/ciencias/fisica/pregrado/js.perez20/Gadget-2.0.7/512_150k/bolshoi_128/snapshot_00{0}.eigen_2".format(i)
        print file2
        file3="/hpcfs/home/ciencias/fisica/pregrado/js.perez20/Gadget-2.0.7/512_150k/bolshoi_128/snapshot_00{0}.eigen_3".format(i)
        print file3
        classify(file1, file2, file3, 0.2/(1+z[i])**3)
    else:
        file1="/hpcfs/home/ciencias/fisica/pregrado/js.perez20/Gadget-2.0.7/512_150k/bolshoi_128/snapshot_0{0}.eigen_1".format(i)
        print file1
        file2="/hpcfs/home/ciencias/fisica/pregrado/js.perez20/Gadget-2.0.7/512_150k/bolshoi_128/snapshot_0{0}.eigen_2".format(i)
        print file2
        file3="/hpcfs/home/ciencias/fisica/pregrado/js.perez20/Gadget-2.0.7/512_150k/bolshoi_128/snapshot_0{0}.eigen_3".format(i)
        print file3
        classify(file1, file2, file3, 0.2/(1+z[i])**3)


plt.plot(z,mff_voids, 'bo', label='Voids')
plt.plot(z,mff_sheets, 'r--', label='Sheets')
plt.plot(z,mff_fils, 'ys', label='Filaments')
plt.plot(z,mff_knots, 'g^', label='Knots')
plt.gca().invert_xaxis()
plt.xlim(z[0],0)
plt.legend(bbox_to_anchor=(0.7,1))
plt.xlabel('z')
plt.ylabel('MFF')
plt.title('MFF $\lambda_{th}(z)=\lambda_0/(1+z)^3$')
plt.savefig('mff_lt.pdf')


#eigen_1 = read_CIC_scalar(filein)
#print eigen_1.max(), eigen_1.min()
