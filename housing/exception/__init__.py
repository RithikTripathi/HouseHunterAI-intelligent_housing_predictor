import os
import sys # sys module is helpful to find which line / which file is causing error

# inheriting Exception super class in our custom class
class Housing_Exception(Exception):
    
    # error_message:Exception : this means that error_message is basically of type exception and is an object of Exception
    def __init__(self, error_message:Exception,error_detail:sys):
        # below super method is equivalent to Exception(error_message)
        # i.e passing error message to the Exception class
        super().__init__(error_message)
        self.error_message=Housing_Exception.get_detailed_error_message(error_message=error_message,
                                                                       error_detail=error_detail
                                                                        )

    # making this fun() static so that we dont need to initialize an object repeatively and can directly access with help of class
    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_detail:sys)->str:
        """
        Returns the caught error message.
        ---
        error_message: Exception object
        error_detail: object of sys module
        """

        # exc.info() returns info about most recent exception caught by except block
        # it returns a tuple of type, value and traceback
        _,_ ,exec_tb = error_detail.exc_info()
        # as we do not require the type and value, we used _ to catch it and ignore

        # traceback : which file and line is causing error
        exception_block_line_number = exec_tb.tb_frame.f_lineno
        try_block_line_number = exec_tb.tb_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename
        error_message = f"""
        Error occured in script: 
        [ {file_name} ] at 
        try block line number: [{try_block_line_number}] and exception block line number: [{exception_block_line_number}] 
        error message: [{error_message}]
        """
        return error_message

    # whenever we try to print any object, what info. should be displayed, that we can define in str()
    # it is a dunder method
    def __str__(self):
        return self.error_message

    # returns a printable representation of the given object.
    def __repr__(self) -> str:
        return Housing_Exception.__name__.str()

     # in short : how a object should be visible with print() => __Str__ and without print() => __repr__