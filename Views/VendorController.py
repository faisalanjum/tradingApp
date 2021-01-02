"""
|--------------------------------------------------------------------------------------------|
|                                                                                            |
|                                                                                            |
|        THIS CLASS iMPLEMENTS THE CRUD OPERATION AND BUSINESS LOGIC ON THE VENDOR TABLE     | 
|                                                                                            |
|                                                                                            |
|--------------------------------------------------------------------------------------------|

"""

# imports
import sys,os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import config 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from Model.app_db import Vendor
class VendorController:
	def __init__(self):

		self.url=config.DB_URL
		self.Session=sessionmaker()


	def addVendor(self,vendor_info):
		
		engine=create_engine(self.url)
		self.Session.configure(bind=engine)
		session=self.Session()
		try:
			session.bulk_insert_mappings(Vendor,vendor_info)

		except Exception as e:
			session.rollback()
			raise e
		finally:
			session.commit()



		

		


		


	







   
obj=VendorController()

dct=list()
dct.append({
	"name":"Alpaca",
	"vendor_id":"PKI36ROS1FUJVRPI1UK7",}
)	

obj.addVendor(vendor_info=dct)

