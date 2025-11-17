def first_fit(partitions, waiting_jobs, allocated_jobs):
    # try to allocate each waiting job
    for job in waiting_jobs[:]:
        # check and assign if it fits in a free partition
        for partition in partitions:
            if not partition.occupied and job.memory_needed <= partition.memory_space:
                partition.current_job = job
                partition.occupied = True
                job.status = "allocated"
                waiting_jobs.remove(job)
                allocated_jobs.append(job)
                break

def best_fit(partitions, waiting_jobs, allocated_jobs):
    # try to allocate each waiting job
    for job in waiting_jobs[:]:
        smallest_internal_fragmentation = float('inf')
        selected_index = -1

        # check if it fits in each partition
        for i, partition in enumerate(partitions):
            if not partition.occupied and job.memory_needed <= partition.memory_space:
                # compute for its internal fragmentation
                internal_fragmentation = partition.memory_space - job.memory_needed
                if internal_fragmentation < smallest_internal_fragmentation:
                    smallest_internal_fragmentation = internal_fragmentation
                    selected_index = i

        # assign job if a suitable partition was found
        if selected_index != -1:
            partitions[selected_index].current_job = job
            partitions[selected_index].occupied = True
            job.status = "allocated"
            waiting_jobs.remove(job)
            allocated_jobs.append(job)       
        # else job remains waiting

def worst_fit(partitions, waiting_jobs, allocated_jobs):
    # try to allocate each waiting job
    for job in waiting_jobs[:]:
        largest_internal_fragmentation = -1
        selected_index = -1

        # check if it fits in each partition
        for i, partition in enumerate(partitions):
            if not partition.occupied and job.memory_needed <= partition.memory_space:
                # compute for its internal fragmentation
                internal_fragmentation = partition.memory_space - job.memory_needed
                if internal_fragmentation > largest_internal_fragmentation:
                    largest_internal_fragmentation = internal_fragmentation
                    selected_index = i

        # assign job if a suitable partition was found
        if selected_index != -1:
            partitions[selected_index].current_job = job
            partitions[selected_index].occupied = True
            job.status = "allocated"
            waiting_jobs.remove(job)
            allocated_jobs.append(job)
        # else job remains waiting

def next_fit(partitions, waiting_jobs, allocated_jobs, last_index=0):
    n = len(partitions)

    # try to allocate each waiting job  
    for job in waiting_jobs[:]:

        # check and assign if it fits in a free partition
        for i in range(n):
            idx = (last_index + 1 + i) % n  # Start AFTER last_index
            partition = partitions[idx]
            if not partition.occupied and job.memory_needed <= partition.memory_space:
                partition.current_job = job
                partition.occupied = True
                job.status = "allocated"
                waiting_jobs.remove(job)
                allocated_jobs.append(job)
                last_index = idx  # remember this position for next time
                break # move to next job

    return last_index

def deallocate(partitions, allocated_jobs, finished_jobs, job_to_remove):
    # Find the partition containing this job
    for partition in partitions:
        if partition.current_job == job_to_remove:
            partition.current_job = None
            partition.occupied = False
            break
    # Update lists
    allocated_jobs.remove(job_to_remove)
    finished_jobs.append(job_to_remove)
    job_to_remove.status = "finished"