import unittest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)

class TestApp(unittest.TestCase):
    
    def setUp(self):
        # Создаём тестовую БД в памяти
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def test_create_task(self):
        session = self.Session()
        task = Task(title="Test", description="Description")
        session.add(task)
        session.commit()
        
        result = session.query(Task).first()
        self.assertEqual(result.title, "Test")
        session.close()
    
    def test_update_task(self):
        session = self.Session()
        task = Task(title="Old", description="Old desc")
        session.add(task)
        session.commit()
        
        task.title = "New"
        session.commit()
        
        result = session.query(Task).first()
        self.assertEqual(result.title, "New")
        session.close()
    
    def test_delete_task(self):
        session = self.Session()
        task = Task(title="ToDelete")
        session.add(task)
        session.commit()
        
        session.delete(task)
        session.commit()
        
        result = session.query(Task).first()
        self.assertIsNone(result)
        session.close()
    
    def test_read_tasks(self):
        session = self.Session()
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        session.add_all([task1, task2])
        session.commit()
        
        tasks = session.query(Task).all()
        self.assertEqual(len(tasks), 2)
        session.close()

if __name__ == '__main__':
    unittest.main()