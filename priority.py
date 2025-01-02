class Priority:
    def __init__(self):
        self.priority_groups = {"High": [], "Medium": [], "Low": []}

    def add_task(self, task, priority="Medium"):
        self.priority_groups[priority].append(task)

    def remove_task(self, task):
        for priority in self.priority_groups:
            if task in self.priority_groups[priority]:
                self.priority_groups[priority].remove(task)
                break

    def get_tasks(self, priority):
        return self.priority_groups.get(priority, [])

    def get_all_tasks(self):
        return self.priority_groups