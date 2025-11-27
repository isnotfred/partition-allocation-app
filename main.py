# Import required system and custom modules
import sys
from partition.memory_classes import Partition, Job
from partition.algorithms import first_fit, best_fit, worst_fit, next_fit, deallocate
# Import PyQt5 GUI components
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QLineEdit, QPushButton, QLabel, QHeaderView, QComboBox, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    """
    Main application window for the Partition Allocation Simulator.
    Provides a GUI for managing memory partitions and job allocations using various algorithms.
    """
    
    def __init__(self):
        """
        Initialize the main window with UI components and data structures.
        Sets up three main sections: Jobs, Partitions, and Operations.
        """
        super().__init__()
        # Initialize data structures
        self.jobs = []  # List of all jobs (waiting, allocated, finished)
        self.partitions = []  # List of all memory partitions
        self.job_id = 0  # Counter for generating unique job IDs
        self.partition_id = 0  # Counter for generating unique partition IDs
        self.next_fit_last_index = 0  # Tracks last allocation position for Next Fit algorithm

        # Set window background color
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QWidget {
                background-color: #f5f5f5;
            }
        """)

        # Initialize layout containers for three main sections
        jobs_section = QVBoxLayout()
        partitions_section = QVBoxLayout()

        # ==================== STYLING DEFINITIONS ====================
        
        # Style for input text fields (memory needed, memory space)
        input_field_style = """
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 10px 14px;
                background-color: white;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:hover {
                border: 2px solid #bbb;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
                background-color: #fafafa;
            }
        """

        # Style for add buttons (Add Job, Add Partition)
        input_btn_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                padding: 14px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """

        # Style for table widgets (Jobs and Partitions tables)
        table_style = """
            QTableWidget {
                border: 2px solid #ddd;
                border-radius: 8px;
                background-color: white;
                gridline-color: #e8e8e8;
                selection-background-color: #e3f2fd;
            }
            QTableWidget::item {
                padding: 8px;
                color: #333;
            }
            QTableWidget::item:selected {
                background-color: #bbdefb;
                color: #000;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 13px;
                border-right: 1px solid #45a049;
            }
            QHeaderView::section:last {
                border-right: none;
            }
        """

        # Style for regular labels
        label_style = """
            QLabel {
                color: #333;
                font-weight: bold;
                font-size: 16px;
                padding: 5px 0;
            }
        """

        # Style for section header labels
        section_label_style = """
            QLabel {
                color: #2c3e50;
                font-weight: bold;
                font-size: 20px;
                padding: 8px 0;
                border-bottom: 3px solid #4CAF50;
                margin-bottom: 10px;
            }
        """

        # ==================== JOBS SECTION ====================
        
        # Create Jobs section header
        jobs_section_label = QLabel("📋 Jobs")
        jobs_section_label.setStyleSheet(section_label_style)
        
        # Input field for entering job memory requirements
        self.memory_needed_field = QLineEdit()
        self.memory_needed_field.setPlaceholderText("Enter memory needed (KB)")
        self.memory_needed_field.setStyleSheet(input_field_style)

        # Button to add new job
        add_job_btn = QPushButton("Add Job")
        add_job_btn.clicked.connect(self.add_job)
        add_job_btn.setStyleSheet(input_btn_style)
        add_job_btn.setMinimumWidth(120)

        # Layout for job input field and button
        job_input_layout = QHBoxLayout()
        job_input_layout.addWidget(self.memory_needed_field, 3)  # 3/4 of the width
        job_input_layout.addWidget(add_job_btn, 1)  # 1/4 of the width
        job_input_layout.setSpacing(10)

        # Table to display all jobs and their statuses
        self.jobs_table_widget = QTableWidget()
        self.jobs_table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # Read-only
        self.jobs_table_widget.setColumnCount(3)
        self.jobs_table_widget.setHorizontalHeaderLabels(["Job ID", "Memory Needed", "Status"])
        self.jobs_table_widget.horizontalHeader().setStretchLastSection(True)
        self.jobs_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.jobs_table_widget.setStyleSheet(table_style)
        self.jobs_table_widget.setAlternatingRowColors(True)  # Zebra striping for readability
        self.jobs_table_widget.setStyleSheet(table_style + """
            QTableWidget {
                alternate-background-color: #f9f9f9;
            }
        """)

        # Assemble Jobs section
        jobs_section.addWidget(jobs_section_label)
        jobs_section.addLayout(job_input_layout)
        jobs_section.addWidget(self.jobs_table_widget)
        jobs_section.setSpacing(12)
        
        # ==================== PARTITIONS SECTION ====================
        
        # Create Partitions section header
        partitions_section_label = QLabel("💾 Partitions")
        partitions_section_label.setStyleSheet(section_label_style)

        # Input field for entering partition memory size
        self.memory_space_field = QLineEdit()
        self.memory_space_field.setPlaceholderText("Enter memory space (KB)")
        self.memory_space_field.setStyleSheet(input_field_style)

        # Button to add new partition
        add_partition_btn = QPushButton("Add Partition")
        add_partition_btn.clicked.connect(self.add_partition)
        add_partition_btn.setStyleSheet(input_btn_style)
        add_partition_btn.setMinimumWidth(140)

        # Layout for partition input field and button
        partition_input_layout = QHBoxLayout()
        partition_input_layout.addWidget(self.memory_space_field, 3)  # 3/4 of the width
        partition_input_layout.addWidget(add_partition_btn, 1)  # 1/4 of the width
        partition_input_layout.setSpacing(10)

        # Table to display all partitions and their allocations
        self.partitions_table_widget = QTableWidget()
        self.partitions_table_widget.setAlternatingRowColors(True)  # Zebra striping
        self.partitions_table_widget.setStyleSheet(table_style + """
            QTableWidget {
                alternate-background-color: #f9f9f9;
            }
        """)

        # Assemble Partitions section
        partitions_section.addWidget(partitions_section_label)
        partitions_section.addLayout(partition_input_layout)
        partitions_section.addWidget(self.partitions_table_widget)
        partitions_section.setSpacing(12)

        # ==================== OPERATIONS SECTION ====================
        
        # Create Operations section header
        operations_section_label = QLabel("⚙️ Operations")
        operations_section_label.setStyleSheet(section_label_style)
        
        # Label for algorithm selection
        allocate_label = QLabel("Algorithm:")
        allocate_label.setStyleSheet(label_style)

        # Style for combo boxes (dropdowns)
        combo_style = """
            QComboBox {
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 8px 12px;
                background-color: white;
                font-size: 14px;
                color: #333;
            }
            QComboBox:hover {
                border: 2px solid #bbb;
            }
            QComboBox:focus {
                border: 2px solid #2196F3;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #ddd;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #2196F3;
                selection-color: white;
                padding: 5px;
            }
        """

        # Dropdown to select allocation algorithm
        self.algorithms_cmb = QComboBox()
        self.algorithms_cmb.addItem("First Fit")
        self.algorithms_cmb.addItem("Best Fit")
        self.algorithms_cmb.addItem("Worst Fit")
        self.algorithms_cmb.addItem("Next Fit")
        self.algorithms_cmb.setStyleSheet(combo_style)

        # Button to execute allocation using selected algorithm
        allocate_btn = QPushButton("ALLOCATE")
        allocate_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        allocate_btn.clicked.connect(self.allocate_job)
        allocate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2196F3, stop:1 #1976D2);
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 20px;
            }
            QPushButton:hover {
                background: #2196F3;
            }
            QPushButton:pressed {
                background: #1565C0;
            }
        """)

        # Label for deallocation section
        deallocate_label = QLabel("Deallocate Job:")
        deallocate_label.setStyleSheet(label_style)
        
        # Dropdown to select allocated job for deallocation
        self.allocated_jobs_cmb = QComboBox()
        self.allocated_jobs_cmb.setStyleSheet(combo_style)
        
        # Button to deallocate selected job
        deallocate_btn = QPushButton("DEALLOCATE")
        deallocate_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
        deallocate_btn.clicked.connect(self.deallocate_job)
        deallocate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FF9800, stop:1 #F57C00);
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 20px;
            }
            QPushButton:hover {
                background: #FF9800;
            }
            QPushButton:pressed {
                background: #E65100;
            }
        """)

        # Button to reset entire application state
        reset_btn = QPushButton("RESET")
        reset_btn.clicked.connect(self.reset)
        reset_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F44336, stop:1 #D32F2F);
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                padding: 20px;
            }
            QPushButton:hover {
                background: #F44336;
            }
            QPushButton:pressed {
                background: #B71C1C;
            }
        """)

        # Assemble Operations section
        operations_section = QVBoxLayout()
        operations_section.addWidget(operations_section_label)
        operations_section.addWidget(allocate_label)
        operations_section.addWidget(self.algorithms_cmb)
        operations_section.addWidget(allocate_btn)
        operations_section.addWidget(deallocate_label)
        operations_section.addWidget(self.allocated_jobs_cmb)
        operations_section.addWidget(deallocate_btn)
        operations_section.addWidget(reset_btn)

        # ==================== MAIN LAYOUT ASSEMBLY ====================
        
        # Combine all three sections horizontally with specific width ratios
        main_layout = QHBoxLayout()
        main_layout.addLayout(jobs_section, 6)  # 40% width
        main_layout.addLayout(partitions_section, 6)  # 40% width
        main_layout.addLayout(operations_section, 3)  # 20% width
        main_layout.setContentsMargins(20, 20, 20, 20)  # Add padding around window

        # Set main layout as central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.resize(1400, 700)  # Set initial window size
        self.setMinimumSize(1200, 500)
        self.setWindowTitle("Partition Allocation Simulator")

    def add_job(self):
        """
        Add a new job to the system.
        Validates input, creates Job object, and updates the jobs table.
        """
        try:
            # Parse and validate memory requirement input
            memory_needed = int(self.memory_needed_field.text().strip())
            if memory_needed <= 0:
                raise ValueError
        except ValueError:
            # Clear field if invalid input
            self.memory_needed_field.clear()
            return
        
        # Generate new job ID and add row to table
        self.job_id += 1
        row_position = self.jobs_table_widget.rowCount()
        self.jobs_table_widget.insertRow(row_position)
        
        # Create table items with centered alignment
        job_id_item = QTableWidgetItem(f"J{self.job_id}")
        job_id_item.setTextAlignment(Qt.AlignCenter)
        memory_item = QTableWidgetItem(f"{memory_needed} KB")
        memory_item.setTextAlignment(Qt.AlignCenter)
        status_item = QTableWidgetItem("Waiting")
        status_item.setTextAlignment(Qt.AlignCenter)
        
        # Populate table row
        self.jobs_table_widget.setItem(row_position, 0, job_id_item)
        self.jobs_table_widget.setItem(row_position, 1, memory_item)
        self.jobs_table_widget.setItem(row_position, 2, status_item)
        
        # Create Job object and add to jobs list
        self.jobs.append(Job(self.job_id, memory_needed))

        # Clear input field for next entry
        self.memory_needed_field.clear()

    def add_partition(self):
        """
        Add a new memory partition to the system.
        Validates input, creates Partition object, and updates the partitions table.
        """
        try:
            # Parse and validate memory space input
            memory_space = int(self.memory_space_field.text().strip())
            if memory_space <= 0:
                raise ValueError
        except ValueError:
            # Clear field if invalid input
            self.memory_space_field.clear()
            return
        
        # Generate new partition ID and create Partition object
        self.partition_id += 1
        self.partitions.append(Partition(self.partition_id, memory_space))
        
        # Update partitions table to reflect new partition
        self.update_partitions_table()
        
        # Clear input field for next entry
        self.memory_space_field.clear()

    def allocate_job(self):
        """
        Allocate waiting jobs to partitions using the selected algorithm.
        Updates all relevant UI components after allocation.
        """
        # Check if there are any jobs to allocate
        if not self.jobs:
            return
        
        # Get selected algorithm and filter jobs by status
        algorithm = self.algorithms_cmb.currentText()
        waiting_jobs = [job for job in self.jobs if job.status == "waiting"]
        allocated_jobs = [job for job in self.jobs if job.status == "allocated"]
        
        # Exit if no waiting jobs
        if not waiting_jobs:
            return
        
        # Execute appropriate allocation algorithm
        if algorithm == "First Fit":
            first_fit(self.partitions, waiting_jobs, allocated_jobs)
        elif algorithm == "Best Fit":
            best_fit(self.partitions, waiting_jobs, allocated_jobs)
        elif algorithm == "Worst Fit":
            worst_fit(self.partitions, waiting_jobs, allocated_jobs)
        elif algorithm == "Next Fit":
            # Next Fit requires tracking last allocation position
            self.next_fit_last_index = next_fit(self.partitions, waiting_jobs, allocated_jobs, self.next_fit_last_index)
        
        # Update UI to reflect allocation changes
        self.update_partitions_table()
        self.update_allocated_jobs_combo()
        self.update_jobs_status()

    def update_partitions_table(self):
        """
        Refresh the partitions table to show current allocation state.
        Displays partition ID, size, and any allocated job.
        """
        # Set table structure
        self.partitions_table_widget.setColumnCount(2)
        self.partitions_table_widget.setHorizontalHeaderLabels(["Partition", "Allocated Job"])
        self.partitions_table_widget.setRowCount(len(self.partitions))
        self.partitions_table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # Read-only
        self.partitions_table_widget.horizontalHeader().setStretchLastSection(True)
        self.partitions_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Populate each row with partition information
        for i, partition in enumerate(self.partitions):
            # Display partition ID and size
            partition_text = f"F{partition.partition_id} ({partition.memory_space} KB)"
            partition_item = QTableWidgetItem(partition_text)
            partition_item.setTextAlignment(Qt.AlignCenter)
            self.partitions_table_widget.setItem(i, 0, partition_item)
            
            # Display allocated job if partition is occupied
            if partition.occupied and partition.current_job:
                job_text = f"J{partition.current_job.job_id} ({partition.current_job.memory_needed} KB)"
                job_item = QTableWidgetItem(job_text)
                job_item.setTextAlignment(Qt.AlignCenter)
                self.partitions_table_widget.setItem(i, 1, job_item)
            else:
                # Leave cell empty if partition is free
                empty_item = QTableWidgetItem("")
                self.partitions_table_widget.setItem(i, 1, empty_item)

    def update_allocated_jobs_combo(self):
        """
        Refresh the allocated jobs dropdown with currently allocated jobs.
        Used for selecting which job to deallocate.
        """
        self.allocated_jobs_cmb.clear()
        # Add each allocated job to dropdown with job reference as data
        for job in self.jobs:
            if job.status == "allocated":
                self.allocated_jobs_cmb.addItem(f"J{job.job_id} ({job.memory_needed} KB)", job)

    def update_jobs_status(self):
        """
        Refresh the status column in the jobs table to reflect current job states.
        Updates status for all jobs (waiting, allocated, finished).
        """
        # Iterate through each row in jobs table
        for row in range(self.jobs_table_widget.rowCount()):
            # Extract job ID from table cell
            job_id_text = self.jobs_table_widget.item(row, 0).text()
            job_id = int(job_id_text[1:])  # Remove "J" prefix and convert to int
            
            # Find corresponding job object and update status
            for job in self.jobs:
                if job.job_id == job_id:
                    status_text = job.status.capitalize()
                    status_item = QTableWidgetItem(status_text)
                    status_item.setTextAlignment(Qt.AlignCenter)
                    self.jobs_table_widget.setItem(row, 2, status_item)
                    break

    def deallocate_job(self):
        """
        Deallocate the selected job from its partition.
        Frees the partition and marks job as finished.
        """
        # Check if there are any allocated jobs to deallocate
        if self.allocated_jobs_cmb.count() == 0:
            return
        
        # Get selected job from dropdown
        job_to_remove = self.allocated_jobs_cmb.currentData()
        
        if job_to_remove:
            # Filter jobs by current status
            allocated_jobs = [job for job in self.jobs if job.status == "allocated"]
            finished_jobs = [job for job in self.jobs if job.status == "finished"]
            
            # Execute deallocation
            deallocate(self.partitions, allocated_jobs, finished_jobs, job_to_remove)
            
            # Update UI to reflect deallocation
            self.update_partitions_table()
            self.update_allocated_jobs_combo()
            self.update_jobs_status()

    def reset(self):
        """
        Reset the entire application to initial state.
        Clears all jobs, partitions, and resets all counters.
        """
        # Clear all data structures
        self.jobs.clear()
        self.partitions.clear()
        self.next_fit_last_index = 0
        self.job_id = 0
        self.partition_id = 0
        
        # Clear all table displays
        self.jobs_table_widget.setRowCount(0)
        self.partitions_table_widget.setRowCount(0)
        self.partitions_table_widget.setColumnCount(0)
        
        # Clear allocated jobs dropdown
        self.allocated_jobs_cmb.clear()

def main():
    """
    Main entry point for the application.
    Initializes Qt application and displays the main window.
    """
    # Create Qt application instance
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Create and display main window
    window = MainWindow()
    window.show()
    
    # Start event loop and exit when closed
    sys.exit(app.exec_())

# Run application if this file is executed directly
if __name__ == '__main__':
    main()