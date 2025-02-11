# hash_functions.py
"""
This module defines common hash functions for collision analysis.
It includes:
- A simple modulo-based hash function.
- A polynomial rolling hash function.
- Python's built-in hash() function.
"""

def modulo_hash(value, table_size):
    """
    Simple modulo-based hash function.
    
    Parameters:
        value (int): The input value to hash.
        table_size (int): The size of the hash table.
        
    Returns:
        int: Hash value computed as value % table_size.
    """
    if isinstance(value, int):
        return value % table_size
    else:
        # Fallback: use Python's built-in hash if value is not an integer.
        return hash(value) % table_size

def polynomial_hash(value, table_size, base=31):
    """
    Polynomial rolling hash function.
    
    This function converts the input to a string and computes a hash using a polynomial rolling approach.
    
    Parameters:
        value: The input value to hash (will be converted to string).
        table_size (int): The size of the hash table.
        base (int): The base used in the polynomial rolling hash (default is 31).
        
    Returns:
        int: The computed hash value.
    """
    s = str(value)
    h = 0
    for ch in s:
        h = (h * base + ord(ch)) % table_size
    return h

def built_in_hash(value, table_size):
    """
    Hash function using Python's built-in hash() function.
    
    Parameters:
        value: The input value to hash.
        table_size (int): The size of the hash table.
        
    Returns:
        int: The computed hash value.
    """
    return hash(value) % table_size

# Dictionary of available hash functions for future extensibility.
HASH_FUNCTIONS = {
    'modulo': modulo_hash,
    'polynomial': polynomial_hash,
    'built_in': built_in_hash
}
