class Partition():
    """
    Represents a memory partition in a memory management system.
    Used for fixed partition memory allocation schemes.
    """
    
    def __init__(self, partition_id, memory_space):
        """
        Initialize a memory partition.
        
        Args:
            partition_id: Unique identifier for this partition
            memory_space: Total size/capacity of this partition in memory units
        """
        self.partition_id = partition_id  # Unique ID to identify this partition
        self.memory_space = memory_space  # Total memory capacity of this partition
        self.occupied = False  # Flag indicating if partition is currently in use
        self.current_job = None  # Reference to the job currently occupying this partition (None if empty)

class Job():
    """
    Represents a job/process that needs to be allocated to memory.
    Tracks the job's memory requirements and current status.
    """
    
    def __init__(self, job_id, memory_needed):
        """
        Initialize a job with its memory requirements.
        
        Args:
            job_id: Unique identifier for this job
            memory_needed: Amount of memory required by this job
        """
        self.job_id = job_id  # Unique ID to identify this job
        self.memory_needed = memory_needed  # Memory size required by this job
        self.status = "waiting"  # Current status of the job (e.g., "waiting", "allocated", "finished")