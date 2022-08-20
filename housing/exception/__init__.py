import os
import sys # sys module is helpful to find which line / which file is causing error

# inheriting Exception super class in out custom class
# error_message:Exception : this means that wrror_message is basically of type exception and is an object of Exception
class Housing_Exception(Exception):
    def __init__(self, error_message:Exception, error_detail:sys):
        # below super method is equivalent to Exception(error_message)
        # i.e passing error message to the Exception class
        super().__init__(error_message) 
        self.error_message = Housing_Exception.get_detailed_error_message(error_message = error_message,
                                                                          error_detail = error_detail  )

        # making this fun() static so that we dont need to initialize an object repeatively and can directly access with help of class
    @staticmethod
    def get_detailed_error_message(error_message:Exception, error_detail:sys) -> str:
        """
        Returns the caught error message.
        ---
        error_message : Exception object
        error_details : object of sys module
        """
        # exc.info() returns info about most recent exception caught by except block
        # it returns a tuple of type, value and traceback
        _,_ ,exec_tb = error_detail.exc_info() 
        # as we do not require the type and value, we used _ to catch it and ignore
        # traceback : which file and line is causing error

        line_number = exec_tb.tb_frame.f_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename
        # customising the Error message 
        error_message = f"Error Occured in Script : [{file_name}] at Line Nummber : [{line_number}] with Error Message : [{error_message}]"

        return error_message

    # whenever we try to print details of any object, what info. should be displayed, that we can define in str()
    # it is a dunder method
    def __str__(self):
        return self.error_message

    
    def __repr__(self) -> str:
        return Housing_Exception.__name__.str()



