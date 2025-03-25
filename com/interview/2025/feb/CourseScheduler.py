from collections import defaultdict, deque


class CourseScheduler:

    def can_finish(self, num_courses, prerequisites):
        graph = defaultdict(list)  # Represents the adjacency list of graph
        indegrees = [0] * num_courses  # Stores number of prerequisites for each course

        for course, prereq in prerequisites:
            graph[prereq].append(course)  # Add edge from prereq to course
            indegrees[course] += 1  # Increment indegree of course

        queue = deque([i for i in range(num_courses) if indegrees[i] == 0])  # Courses without prerequisites
        courses_completed = 0  # Counter for courses processed

        while queue:
            current = queue.popleft()  # Take a course with no prerequisites
            courses_completed += 1

            for neighbor in graph[current]:
                indegrees[neighbor] -= 1  # Decrement indegree as prerequisite is fulfilled
                if indegrees[neighbor] == 0:  # If no more prerequisites, enqueue the course
                    queue.append(neighbor)

        return courses_completed == num_courses  # True if all courses completed, else False
