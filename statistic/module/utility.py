import matplotlib.pyplot as plt

def show_distribution(fs, xs):
    n = len(fs)
    fig, axs = plt.subplots(nrows=1, ncols=n, figsize=(
        20, 5), sharex=True, sharey=True)

    for y, ax in zip(fs, axs):
        title, val = y
        ax.plot(xs, val)
        ax.set_title(title)
    plt.show()
