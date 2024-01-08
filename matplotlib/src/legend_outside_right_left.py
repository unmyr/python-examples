"""Place a legend outside of plot axes."""
import matplotlib.pyplot as plt
import numpy as np


def main():
    """Run main."""
    # Generate random data for plotting
    x = np.linspace(0.0, 100, 20)

    # now there's 3 sets of points
    y1 = np.random.normal(scale=0.2, size=20)
    y2 = np.random.normal(scale=0.5, size=20)
    y3 = np.random.normal(scale=0.8, size=20)

    # Get figure
    fig = plt.figure(figsize=(6, 8))
    fig.suptitle("Figure title", fontsize=16)

    # Get axis
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.set_title("Random data")
    ax1.plot(x, y1, label="plot 1")
    ax1.plot(x, y2, label="plot 2")
    ax1.plot(x, y3, label="plot 3")
    ax1.legend(loc="upper left", bbox_to_anchor=(1.0, 0.5))

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.set_title("Random data")
    ax2.plot(x, y1, label="plot 1")
    ax2.plot(x, y2, label="plot 2")
    ax2.plot(x, y3, label="plot 3")
    ax2.legend(loc="upper right", bbox_to_anchor=(-0.15, 0.5))

    fig.tight_layout()
    fig.show()


if __name__ == "__main__":
    main()

# EOF
