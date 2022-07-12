from enum import Enum, unique


@unique
class TestType(str, Enum):
	""" types of tests (myers-briggs etc) """
	MB = "MB"
	BIGFIVE = "BIGFIVE"
	APTITUDE = "APTITUDE"
	DISC = "DISC"

	def __str__(self):
		return str(self.value)


@unique
class QuestionType(str, Enum):
	""" types of questions (currently only multichoice) """
	qt_text = "qt_text"  # mc meaning multiple choice
	qt_images = "qt_images"

	def str(self):
		return str(self.value)


class SessionState(str, Enum):
	""" states of answering sessions """
	RUNNING = "RUNNING"
	CLOSED = "CLOSED"
	DONE = "DONE"

	def str(self):
		return str(self.value)


class ActionType(str, Enum):
	""" used in both actions table and oplogs table (because an action can be queued for later or performed) """
	CREATE = "CREATE"  # create question, create session
	READ = "READ"
	UPDATE = "UPDATE"
	DELETE = "DELETE"
	SKIP = "SKIP"  # skip question
	FETCH = "FETCH"  # fetch another question
	ANSWER = "ANSWER"  # answer question
	LOGIN = "LOGIN"
	LOGOUT = "LOGOUT"
	START = "START"
	END = "END"
	CRON = "CRON"
	ACCESS = "ACCESS"  # assess (score) a candidate's finished session
	CREATEPDF = "CREATEPDF"  # create pdf from a finished session

	def str(self):
		return str(self.value)


class ObjectType(str, Enum):
	""" used in oplogs and action queue; in simplest terms, the list of objects (combines with actiontype, ie. actiontype is create, and actionobject is user) """
	ot_page: "ot_page"
	ot_attendee: "ot_attendee"
	ot_choice: "ot_choice"
	ot_customer: "ot_customer"
	ot_customertest: "ot_customertest"
	ot_optiongroup: "ot_optiongroup"
	ot_paper: "ot_paper"
	ot_partner: "ot_partner"
	ot_partnertest: "ot_partnertest"
	ot_perm: "ot_perm"
	ot_question: "ot_question"
	ot_role: "ot_role"
	ot_roleperm: "ot_roleperm"
	ot_session: "ot_session"
	ot_test: "ot_test"
	ot_user: "ot_user"
	ot_userperm: "ot_userperm"
	ot_userrole: "ot_userrole"

	def str(self):
		return str(self.value)
