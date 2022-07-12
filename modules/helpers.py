import json
import os
import random
import string
import time
from datetime import datetime
from typing import Any, Union, Dict
import logging
import psycopg2
import psycopg2.extras
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import Response

from models.question import DetailedQuestion
from modules.constants import Constants
from modules.enums import SessionState

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
	def nowts():
		return time.time()
	
	@staticmethod
	def log(*args, **kwargs):
		if kwargs:
			logging.info(kwargs)
		if args:
			for arg in args:
				logging.info(arg)
	
	def db_createorselect(self, tablename, conds):
		row = self.db_select(tablename, conds)
		if len(row) != 1:
			row = self.db_insert(tablename, conds, [c.retrows])
		return row[0]
	
	def db_selectsingle(self, tablename, conds) -> Union[dict, bool]:
		rows = self.db_select(tablename, conds)
		if len(rows) == 1:
			return {**rows[0]}
		return False
	
	def db_select(self, tablename, conds: Dict[str, Any] = Dict, order="id"):
		# SELECT * FROM {tablename} WHERE a=b AND c>=d
		qstr = f"SELECT * FROM {tablename} "
		if conds:
			qstr += "WHERE "
			for key in conds.keys():
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
			config = [c.retrows]
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
				return self.db_selectsingle(tablename, {"id": idx})
			else:
				return True
		except:
			raise
			# print(sys.exc_info())
			# return False
	
	def db_update(self, tablename, where, data):
		rows = self.db_select(tablename, {**where})
		if len(rows) >= 1:
			ids = self.field2tuple(rows, "id")
			where = {"id__in": ids}
		else:
			return False
		if type(data) != dict:
			data = data.dict()
		if "id" in data:
			del data["id"]
		if "updated_at" in data:
			del data["updated_at"]
		data["updated_at"] = datetime.now()
		qstr = f"UPDATE {tablename} SET "
		for colname in data.keys():
			qstr += f"{colname}=%({colname})s, "
			if type(data[colname]) == datetime:
				data[colname] = data[colname].strftime('%Y-%m-%d %H:%M:%S')
		qstr = qstr[:-2] + " WHERE id in %(id)s RETURNING id"
		data["id"] = ids
		try:
			self._cursor.execute(qstr, data)
		except:
			raise
		return self.db_select(tablename, where)
	
	def db_delete(self, tablename, idx):
		qstr = f"UPDATE {tablename} SET is_deleted=1 WHERE id=%s"
		try:
			self._cursor.execute(qstr, (idx,))
			self._db.commit()
			return idx
		except:
			# print(sys.exc_info())
			return False
	
	def idor404(self, tablename, conds):
		row = self.db_select(tablename, conds)
		if len(row) == 1:
			return row[0]["id"]
		else:
			raise HTTPException(status_code=404, detail=f"Record not found in {tablename}")
	
	def http404(self, text):
		raise HTTPException(status_code=404, detail=text)
	
	def http200(self, text):
		return Response(status_code=200)
		
	def listing_endpoint(self, tablename, additional_conds: dict = Dict):
		if "is_deleted" not in additional_conds:
			additional_conds["is_deleted"] = 0
		return self.db_select(tablename, additional_conds)
	
	def adding_endpoint(self, tablename, records, additional_fields: dict = Dict):
		ids = []
		for record in records:
			newrecord = additional_fields
			newrecord.update(record)
			self.log(newrecord)
			ids.append(self.db_insert(tablename, newrecord, [c.retrows]))
		return ids
	
	def deleting_endpoint(self, tablename, ids):
		for idx in ids:
			self.db_delete(tablename, idx)
		return ids
	
	def patching_endpoint(self, tablename, ids):
		raise AssertionError
		# TODO: prepare patching endpoint
	
	@staticmethod
	def env(varname, default_value):
		return os.getenv(varname, default_value)
	
	@staticmethod
	def err(errcode: int, data: Any):
		return JSONResponse(data, status_code=errcode)
	
	def create_attendee_session(self, paper_id):
		""" create a new session for an attendee/paper pair """
		paper = self.db_selectsingle(c.tblPapers, {"id": paper_id})
		attendee = self.db_selectsingle(c.tblAttendees, {"id": paper["attendee_id"]})
		data = {"attendee_id": attendee["id"], "paper_id": paper_id, "state": SessionState.RUNNING, "started_at": self.now(), "token": self.randstr(64)}
		row = self.db_insert(c.tblSessions, data, [c.retrows])
		return row["token"]
	
	def close_attendee_sessions(self, paper_id):
		""" closes all dangling (previous) sessions of a paper """
		self.db_update(c.tblSessions, {"paper_id": paper_id, "state": SessionState.RUNNING}, {"state": SessionState.CLOSED, "finished_at": self.now()})
	
	def questions_choices(self, test_id, paper_id, question_id: int = 0) -> dict:
		""" returns the choices attendee made for a specific paper (and a specific question if non-zero) """
		questions = self.field2tuple(self.db_select(c.tblQuestions, {"test_id": test_id}))
		choices = self.field2key(self.db_select(c.tblChoices, {"paper_id": paper_id}), "question_id")
		result = {}
		for question in questions:
			if question in choices:
				result[question] = choices[question]["choice"]
			else:
				result[question] = 0
		if question_id:
			result = {question_id: result[question_id]}
		return result
	
	def detailed_question(self, test_id: int, paper_id: int, question_id: int) -> DetailedQuestion:
		question_dict = self.db_selectsingle(c.tblQuestions, {"test_id": test_id, "id": question_id})
		if not question_dict:
			self.http404("Question not found")
		question_dict["options"] = []
		question = DetailedQuestion(**question_dict)
		option_group = self.db_selectsingle(c.tblOptionGroups, {"id": question.optiongroup_id})
		if not option_group:
			self.http404("Question options not found")
		question.options = json.loads(option_group["texts"])
		question.choice = self.questions_choices(test_id, paper_id, question_id)[question_id]
		return question
