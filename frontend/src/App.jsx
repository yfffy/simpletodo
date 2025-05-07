import React, { useState } from 'react';
import AddTask from './components/AddTask';
import TaskList from './components/TaskList';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';

function App() {
  const [refreshTasks, setRefreshTasks] = useState(false);

  const handleTaskAdded = () => {
    setRefreshTasks(prev => !prev);
  };

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6 text-center">Simple Todo</h1>
      
      <Tabs defaultValue="add" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="add">Add Task</TabsTrigger>
          <TabsTrigger value="list">Task List</TabsTrigger>
        </TabsList>
        
        <TabsContent value="add">
          <AddTask onTaskAdded={handleTaskAdded} />
        </TabsContent>
        
        <TabsContent value="list">
          <TaskList refreshTrigger={refreshTasks} />
        </TabsContent>
      </Tabs>
    </div>
  );
}

export default App;