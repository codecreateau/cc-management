SELECT table_name FROM information_schema.tables
	WHERE table_name IN (
		'classes',
		'contacts',
		'course_history',
		'courses',
		'enrolments',
		'institutions',
		'locations',
		'students',
		'teachers'
	);
