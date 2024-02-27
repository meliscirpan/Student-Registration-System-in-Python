from registration_system import RegistrationSystem
import logging
import sys


def init_logger():
    """Initializes logger for logging purposes"""
    
    a_logger = logging.getLogger()
    output_file_handler = logging.FileHandler("Registration Process&Stats.log")
    stdout_handler = logging.StreamHandler(sys.stdout)
    a_logger.addHandler(output_file_handler)
    a_logger.addHandler(stdout_handler)


init_logger()

sys = RegistrationSystem()
sys.start_simulation()






