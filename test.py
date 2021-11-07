import matplotlib

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import multiprocessing
import time
import random
from Tkinter import *

# Create a window
window = Tk()


def main():
    q = multiprocessing.Queue()
    simulate = multiprocessing.Process(None, simulation, args=(q,))
    simulate.start()
    plot()
    updateplot(q)
    window.mainloop()
    print 'Done'


def plot():
    global line, ax, canvas
    fig = matplotlib.figure.Figure()
    ax = fig.add_subplot(1, 1, 1)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.show()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
    line, = ax.plot([1, 2, 3], [1, 2, 10])


def updateplot(q):
    try:
        result = q.get_nowait()

        if result != 'Q':
            print result
            line.set_ydata([1, result, 10])
            ax.draw_artist(line)
            canvas.draw()
            window.after(500, updateplot, q)
        else:
            print 'done'
    except:
        print "empty"
        window.after(500, updateplot, q)


def simulation(q):
    iterations = xrange(100)
    for i in iterations:
        if not i % 10:
            time.sleep(1)
            # here send any data you want to send to the other process, can be any pickable object
            q.put(random.randint(1, 10))
    q.put('Q')


if __name__ == '__main__':
    main()
