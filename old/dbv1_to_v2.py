@app.get("/import")
async def import_old_data() -> Dict:
	""" imports old database tables, surveys=>tests, questions=>questions,optiongroups """
	surveys = h.field2key(h.db_select("old_surveys", {}, "sid"), "sid")
	for (surveyid, survey) in surveys.items():
		# newrow = {"typ": survey["stitle"], "title": surveyid, "pretext": survey["greetings"]}
		pass
	tests = h.field2key(h.db_select("tests"), "title")
	questions = h.field2key(h.db_select("old_questions", {}, "qid"), "qid")
	optgroups = []
	for (qid, question) in questions.items():
		# prepare for ETL
		optiongroup = {}
		test = tests[question["sid"]]
		# find or save the optiongroup
		if question["qoptions"][:3] == "iq/":
			question["qoptions"] = question["qoptions"][3:]
		qoptions = question["qoptions"].split(";")
		qpoints = question["qvalues"].split(";")
		for idx in range(len(qoptions)):
			optiongroup[qoptions[idx]] = int(qpoints[idx])
			if question["direction"] == "-":
				optiongroup[qoptions[idx]] = 0 - int(qpoints[idx])
		opttext = json.dumps(optiongroup)
		optiongroup_id = h.db_select("optiongroups", {"texts": opttext})
		if not optiongroup_id:
			optiongroup_id = h.db_insert("optiongroups", {"texts": opttext}, [c.retrows])
		optiongroup_id = optiongroup_id[0]["id"]
		# save the question
		newquestion = {"typ": test["typ"], "body": question["question"], "test_id": test["id"], "qorder": question["ordernum"], "dimension": question["dimension"], "optiongroup_id": optiongroup_id}
		h.db_insert("questions", newquestion)
		# return [question, test, optiongroup, newquestion]
	return questions

