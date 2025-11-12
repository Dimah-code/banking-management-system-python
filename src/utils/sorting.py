"""
Sorting algorithms for the banking system.
"""

def merge_sort(arr, key_index, ascending=True):
    """
    Implements the Merge Sort algorithm, a comparison sort based on the 
    divide-and-conquer paradigm, ensuring O(N log N) time complexity.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    left = merge_sort(left, key_index, ascending)
    right = merge_sort(right, key_index, ascending)

    return merge(left, right, key_index, ascending)


def merge(left, right, key_index, ascending):
    """Merges two sorted lists."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        left_val = left[i][key_index]
        right_val = right[j][key_index]

        # Convert amount to float for correct numeric comparison if required
        if key_index in (2, 3): 
            try:
                left_val = float(left_val)
                right_val = float(right_val)
            except (ValueError, TypeError):
                pass 
        
        if ascending:
            if left_val < right_val:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        else: # Descending
            if left_val > right_val:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result