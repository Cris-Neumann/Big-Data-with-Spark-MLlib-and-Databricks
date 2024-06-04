# Databricks notebook source
class DataSource:
    """
    Abstract Class
    """

    def __init__(self, path):
        self.path = path
    
    def get_data_frame(self):
        """
        Abstract method, Function will be defined in sub classes
        """

        raise ValueError("Not Implemented")
