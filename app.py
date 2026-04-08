import os
from nicegui import ui
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Берём переменные из окружения (будут переданы через Docker)
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'tasksdb')

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)

Base.metadata.create_all(engine)

current_edit_id = None

@ui.page('/')
def main():
    global current_edit_id
    
    ui.label('Task Manager - Docker Version').classes('text-2xl font-bold')
    
    with ui.card():
        title_input = ui.input('Название')
        desc_input = ui.textarea('Описание')
        
        def save():
            global current_edit_id
            if not title_input.value:
                ui.notify('Введите название!', type='warning')
                return
            session = Session()
            if current_edit_id:
                task = session.query(Task).filter(Task.id == current_edit_id).first()
                if task:
                    task.title = title_input.value
                    task.description = desc_input.value
                current_edit_id = None
                save_btn.set_text('Добавить')
            else:
                task = Task(title=title_input.value, description=desc_input.value)
                session.add(task)
            session.commit()
            session.close()
            refresh()
            title_input.set_value('')
            desc_input.set_value('')
            ui.notify('Сохранено!', type='positive')
        
        save_btn = ui.button('Добавить', on_click=save, icon='add')
        ui.button('Очистить', on_click=lambda: (title_input.set_value(''), desc_input.set_value(''), clear_edit()))
        
        def clear_edit():
            global current_edit_id
            current_edit_id = None
            save_btn.set_text('Добавить')
    
    columns = [
        {'name': 'id', 'label': 'ID', 'field': 'id'},
        {'name': 'title', 'label': 'Название', 'field': 'title'},
        {'name': 'desc', 'label': 'Описание', 'field': 'desc'},
    ]
    table = ui.table(columns=columns, rows=[], selection='single', row_key='id').classes('w-full')
    
    def refresh():
        session = Session()
        tasks = session.query(Task).all()
        rows = [{'id': t.id, 'title': t.title, 'desc': t.description or ''} for t in tasks]
        session.close()
        table.rows = rows
    
    def edit_row():
        global current_edit_id
        if not table.selected:
            ui.notify('Выберите задачу!', type='warning')
            return
        task = table.selected[0]
        title_input.set_value(task['title'])
        desc_input.set_value(task['desc'])
        current_edit_id = task['id']
        save_btn.set_text('Обновить')
    
    def delete_row():
        if not table.selected:
            ui.notify('Выберите задачу!', type='warning')
            return
        task_id = table.selected[0]['id']
        session = Session()
        session.query(Task).filter(Task.id == task_id).delete()
        session.commit()
        session.close()
        refresh()
        ui.notify('Удалено!', type='negative')
    
    with ui.row().classes('w-full justify-end gap-2'):
        ui.button('Редактировать', on_click=edit_row, icon='edit')
        ui.button('Удалить', on_click=delete_row, icon='delete', color='red')
    
    refresh()

ui.run(title='Lab2 Docker', port=8080, host='0.0.0.0', reload=False)
