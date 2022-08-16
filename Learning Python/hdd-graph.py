# This software will check all mounted partitions on the system and will create a graph of the usage of the partitions. (WIP)

# Importing modules
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import pandas as pd



# Function to get the partitions
def get_partitions():
    partitions = subprocess.check_output(["sudo", "df", "-h"]).decode("utf-8").split("\n")
    partitions = partitions[1:]
    return partitions # Returns a list of all partitions

#create a dataframe to store the data
df = pd.DataFrame(columns=['partition', 'size', 'used', 'available', 'percentage'])



# # Function to get the usage of the partitions
# def get_usage(partitions):
#     usage = []
#     for partition in partitions:
#         usage.append(partition.split()[4])
#     return usage # Returns a list of all usage of the partitions

# # Function to get the usage of the partitions in percentages
# def get_usage_percent(partitions):
#     usage_percent = []
#     for partition in partitions:
#         usage_percent.append(partition.split())
#     return usage_percent # Returns a list of all usage of the partitions in percentages




# # Function to create the graph
# def create_graph(partitions, usage, usage_percent):
#     x = np.arange(len(usage))
#     y = usage
#     plt.bar(x, y, align="center", width=0.5)
#     plt.xticks(x, usage_percent)
#     plt.show()
#     plt.pause(0.001)
#     plt.close()
#     #plt.plot(x, y)
#     #plt.show()




# # Function to create the animation
# def create_animation(partitions, usage, usage_percent):
#     x = np.arange(len(usage))
#     y = usage
#     plt.bar(x, y, align="center", width=0.5)
#     plt.xticks(x, usage_percent)
#     plt.show()
#     plt.pause(0.001)
#     plt.close()
#     #plt.plot(x, y)
#     #plt.show()






# # Main function
# def main():
#     partitions = get_partitions()
#     usage = get_usage(partitions)
#     usage_percent = get_usage_percent(partitions)
#     create_graph(partitions, usage, usage_percent)
#     #create_animation(partitions, usage, usage_percent)
    


# # Calling the main function
# if __name__ == "__main__":
#     main()
#     print(get_partitions())
#     print(get_usage(get_partitions()))
#     print(get_usage_percent(get_partitions()))
    














# # function to get the current mounted partitions on the system
# def get_mounted_partitions():
#     partitions = subprocess.check_output(["sudo", "df", "-h"]).decode("utf-8")  # get the mounted partitions
#     return partitions


# # function to create a dataframe with the mounted partitions
# def create_dataframe(partitions):
#     partitions = partitions.split("\n")  # split the partitions into a list
#     df = []
#     for partition in partitions:
#         if partition:
#             partition = partition.split()
#             df.append(partition)  # append the partition to the dataframe
#     return df

# # function to create the graph
# def create_graph(df):
#     fig, ax = plt.subplots()  
#     ax.set_xlabel("Partition")
#     ax.set_ylabel("Usage")
#     ax.set_title("HDD Usage")
#     ax.set_ylim(0, 100)  # set the y-axis range from 0 to 100
#     ax.set_xlim(0, len(df))  
#     ax.set_xticks(np.arange(len(df)))  # set the x axis to the partitions
#     ##list indices must be integers or slices, not tuple
#     #ax.set_xticklabels(df[:, 0])  # partition name
#     ax.set_yticks(np.arange(0, 101, 10))  # set the y axis to the usage
#     ax.set_yticklabels(np.arange(0, 101, 10))  # set the y axis to the usage
#     ax.grid(True)  # show the grid
#     return fig, ax

# #function to show graph to user
# def show_graph(fig, ax):
#     ani = animation.FuncAnimation(fig, update_graph, interval=1000, fargs=(ax,))  # update the graph every 1 second
#     plt.show()

# #function to update the graph
# def update_graph(i, ax):
#     df = create_dataframe(get_mounted_partitions())
#     ax.clear()
#     ax.set_xlabel("Partition")
#     ax.set_ylabel("Usage")
#     ax.set_title("HDD Usage")
#     ax.set_ylim(0, 100)  # set the y-axis range from 0 to 100
#     ax.set_xlim(0, len(df))  
#     ax.set_xticks(np.arange(len(df)))  # set the x axis to the partitions
#     ##list indices must be integers or slices, not tuple
#     #ax.set_xticklabels(df[:, 0])  # partition name
#     ax.set_yticks(np.arange(0, 101, 10))
#     ax.set_yticklabels(np.arange(0, 101, 10))  # set the y axis to the usage
#     ax.grid(True)
#     ##list indices must be integers or slices, not tuple
#     ax.plot(df[:, 0], df[:, 4])  # plot the usage of the partitions
#     ax.legend(["Usage"])
#     return ax

# # main function
# def main():
#     partitions = get_mounted_partitions()  # get the mounted partitions
#     df = create_dataframe(partitions)  # create a dataframe with the partitions
#     fig, ax = create_graph(df)  # create the graph
#     show_graph(fig, ax)  # show the graph to the user
    
    
# if __name__ == "__main__":
#     main()
    

# # End of program