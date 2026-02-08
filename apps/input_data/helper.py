def resolve_sql_params(sql, params, print_sql = False):

	"""
	Replace the placeholders in the SQL query with the actual parameters for debugging purposes.
	:param sql: The SQL query with placeholders.
	:param params: The parameters to replace the placeholders.
	:param print_sql: If true, print the resolved SQL query.
	:return: The SQL query with parameters replaced.
	"""
	if params is None:
		return sql
	for param in params:
		if isinstance(param, str):
			param = f"'{param}'"
		elif param is None:
			param = 'NULL'
		sql = sql.replace('%s', str(param), 1)
	if print_sql:
		print(sql)
	return sql

