SELECT COUNT(*)
FROM (
    SELECT teacher_id, COUNT(*) AS assignment_count
    FROM assignments
    WHERE grade = 'A'
    GROUP BY teacher_id
    ORDER BY assignment_count DESC
    LIMIT 1
) AS teachers_with_max_grading
