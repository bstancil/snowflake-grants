#!/usr/bin/env python

import os
import utils
import logging
import snowflake.connector

from snowflake.connector import DictCursor

class Query(object):
	
	def __init__(self):
		creds          = utils.read_yml('config.yaml')
		self.account   = creds['account']
		self.username  = creds['username']
		self.password  = creds['password']
		warehouse      = creds['warehouse']
		
		# Sets log location
		logging.basicConfig(
    		filename='/tmp/snowflake_python_connector.log',
    		level=logging.INFO)
		
		print(">>> Establishing connection.")
		print(">>> Wating for 2FA...")
		self.conn = snowflake.connector.connect(
			user=self.username,
  			password=self.password,
  			account=self.account,
		)
		print(">>> Connection successful.")
		
		self.conn.cursor().execute("USE WAREHOUSE %s;" % warehouse)
	
	def run(self,**kwargs):
		stmt = kwargs['query']
		return_result = kwargs['return_result']
		
		cur = self.conn.cursor(DictCursor)
		stmts = stmt.split(";")
		
		for s in stmts:
			try:
				cur.execute(s)
				
				if return_result:
					results =  []
					for row in cur:
						results.append(row)
						
					return results
			
			except snowflake.connector.errors.ProgrammingError as e:
				print('Error {0} ({1}): {2} ({3})'.format(e.errno, e.sqlstate, e.msg, e.sfqid))
	
	def close(self):
		print(">>> Closing connection.")
		cur = self.conn.cursor(DictCursor)
		cur.close()	