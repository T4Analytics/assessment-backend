import os
import sys
import random
import string
from datetime import datetime
from typing import Any, Union
import logging
import psycopg2
import psycopg2.extras
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from modules.constants import Constants

c = Constants()


class Helpers:
	_db: None
	
	# this attribute and method make this a singleton
	_instance = None
	
	def __new__(cls, *args, **kwargs):
		if not isinstance(cls._instance, cls):
			cls._instance = object.__new__(cls, *args, **kwargs)
		return cls._instance
	
	def __init__(self):
		self._db = psycopg2.connect(
			host=self.env("db_server", "localhost"),
			database=self.env("db_name", "assessment"),
			user=self.env("db_user", "t4"),
			password=self.env("db_password", "t4")
		)
		self._cursor = self._db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		logging.basicConfig(
			filename="/tmp/t4-assessment-debug.log",
			level=logging.DEBUG,
			format='%(asctime)s %(levelname)-8s %(message)s',
			datefmt='%Y-%m-%d %H:%M:%S'
		)
	
	@staticmethod
	def field2tuple(rows, fieldname="id"):
		lst = [row[fieldname] for row in rows]
		return tuple(lst)
	
	@staticmethod
	def field2key(rows, fieldname="id"):
		lst = {row[fieldname]: row for row in rows}
		return lst
	
	def randstr(self, length: int = 8):
		letters = string.ascii_lowercase + string.digits
		randy = ''.join(random.choice(letters) for i in range(length))
		self.log(["randy", randy])
		return randy
	
	@staticmethod
	def now():
		dt = datetime.now()
		return dt.strftime('%Y-%m-%d %H:%M:%S')
	
	@staticmethod
	def log(*args, **kwargs):
		if kwargs:
			logging.info(kwargs)
		if args:
			for arg in args:
				logging.info(arg)
	
	def db_select(self, tablename, conds={}, order="id"):
		# SELECT * FROM {tablename} WHERE a=b AND c>=d
		qstr = f"SELECT * FROM {tablename} "
		if conds:
			qstr += "WHERE "
			for key in conds:
				if key[-4:] == "__ne":
					qstr += f"{key[:-4]} != %({key})s AND "
				elif key[-4:] == "__gt":
					qstr += f"{key[:-4]} > %({key})s AND "
				elif key[-4:] == "__in":
					qstr += f"{key[:-4]} in %({key})s AND "
				elif key[-5:] == "__gte":
					qstr += f"{key[:-5]} >= %({key})s AND "
				elif key[-4:] == "__lt":
					qstr += f"{key[:-4]} < %({key})s AND "
				elif key[-5:] == "__lte":
					qstr += f"{key[:-5]} <= %({key})s AND "
				else:
					qstr += f"{key} = %({key})s AND "
			qstr = qstr[:-4] + f" ORDER BY {order} DESC"
			self._cursor.execute(qstr, conds)
		else:
			qstr += f"ORDER BY {order} DESC"
			self._cursor.execute(qstr)
		return self._cursor.fetchall()
	
	def db_insert(self, tablename, data, config=None):
		if config is None:
			config = [c.retids]
		if type(data) != dict:
			data = data.dict()
		if "id" in data:
			del data["id"]
		if "created_at" in data:
			del data["created_at"]
		if "updated_at" in data:
			del data["updated_at"]
		data["created_at"] = Helpers.now()
		data["updated_at"] = Helpers.now()
		qstr = f"INSERT INTO {tablename} ("
		valuestr = ""
		values = []
		for colname, colvalue in data.items():
			qstr += f"{colname}, "
			valuestr += "%s, "
			if type(colvalue) == datetime:
				colvalue = colvalue.strftime('%Y-%m-%d %H:%M:%S')
			values.append(colvalue)
		qstr = qstr[:-2] + ") values (" + valuestr[:-2] + ") RETURNING id"
		try:
			self._cursor.execute(qstr, values)
			if c.retids in config:
				idx = self._cursor.fetchall()[0]["id"]
				self._db.commit()
				return idx
			elif c.retrows in config:
				idx = self._cursor.fetchall()[0]["id"]
				self._db.commit()
				row = self.db_select(tablename, {"id": idx})
				return row
			else:
				return True
		except:
			raise
			print(sys.exc_info())
			return False
	
	def db_delete(self, tablename, id):
		qstr = f"UPDATE {tablename} SET is_deleted=1 WHERE id=%s"
		try:
			self._cursor.execute(qstr, (id,))
			self._db.commit()
			return id
		except:
			print(sys.exc_info())
			return False
	
	def idor404(self, tablename, conds):
		row = self.db_select(tablename, conds)
		if len(row) == 1:
			return row[0]["id"]
		else:
			raise HTTPException(status_code=404, detail=f"Record not found in {tablename}")
	
	def db_createorselect(self, tablename, conds):
		row = self.db_select(tablename, conds)
		if len(row) != 1:
			row = self.db_insert(tablename, conds, [c.retrows])
		return row[0]
	
	def db_selectsingle(self, tablename, conds) -> Union[dict, bool]:
		rows = self.db_select(tablename, conds)
		if len(rows) == 1:
			return rows[0]
		return False
	
	def listing_endpoint(self, tablename, additional_conds={}):
		if "is_deleted" not in additional_conds:
			additional_conds["is_deleted"] = 0
		return self.db_select(tablename, additional_conds)
	
	def adding_endpoint(self, tablename, records, additional_fields={}):
		ids = []
		for record in records:
			newrecord = additional_fields
			newrecord.update(record)
			self.log(newrecord)
			ids.append(self.db_insert(tablename, newrecord, [c.retrows]))
		return ids
	
	def deleting_endpoint(self, tablename, ids):
		for id in ids:
			self.db_delete(tablename, id)
		return ids
	
	def env(self, varname, default_value):
		return os.getenv(varname, default_value)
	
	def err(self, errcode: int, data: Any):
		return JSONResponse(data, status_code=errcode)
