# This software will check all mounted partitions on the system and will create a graph of the usage of the partitions. (WIP)

# Importing modules
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# function to get the current mounted partitions on the system
def get_mounted_partitions():
    partitions = subprocess.check_output(["sudo", "df", "-h"]).decode("utf-8")  # get the mounted partitions
    return partitions


# function to create a dataframe with the mounted partitions
def create_dataframe(partitions):
    partitions = partitions.split("\n")  # split the partitions into a list
    df = []
    for partition in partitions:
        if partition:
            partition = partition.split()
            df.append(partition)
    return df

# function to create the graph
def create_graph(df):
    fig, ax = plt.subplots()  
    ax.set_xlabel("Partition")
    ax.set_ylabel("Usage")
    ax.set_title("HDD Usage")
    ax.set_ylim(0, 100)  # set the y-axis range from 0 to 100
    ax.set_xlim(0, len(df))  
    ax.set_xticks(np.arange(len(df)))  # set the x axis to the partitions
    # ax.set_xticklabels(df[:, 0]) #partition name
    ax.set_yticks(np.arange(0, 101, 10))  # set the y axis to the usage
    ax.set_yticklabels(np.arange(0, 101, 10))  # set the y axis to the usage
    ax.grid(True)  # show the grid
    return fig, ax

#function to show graph to user
def show_graph(fig, ax):
    ani = animation.FuncAnimation(fig, update_graph, interval=1000, fargs=(ax,))  # update the graph every 1 second
    plt.show()

#function to update the graph
def update_graph(i, ax):
    df = create_dataframe(get_mounted_partitions())
    ax.clear()
    ax.set_xlabel("Partition")
    ax.set_ylabel("Usage")
    ax.set_title("HDD Usage")
    ax.set_ylim(0, 100)
    ax.set_xlim(0, len(df))
    ax.set_xticks(np.arange(len(df)))
    ax.set_xticklabels(df[:, 0])
    ax.set_yticks(np.arange(0, 101, 10))
    ax.set_yticklabels(np.arange(0, 101, 10))
    ax.grid(True)
    ax.plot(df[:, 0], df[:, 4])
    ax.legend(["Usage"])
    return ax

# main function
def main():
    partitions = get_mounted_partitions()
    df = create_dataframe(partitions)
    fig, ax = create_graph(df)
    show_graph(fig, ax)
    
    
if __name__ == "__main__":
    main()
    

# End of program