import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as spo

def get_data(name, mmin, mmax):
    f = open(name, 'r')
    S = f.readlines()
    f.close()
    JD, mag = [], []
    for i in range(len(S)):
        a = S[i].split()
        m = float(a[1])
        if m >= mmin and m <= mmax:
            JD.append(float(a[0]))
            mag.append(m)
    JD, mag = np.array(JD), np.array(mag)
    return JD, mag

def initial_plotting(JD, mag, inv, tp, ms, lw, title):
    fig = plt.figure(1)
    fig.set_size_inches(15, 8)
    plt.plot(JD, mag, tp, markersize=ms, linewidth=lw)
    plt.xlabel('JD - 2 457 000', fontsize=16)
    plt.ylabel('magnitude, mmag', fontsize=16)
    plt.title(title, fontsize=20)
    plt.rc('xtick', labelsize=16)
    plt.rc('ytick', labelsize=16)
    if inv:
        plt.gca().invert_yaxis()

def sm(y, N):
    Y = y.copy()
    for i in range(N, len(y) - N):
        Y[i] = 1 / (2 * N + 1) * np.sum([y[k] for k in range(i - N, i + N + 1)])
    return Y

def NN(T0, alpha):
    N = []
    Nmax = alpha * T0 * 584
    n = 2
    nn = 0
    while nn < Nmax:
        nn = int(0.7734 * np.exp(0.4484 * n))
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
    return x**2 * pp[0] + x * pp[1] + pp[2]

def parabolic_approximation(xxx, y, N):
    x = xxx.copy()
    x -= np.average(x)
    P = [0, 0, 0]
    ss = 1e99
    for i in range(N):
        p0 = np.random.uniform(-1, 1, 3)
        par = spo.leastsq(lambda pp: y - parabola(x, pp), p0, full_output=1)[0]
        s = np.sum((y - parabola(x, par))**2)
        if s < ss:
            ss = s
            P = par
    return P, x

def splitting(x, y, T0):
    alpha = 0.12
    yy, Nmax = smooth(T0, alpha, y)
    d = [(yy[i + 1] - yy[i]) / (x[i + 1] - x[i]) for i in range(len(x) - 1)]
    d = np.array(d)
    for N in [3, 5, 9, 13, 9, 5, 3]:
        d = sm(d, N)

    dd = [(d[i + 1] - d[i]) / (x[i + 2] - x[i + 1]) for i in range(len(x) - 2)]
    dd = np.array(dd)
    for N in [3, 5, 9, 13, 9, 5, 3]:
        dd = sm(dd, N)

    xx = x[Nmax + 1:-Nmax - 1].copy()
    start = [0]
    finish = []

    for i in range(len(xx) - 1):
        if xx[i + 1] - xx[i] > T0 * 0.5:
            finish.append(i)
            start.append(i + 1)
        if dd[i] * dd[i - 1] < 0:
            finish.append(i)
            start.append(i + 1)
    finish.append(len(xx) - 1)
    return start, finish

def if_extr_is_inside_interval(xxx, y):
    par, x = parabolic_approximation(xxx, y, 10)
    X = -0.5 * par[1] / par[0]
    return x[0] < X < x[-1]

def check_and_plot(x, y, T0):
    res = True
    if len(x) < 10:
        res = False
    else:
        if not 0.1 * T0 < (max(x) - min(x)) < T0:
            res = False
        in_int = if_extr_is_inside_interval(x, y)
        if not in_int:
            res = False
    return res

def check_up(x, y, start, finish, T0):
    i = 0
    while i < len(start):
        xx = x[start[i]:finish[i]]
        yy = y[start[i]:finish[i]]
        res = check_and_plot(xx, yy, T0)
        if not res:
            del start[i]
            del finish[i]
        else:
            plt.plot(xx, yy, '.', markersize=5)
            i += 1
    return start, finish

def save_data(start, finish, x, fname):
    fname = fname.replace('.tess', '.da!')
    data = ''
    for i in range(len(start)):
        data += str(start[i]) + ' ' + str(x[start[i]]) + ' ' + str(finish[i]) + ' ' + str(x[finish[i]]) + '\n'
    with open(fname, 'w') as f:
        f.writelines(data)




def open_light_curve():
    filename = filedialog.askopenfilename(initialdir="/", title="Open Light Curve File", filetypes=(("Text files", "*.tess"), ("all files", "*.*")))
    if filename:
        entry_filename.delete(0, tk.END) 
        entry_filename.insert(0, filename)  

        JD, mag = np.loadtxt(filename, unpack=True)
        ax.clear()
        ax.plot(JD, mag, '.k', markersize=6)
        ax.set_xlabel('JD - 2 457 000', fontsize=16)
        ax.set_ylabel('magnitude, mmag', fontsize=16)
        ax.set_title('Light Curve', fontsize=20)
        ax.invert_yaxis()
        canvas.draw()

def process_data():
    fname = entry_filename.get()
    T0 = float(entry_period.get())

    JD, mag0 = get_data(fname, -1000, 1000)

    
    

    initial_plotting(JD, mag0, True, '.k', 6, 0, fname)
    start, finish = splitting(JD, mag0, T0)
    start, finish = check_up(JD, mag0, start, finish, T0)
    save_data(start, finish, JD, fname)

    ax.set_xlabel('JD - 2 457 000', fontsize=16)
    ax.set_ylabel('magnitude, mmag', fontsize=16)
    ax.set_title('Final Light Curve', fontsize=20)
    if True:
        ax.invert_yaxis()

    canvas.draw()

def save_results():
    filename = filedialog.asksaveasfilename(defaultextension=".da!", filetypes=[("Data files", "*.da!")])
    if filename:
        with open(filename, 'w') as f:
            f.write(data)  


def clear_all():
    entry_filename.delete(0, tk.END)
    entry_period.delete(0, tk.END)
    ax.clear()
    canvas.draw()

# Initialize Tkinter and Matplotlib Figure
root = tk.Tk()
root.title("Splitter 3")
fig, ax = plt.subplots() 

# Tkinter Application
frame = tk.Frame(root)
label = tk.Label(text = "Splitter 3")
label.config(font=("DejaVu Sans", 32))
label.pack()
frame.pack()

# Create Canvas
canvas = FigureCanvasTkAgg(fig, master=root)  
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create Toolbar
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()
toolbar.pack(side=tk.BOTTOM, fill=tk.X)

# Open Light Curve Button
button_open_file = tk.Button(root, text="Open Light Curve File", command=open_light_curve)
button_open_file.pack(side=tk.LEFT, padx=10, pady=10)

# Entry for Filename
entry_filename = tk.Entry(root)
entry_filename.pack(side=tk.LEFT, padx=10, pady=10)

# Estimated Period Entry
label_period = tk.Label(root, text="Enter Estimated Period:")
label_period.pack(side=tk.LEFT, padx=15, pady=15)  
entry_period = tk.Entry(root)
entry_period.pack(side=tk.LEFT, padx=15, pady=10)  


# Process Button
button_process_data = tk.Button(root, text="Process Data", command=process_data)
button_process_data.pack(side=tk.LEFT, padx=10, pady=10) 

# Save Results Button
button_save_results = tk.Button(root, text="Save Results", command=save_results)
button_save_results.pack(side=tk.LEFT, padx=10, pady=10)  

# Clear Button
button_clear = tk.Button(root, text="Clear", command=clear_all)
button_clear.pack(side=tk.LEFT, padx=10, pady=10) 

# Run the Tkinter event loop
root.mainloop()