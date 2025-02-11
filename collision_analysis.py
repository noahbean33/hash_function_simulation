# collision_analysis.py
"""
This module performs collision analysis experiments.
It includes functions to generate inputs, run a single collision experiment, and perform parameter sweeps.
"""

import random
import string

def generate_random_integers(n, low=0, high=1000000):
    """
    Generate a list of random integers.
    
    Parameters:
        n (int): Number of integers to generate.
        low (int): Minimum value (inclusive).
        high (int): Maximum value (inclusive).
        
    Returns:
        list: List of random integers.
    """
    return [random.randint(low, high) for _ in range(n)]

def generate_random_strings(n, length=10):
    """
    Generate a list of random strings.
    
    Parameters:
        n (int): Number of strings to generate.
        length (int): Length of each string.
        
    Returns:
        list: List of random strings.
    """
    characters = string.ascii_letters + string.digits
    return [''.join(random.choices(characters, k=length)) for _ in range(n)]

def generate_structured_sequence(n):
    """
    Generate a structured sequence of integers (e.g., a sequence from 0 to n-1).
    
    Parameters:
        n (int): Number of elements in the sequence.
        
    Returns:
        list: List of integers.
    """
    return list(range(n))

def get_inputs(distribution, n, **kwargs):
    """
    Generate input data based on the specified distribution.
    
    Parameters:
        distribution (str): Type of distribution ('random_integers', 'random_strings', or 'structured').
        n (int): Number of inputs to generate.
        **kwargs: Additional keyword arguments for the generator functions.
        
    Returns:
        list: List of generated inputs.
    """
    if distribution == "random_integers":
        return generate_random_integers(n, **kwargs)
    elif distribution == "random_strings":
        return generate_random_strings(n, **kwargs)
    elif distribution == "structured":
        return generate_structured_sequence(n)
    else:
        raise ValueError("Unknown distribution type: " + distribution)

def run_collision_experiment(hash_func, table_size, inputs, **kwargs):
    """
    Run a collision experiment using a specified hash function, hash table size, and inputs.
    
    Parameters:
        hash_func (callable): The hash function to use. Should accept (value, table_size, **kwargs).
        table_size (int): Size of the hash table.
        inputs (list): List of input values.
        **kwargs: Additional keyword arguments to pass to the hash function.
        
    Returns:
        dict: Results containing total collisions, collision probability, and bucket distribution.
    """
    bucket_counts = [0] * table_size
    collisions = 0
    for value in inputs:
        idx = hash_func(value, table_size, **kwargs)
        if bucket_counts[idx] > 0:
            collisions += 1  # A collision occurs if the bucket already has an item.
        bucket_counts[idx] += 1
    return {
        "total_collisions": collisions,
        "collision_probability": collisions / len(inputs),
        "bucket_counts": bucket_counts
    }

def run_sweep_experiments(hash_func, table_sizes, input_sizes, distribution, **gen_kwargs):
    """
    Run collision experiments over a sweep of table sizes and input sizes.
    
    Parameters:
        hash_func (callable): The hash function to test.
        table_sizes (list): List of hash table sizes.
        input_sizes (list): List of input sizes (number of inputs).
        distribution (str): Input distribution type.
        **gen_kwargs: Additional keyword arguments for input generation.
        
    Returns:
        dict: Dictionary with keys as (table_size, input_size) and values as experiment results.
    """
    results = {}
    for table_size in table_sizes:
        for input_size in input_sizes:
            inputs = get_inputs(distribution, input_size, **gen_kwargs)
            result = run_collision_experiment(hash_func, table_size, inputs)
            results[(table_size, input_size)] = result
    return results
