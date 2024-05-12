SELECT s.id, count(a.id) AS graded_assignments_count
FROM students s
JOIN assignments a ON s.id = a.student_id AND a.state = 'GRADED'
GROUP BY s.id;

