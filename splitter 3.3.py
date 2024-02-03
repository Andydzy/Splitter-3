import matplotlib.pyplot as plt
import scipy.optimize as spo
import numpy as np
import matplotlib



def get_data(name, mmin, mmax):
    f = open(name, 'r')
    S = f.readlines()
    f.close()
    JD, mag = [], []
    for i in range(len(S)):
        a = S[i].split()
        m = float(a[1])
        if m>=mmin and m<=mmax:
            JD.append(float(a[0]))
            mag.append(m)
    JD, mag = np.array(JD), np.array(mag)
    return JD, mag



def initial_plotting(JD, mag, inv, tp, ms, lw, title):   
    fig = plt.figure(1)
    fig.set_size_inches(15, 8)
    plt.plot(JD, mag, tp, markersize = ms, linewidth = lw)
    plt.xlabel('JD - 2 457 000', fontsize = 16)
    plt.ylabel('magnitude, mmag', fontsize = 16)
    plt.title(title, fontsize = 20)
    matplotlib.rc('xtick', labelsize=16)
    matplotlib.rc('ytick', labelsize=16)
    if inv == True:
        plt.gca().invert_yaxis()



def sm(y, N):
    Y = y.copy()
    for i in range(N, len(y)-N):
        Y[i] = 1/(2*N+1) * np.sum([y[k] for k in range(i-N, i+N+1)])
    return Y



def NN(T0, alpha):
    N = []
    Nmax = alpha*T0*584
    n = 2
    nn = 0
    while nn<Nmax:
        nn = int(0.7734*np.exp(0.4484*n))
        N.append(nn)
        n += 1
    return N



def smooth(T0, alpha, y):
    N = NN(T0, alpha)
    Y = y.copy()
    for i in range(len(N)):
        Y = sm(Y, N[i])
    for i in range(len(N)):
        Y = sm(Y, N[-i])
    return Y, max(N)



def parabola(x, pp):
    return x**2*pp[0] + x*pp[1] + pp[2]



def parabolic_approximation(xxx, y, N):
    x = xxx.copy()
    x -= np.average(x)
    P = [0, 0, 0]
    ss = 1e99
    for i in range(N):
        p0 = np.random.uniform(-1, 1, 3)
        par = spo.leastsq(lambda pp: y-parabola(x, pp), p0, full_output=1)[0]
        s = np.sum((y - parabola(x, par))**2)
        if s < ss:
            ss = s
            P = par
    return P, x



def splitting(x, y, T0):
    alpha = 0.12
    yy, Nmax = smooth(T0, alpha, y)
    ###################
    # initial_plotting(x, yy, False, '-c', 0, 3, '')
    d = [(yy[i+1]-yy[i])/(x[i+1]-x[i]) for i in range(len(x)-1)]
    d = np.array(d)
    for N in [3, 5, 9, 13, 9, 5, 3]:
        d = sm(d, N)
    
    dd = [(d[i+1]-d[i])/(x[i+2]-x[i+1]) for i in range(len(x)-2)]
    dd = np.array(dd)
    for N in [3, 5, 9, 13, 9, 5, 3]:
        dd = sm(dd, N)
    
    xx = x[Nmax+1:-Nmax-1].copy()
    start = [0]
    finish = []
    
    for i in range(len(xx)-1):
        if xx[i+1]-xx[i] > T0*0.5:
            finish.append(i)
            start.append(i+1)
        if dd[i]*dd[i-1] < 0:
            finish.append(i)
            start.append(i+1)
    finish.append(len(xx)-1)
    '''
    for i in range(len(start)):
        plt.plot(x[start[i]], yy[start[i]], 'or', markersize = 10)
    '''
    return start, finish



def if_extr_is_iside_interval(xxx, y):
    par, x = parabolic_approximation(xxx, y, 10)
    ######################
    # plt.plot(xxx, par[0]*x**2 + par[1]*x + par[2], '-r', linewidth = 2)
    
    X = -0.5*par[1]/par[0]
    if X>x[0] and X<x[-1]:
        return True
    else:
        return False



def ckeck_and_plot(x, y, T0):
    res = True
    if len(x)<10:
        res = False
    else:
        # print((max(x)-min(x))/T0)
        if ((max(x)-min(x)) < 0.1*T0) or ((max(x)-min(x)) > T0):
            res = False
        in_int = if_extr_is_iside_interval(x, y)
        if in_int == False:
            res = False
    return res



def check_up(x, y, start, finish, T0):
    i = 0
    while i<len(start):
        xx = x[start[i]:finish[i]]
        yy = y[start[i]:finish[i]]
        res = ckeck_and_plot(xx, yy, T0)
        if res == False:
            del start[i]
            del finish[i]
        else:
            ##########################
            plt.plot(xx, yy, '.', markersize = 5)
            i += 1
    return start, finish



def save_data(start, finish, x, fname):
    fname = fname.replace('.tess', '.da!')
    data = ''
    for i in range(len(start)):
        data += str(start[i]) + ' ' + str(x[start[i]]) + ' ' + str(finish[i]) + ' ' + str(x[finish[i]]) + '\n'
    f = open(fname, 'w')
    f.writelines(data)
    f.close()



fname = 'TIC_280055342_2023-05-04_mag.tess'
JD, mag0 = get_data(fname, -1000, 1000)

T0 = float(input('Вкажіть приблизний період зорі -> '))
# tp = input('Вкажіть категорію зорі: подвійна (B) чи пульсуюча (P) -> ')

initial_plotting(JD, mag0, True, '.k', 6, 0, fname)
start, finish = splitting(JD, mag0, T0)
start, finish = check_up(JD, mag0, start, finish, T0)
save_data(start, finish, JD, fname)