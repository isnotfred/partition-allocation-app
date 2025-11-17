class Partition():
    def __init__(self, partition_id, memory_space):
        self.partition_id = partition_id
        self.memory_space = memory_space
        self.occupied = False
        self.current_job = None

class Job():
    def __init__(self, job_id, memory_needed):
        self.job_id = job_id
        self.memory_needed = memory_needed
        self.status = "waiting"