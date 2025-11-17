def first_fit(partitions, waiting_jobs, allocated_jobs):
    """
    First Fit Algorithm: Allocates each job to the first available partition that can fit it.
    Scans partitions from the beginning each time.
    
    Args:
        partitions: List of Partition objects available for allocation
        waiting_jobs: List of Job objects waiting to be allocated
        allocated_jobs: List of Job objects that have been successfully allocated
    
    Strategy:
        - Fast allocation (stops at first fit)
        - May create fragmentation at the beginning of memory
    """
    # Try to allocate each waiting job
    for job in waiting_jobs[:]:  # Create a copy to safely modify list during iteration
        # Check and assign if it fits in a free partition
        for partition in partitions:
            # Check if partition is free and large enough for the job
            if not partition.occupied and job.memory_needed <= partition.memory_space:
                partition.current_job = job  # Assign job to partition
                partition.occupied = True  # Mark partition as occupied
                job.status = "allocated"  # Update job status
                waiting_jobs.remove(job)  # Remove from waiting queue
                allocated_jobs.append(job)  # Add to allocated list
                break  # Move to next job after successful allocation

def best_fit(partitions, waiting_jobs, allocated_jobs):
    """
    Best Fit Algorithm: Allocates each job to the partition with the smallest sufficient space.
    Minimizes internal fragmentation (wasted space within a partition).
    
    Args:
        partitions: List of Partition objects available for allocation
        waiting_jobs: List of Job objects waiting to be allocated
        allocated_jobs: List of Job objects that have been successfully allocated
    
    Strategy:
        - Minimizes wasted space per allocation
        - Scans all partitions to find the best fit
        - May leave many small unusable fragments
    """
    # Try to allocate each waiting job
    for job in waiting_jobs[:]:  # Create a copy to safely modify list during iteration
        smallest_internal_fragmentation = float('inf')  # Track minimum waste
        selected_index = -1  # Index of best-fit partition

        # Check if it fits in each partition and find the one with smallest waste
        for i, partition in enumerate(partitions):
            if not partition.occupied and job.memory_needed <= partition.memory_space:
                # Compute internal fragmentation (wasted space in this partition)
                internal_fragmentation = partition.memory_space - job.memory_needed
                # Update if this partition has less waste than previous candidates
                if internal_fragmentation < smallest_internal_fragmentation:
                    smallest_internal_fragmentation = internal_fragmentation
                    selected_index = i

        # Assign job if a suitable partition was found
        if selected_index != -1:
            partitions[selected_index].current_job = job  # Assign job to best partition
            partitions[selected_index].occupied = True  # Mark partition as occupied
            job.status = "allocated"  # Update job status
            waiting_jobs.remove(job)  # Remove from waiting queue
            allocated_jobs.append(job)  # Add to allocated list
        # Else job remains waiting (no suitable partition found)

def worst_fit(partitions, waiting_jobs, allocated_jobs):
    """
    Worst Fit Algorithm: Allocates each job to the partition with the largest sufficient space.
    Maximizes remaining space in partitions to accommodate future jobs.
    
    Args:
        partitions: List of Partition objects available for allocation
        waiting_jobs: List of Job objects waiting to be allocated
        allocated_jobs: List of Job objects that have been successfully allocated
    
    Strategy:
        - Leaves larger fragments that may be useful for future allocations
        - May lead to more external fragmentation overall
        - Scans all partitions to find the worst fit
    """
    # Try to allocate each waiting job
    for job in waiting_jobs[:]:  # Create a copy to safely modify list during iteration
        largest_internal_fragmentation = -1  # Track maximum remaining space
        selected_index = -1  # Index of worst-fit partition

        # Check if it fits in each partition and find the one with most remaining space
        for i, partition in enumerate(partitions):
            if not partition.occupied and job.memory_needed <= partition.memory_space:
                # Compute internal fragmentation (remaining space in this partition)
                internal_fragmentation = partition.memory_space - job.memory_needed
                # Update if this partition has more remaining space than previous candidates
                if internal_fragmentation > largest_internal_fragmentation:
                    largest_internal_fragmentation = internal_fragmentation
                    selected_index = i

        # Assign job if a suitable partition was found
        if selected_index != -1:
            partitions[selected_index].current_job = job  # Assign job to worst-fit partition
            partitions[selected_index].occupied = True  # Mark partition as occupied
            job.status = "allocated"  # Update job status
            waiting_jobs.remove(job)  # Remove from waiting queue
            allocated_jobs.append(job)  # Add to allocated list
        # Else job remains waiting (no suitable partition found)

def next_fit(partitions, waiting_jobs, allocated_jobs, last_index=0):
    """
    Next Fit Algorithm: Similar to First Fit, but continues searching from where it last left off.
    Avoids repeatedly scanning the same partitions at the beginning of memory.
    
    Args:
        partitions: List of Partition objects available for allocation
        waiting_jobs: List of Job objects waiting to be allocated
        allocated_jobs: List of Job objects that have been successfully allocated
        last_index: Index of the last allocated partition (default: 0)
    
    Returns:
        int: Updated last_index for the next allocation cycle
    
    Strategy:
        - Distributes allocations more evenly across memory
        - Faster than First Fit for repeated allocations
        - Uses circular search starting after last allocation point
    """
    n = len(partitions)  # Total number of partitions

    # Try to allocate each waiting job  
    for job in waiting_jobs[:]:  # Create a copy to safely modify list during iteration

        # Check and assign if it fits in a free partition, starting after last_index
        for i in range(n):  # Check all partitions in circular order
            idx = (last_index + 1 + i) % n  # Calculate circular index (wraps around)
            partition = partitions[idx]
            # Check if partition is free and large enough for the job
            if not partition.occupied and job.memory_needed <= partition.memory_space:
                partition.current_job = job  # Assign job to partition
                partition.occupied = True  # Mark partition as occupied
                job.status = "allocated"  # Update job status
                waiting_jobs.remove(job)  # Remove from waiting queue
                allocated_jobs.append(job)  # Add to allocated list
                last_index = idx  # Remember this position for next allocation
                break  # Move to next job after successful allocation

    return last_index  # Return updated index for future calls

def deallocate(partitions, allocated_jobs, finished_jobs, job_to_remove):
    """
    Deallocates a job from memory, freeing up its partition for future allocations.
    
    Args:
        partitions: List of Partition objects
        allocated_jobs: List of currently allocated Job objects
        finished_jobs: List of Job objects that have completed
        job_to_remove: The Job object to deallocate
    
    Process:
        1. Find the partition containing the job
        2. Free the partition
        3. Update job lists and status
    """
    # Find the partition containing this job
    for partition in partitions:
        if partition.current_job == job_to_remove:
            partition.current_job = None  # Remove job reference
            partition.occupied = False  # Mark partition as free
            break  # Stop searching once found
    
    # Update job lists
    allocated_jobs.remove(job_to_remove)  # Remove from allocated list
    finished_jobs.append(job_to_remove)  # Add to finished list
    job_to_remove.status = "finished"  # Update job status