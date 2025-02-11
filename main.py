# main.py
"""
Entry point for the Hash Collision Simulation and Analysis project.

This script allows the user to select hash functions, hash table sizes, input sizes, and input distributions.
It then runs collision experiments and visualizes the results.
"""

import argparse
import sys

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Hash Collision Simulation and Analysis")
    parser.add_argument("--hash_function", type=str, default="built_in",
                        choices=["modulo", "polynomial", "built_in"],
                        help="Choose the hash function to use.")
    parser.add_argument("--table_sizes", type=str, default="10,100,1000,10000",
                        help="Comma-separated list of hash table sizes (e.g., 10,100,1000,10000).")
    parser.add_argument("--input_sizes", type=str, default="100,1000,10000,100000",
                        help="Comma-separated list of input sizes (e.g., 100,1000,10000,100000).")
    parser.add_argument("--distribution", type=str, default="random_integers",
                        choices=["random_integers", "random_strings", "structured"],
                        help="Type of input distribution.")
    parser.add_argument("--string_length", type=int, default=10,
                        help="Length of strings if distribution is 'random_strings'.")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed for reproducibility.")
    
    args = parser.parse_args()
    
    # Set random seed if provided
    if args.seed is not None:
        import random
        random.seed(args.seed)
    
    # Parse table_sizes and input_sizes into lists of integers
    try:
        table_sizes = [int(x) for x in args.table_sizes.split(",")]
        input_sizes = [int(x) for x in args.input_sizes.split(",")]
    except ValueError:
        print("Error: table_sizes and input_sizes must be comma-separated integers.")
        sys.exit(1)
    
    # Import selected hash function
    from hash_functions import HASH_FUNCTIONS
    if args.hash_function in HASH_FUNCTIONS:
        hash_func = HASH_FUNCTIONS[args.hash_function]
    else:
        print("Unknown hash function:", args.hash_function)
        sys.exit(1)
    
    # Import collision analysis functions
    from collision_analysis import run_collision_experiment, get_inputs, run_sweep_experiments
    
    # Set up additional parameters for input generation if needed
    gen_kwargs = {}
    if args.distribution == "random_strings":
        gen_kwargs["length"] = args.string_length
    
    # Run sweep experiments over specified table sizes and input sizes
    sweep_results = run_sweep_experiments(hash_func, table_sizes, input_sizes, args.distribution, **gen_kwargs)
    
    # Print summary of results
    for (table_size, input_size), result in sweep_results.items():
        print(f"Hash Function: {args.hash_function}, Table Size: {table_size}, Inputs: {input_size}, "
              f"Collisions: {result['total_collisions']}, "
              f"Collision Probability: {result['collision_probability']:.4f}")
    
    # Import visualization functions
    from visualization import plot_collisions_vs_table_size, plot_collision_probability_vs_input_size, plot_bucket_distribution
    
    # Visualize results:
    # 1. Plot collisions vs. table size for the smallest input size.
    min_input_size = min(input_sizes)
    plot_collisions_vs_table_size(sweep_results, min_input_size, args.hash_function)
    
    # 2. Plot collision probability vs. input size for the smallest table size.
    min_table_size = min(table_sizes)
    plot_collision_probability_vs_input_size(sweep_results, min_table_size, args.hash_function)
    
    # 3. Plot bucket distribution for one experiment (e.g., smallest table size and input size).
    experiment = sweep_results[(min_table_size, min_input_size)]
    title = f'Bucket Distribution (Table Size: {min_table_size}, Inputs: {min_input_size}, Function: {args.hash_function})'
    plot_bucket_distribution(experiment["bucket_counts"], title)

if __name__ == "__main__":
    main()
