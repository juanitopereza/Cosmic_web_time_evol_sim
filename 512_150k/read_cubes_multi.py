from ast import literal_eval
from struct import *
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pylab import *

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


def read_CIC_vector(filename):
    f = open(filename, "rb")
    dumb = f.read(38)

    dumb = f.read(4)
    n_x = f.read(4)
    n_y = f.read(4)
    n_z = f.read(4)
    nodes = f.read(4)
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
    nodes = (unpack('i', nodes))[0]
    dx = (unpack('f', dx))[0]
    dy = (unpack('f', dy))[0]
    dz = (unpack('f', dz))[0]
    x0 = (unpack('f', x0))[0]
    y0 = (unpack('f', y0))[0]
    z0 = (unpack('f', z0))[0]
    print n_x, n_y, n_z, nodes, dx, dy, dz

    total_nodes = 3 * n_x * n_y *n_z
    dumb = f.read(4)
    array_data = f.read(total_nodes*4)
    dumb = f.read(4)
    format_s = str(total_nodes)+'f'
    array_data = unpack(format_s, array_data)
    f.close()
    array_data  = np.array(array_data)
    array_data.resize(n_z,n_y,n_x,3)
    vec = array_data[0,0,0,:]
    vec = array_data[0,0,1,:]
    array_data = array_data.transpose()
    #final shape is [3,n_x,n_y,n_z]
    return array_data


#filein="/store/04/bolshoi/V-web/clues/256/snap_190.CIC.s1.00.eigenvec_1"
def test_vector_plot():
    filein="/home/extforer/TV-Web/data/snap_136.s1.00.eigenvec_1"
    eigenvec_1 = read_CIC_vector(filein)

    x_component = eigenvec_1[0,:,:,:]
    x_component = x_component.flatten()
    x_component = np.absolute(x_component)

    print x_component.shape
    nbins = 20
    mu_bins = np.linspace(0.0,1.0,nbins)
    
    histo_mu_x, mu_x_range = np.histogram(x_component, bins=mu_bins)
    histo_mu_x = 1.0*histo_mu_x
    
    delta_x = 1.0/(1.0*nbins)
    histo_mu_x = histo_mu_x/sum(histo_mu_x)/delta_x
    print histo_mu_x, mu_x_range


    rc('text', usetex=True)
    rc('font', family='serif')

#plt.plot(mu_x_range[:-1], histo_mu_x, label="$e_{3}\cdot \hat{x}$")

    plt.plot(histo_mu_x, histo_mu_x, label="$e_{3}\cdot \hat{x}$")

    ylim([0.8, 1.2])
    xlim([0.0, 1.0])
    plt.legend(loc='upper left')
    plt.xlabel("$M_{1500}$")
    plt.ylabel("$\Phi(M_{1500})$ (Mpc$^{-3}$ mag$^{-1}$)")
    plt.savefig('BOX10909_smooth_1.0_align_e3.pdf')


def test_FA_plot(file1, file2, file3, name,  i):
    eigenval1  = read_CIC_scalar(file1)
    eigenval2  = read_CIC_scalar(file2)
    eigenval3  = read_CIC_scalar(file3)

    
    FA = (eigenval1-eigenval3)**2  + (eigenval2-eigenval3)**2  + (eigenval1-eigenval2)**2 
    FA = FA/(eigenval1**2 + eigenval2**2 + eigenval3**2)
    FA = np.sqrt(FA)/np.sqrt(3.0)

    cut = FA[40,:,:]
    
    print('size of FA:{0}'.format(shape(FA)))
    print('size of cut:{0}'.format(shape(cut)))
    plt.imshow(cut.T)
    plt.colorbar()
    plt.xlabel("x  $h^{-1}$ Mpc")
    plt.ylabel("y  $h^{-1}$ Mpc")
    print cut.min(), cut.max()
    if (i<10):
        plt.savefig(name + '_0{0}.pdf'.format(i))
	plt.close()
    else:
        plt.savefig(name + '_{0}.pdf'.format(i))
	plt.close()

#filein="/store/04/bolshoi/V-web/clues/256/snap_190.CIC.s8.00.eigen_1"
#eigen_1 = read_CIC_scalar(filein)

for i in range(0,31,1):
    if (i<10):
        file1="/hpcfs/home/ciencias/fisica/pregrado/js.perez20/Gadget-2.0.7/512_150k/bolshoi_128/snapshot_00{0}.eigen_1".format(i)
        print file1
        file2="/hpcfs/home/ciencias/fisica/pregrado/js.perez20/Gadget-2.0.7/512_150k/bolshoi_128/snapshot_00{0}.eigen_2".format(i)
        print file2
        file3="/hpcfs/home/ciencias/fisica/pregrado/js.perez20/Gadget-2.0.7/512_150k/bolshoi_128/snapshot_00{0}.eigen_3".format(i)
        print file3
        test_FA_plot(file1, file2, file3,'512_bolshoi_128_cut10',i)
    else:
        file1="/hpcfs/home/ciencias/fisica/pregrado/js.perez20/Gadget-2.0.7/512_150k/bolshoi_128/snapshot_0{0}.eigen_1".format(i)
        print file1
        file2="/hpcfs/home/ciencias/fisica/pregrado/js.perez20/Gadget-2.0.7/512_150k/bolshoi_128/snapshot_0{0}.eigen_2".format(i)
        print file2
        file3="/hpcfs/home/ciencias/fisica/pregrado/js.perez20/Gadget-2.0.7/512_150k/bolshoi_128/snapshot_0{0}.eigen_3".format(i)
        print file3
        test_FA_plot(file1, file2, file3,'512_bolshoi_128_cut10',i)
#eigen_1 = read_CIC_scalar(filein)
#print eigen_1.max(), eigen_1.min()
