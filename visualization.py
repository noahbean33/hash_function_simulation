# visualization.py
"""
This module provides functions to visualize hash collision experiment results.
It uses Matplotlib to generate plots for collision statistics and bucket distributions.
"""

import matplotlib.pyplot as plt

def plot_collisions_vs_table_size(sweep_results, input_size, hash_func_name):
    """
    Plot total collisions and collision probability vs. hash table size for a fixed input size.
    
    Parameters:
        sweep_results (dict): Dictionary with keys as (table_size, input_size) and values as experiment results.
        input_size (int): The fixed number of inputs used in the experiment.
        hash_func_name (str): Name of the hash function used.
    """
    table_sizes = []
    collisions = []
    collision_probs = []
    
    for (table_size, n) in sweep_results:
        if n == input_size:
            table_sizes.append(table_size)
            collisions.append(sweep_results[(table_size, n)]["total_collisions"])
            collision_probs.append(sweep_results[(table_size, n)]["collision_probability"])
    
    # Sort data by table size
    sorted_data = sorted(zip(table_sizes, collisions, collision_probs), key=lambda x: x[0])
    table_sizes, collisions, collision_probs = zip(*sorted_data)
    
    # Plot total collisions vs. table size
    plt.figure()
    plt.plot(table_sizes, collisions, marker='o')
    plt.xlabel('Hash Table Size')
    plt.ylabel('Total Collisions')
    plt.title(f'Collisions vs. Table Size\n(Input Size: {input_size}, Function: {hash_func_name})')
    plt.grid(True)
    plt.show()
    
    # Plot collision probability vs. table size
    plt.figure()
    plt.plot(table_sizes, collision_probs, marker='x', color='red')
    plt.xlabel('Hash Table Size')
    plt.ylabel('Collision Probability')
    plt.title(f'Collision Probability vs. Table Size\n(Input Size: {input_size}, Function: {hash_func_name})')
    plt.grid(True)
    plt.show()

def plot_collision_probability_vs_input_size(sweep_results, table_size, hash_func_name):
    """
    Plot collision probability vs. number of inputs for a fixed hash table size.
    
    Parameters:
        sweep_results (dict): Dictionary with keys as (table_size, input_size) and values as experiment results.
        table_size (int): The fixed hash table size used in the experiment.
        hash_func_name (str): Name of the hash function used.
    """
    input_sizes = []
    collision_probs = []
    
    for (ts, n) in sweep_results:
        if ts == table_size:
            input_sizes.append(n)
            collision_probs.append(sweep_results[(ts, n)]["collision_probability"])
    
    # Sort data by input size
    sorted_data = sorted(zip(input_sizes, collision_probs), key=lambda x: x[0])
    input_sizes, collision_probs = zip(*sorted_data)
    
    plt.figure()
    plt.plot(input_sizes, collision_probs, marker='o')
    plt.xlabel('Number of Inputs')
    plt.ylabel('Collision Probability')
    plt.title(f'Collision Probability vs. Input Size\n(Table Size: {table_size}, Function: {hash_func_name})')
    plt.grid(True)
    plt.show()

def plot_bucket_distribution(bucket_counts, title):
    """
    Plot the distribution of items in each bucket as a bar chart.
    
    Parameters:
        bucket_counts (list): List of counts for each bucket.
        title (str): Title of the plot.
    """
    plt.figure(figsize=(10, 5))
    plt.bar(range(len(bucket_counts)), bucket_counts)
    plt.xlabel('Bucket Index')
    plt.ylabel('Number of Items')
    plt.title(title)
    plt.grid(True)
    plt.show()
