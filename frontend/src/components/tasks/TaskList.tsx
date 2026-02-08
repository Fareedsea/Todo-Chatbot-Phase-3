// T041: TaskList component rendering array of TaskCards

'use client';

import React from 'react';
import { Task } from '@/types/task';
import TaskCard from './TaskCard';

interface TaskListProps {
  tasks: Task[];
  onEditTask?: (task: Task) => void;
  onDeleteTask?: (task: Task) => void;
  onToggleComplete?: (task: Task) => void;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onEditTask,
  onDeleteTask,
  onToggleComplete,
}) => {
  if (tasks.length === 0) {
    return null;
  }

  // Sort tasks: incomplete first, then by due date, then by creation date
  const sortedTasks = [...tasks].sort((a, b) => {
    // Completed tasks go to bottom
    if (a.isCompleted !== b.isCompleted) {
      return a.isCompleted ? 1 : -1;
    }

    // Sort by due date if both have one
    if (a.dueDate && b.dueDate) {
      return new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime();
    }

    // Tasks with due dates come before those without
    if (a.dueDate && !b.dueDate) return -1;
    if (!a.dueDate && b.dueDate) return 1;

    // Sort by creation date (newest first)
    return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
  });

  return (
    <div className="space-y-3">
      {sortedTasks.map((task) => {
        return (
          <TaskCard
            key={task.id}
            task={task}
            onEdit={onEditTask}
            onDelete={onDeleteTask}
            onToggleComplete={onToggleComplete}
          />
        );
      })}
    </div>
  );
};

export default TaskList;
