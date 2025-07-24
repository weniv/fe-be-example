// API 기본 URL
const API_BASE_URL = 'http://localhost:8000';

// 할일 목록 불러오기
async function loadTodos() {
    try {
        showLoading();
        const response = await fetch(`${API_BASE_URL}/todos/`);
        
        if (!response.ok) {
            throw new Error('할일 목록을 불러오는데 실패했습니다');
        }
        
        const todos = await response.json();
        displayTodos(todos);
    } catch (error) {
        showError(error.message);
    }
}

// 할일 목록 화면에 표시
function displayTodos(todos) {
    const todosContainer = document.getElementById('todos');
    
    if (todos.length === 0) {
        todosContainer.innerHTML = '<p class="loading">등록된 할일이 없습니다.</p>';
        return;
    }
    
    todosContainer.innerHTML = todos.map(todo => `
        <div class="todo-item ${todo.completed ? 'completed' : ''}">
            <h3>${todo.title}</h3>
            <p>${todo.description || '설명 없음'}</p>
            <div class="todo-actions">
                <button class="complete-btn" onclick="toggleTodo(${todo.id}, ${!todo.completed})">
                    ${todo.completed ? '미완료로 변경' : '완료'}
                </button>
                <button class="delete-btn" onclick="deleteTodo(${todo.id})">
                    삭제
                </button>
            </div>
        </div>
    `).join('');
}

// 새 할일 추가
async function addTodo() {
    const title = document.getElementById('todoTitle').value.trim();
    const description = document.getElementById('todoDescription').value.trim();
    
    if (!title) {
        showError('할일 제목을 입력해주세요');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/todos/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                description: description
            })
        });
        
        if (!response.ok) {
            throw new Error('할일 추가에 실패했습니다');
        }
        
        // 폼 초기화
        document.getElementById('todoTitle').value = '';
        document.getElementById('todoDescription').value = '';
        
        // 할일 목록 새로고침
        loadTodos();
        
    } catch (error) {
        showError(error.message);
    }
}

// 할일 완료 상태 토글
async function toggleTodo(todoId, completed) {
    try {
        const response = await fetch(`${API_BASE_URL}/todos/${todoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                completed: completed
            })
        });
        
        if (!response.ok) {
            throw new Error('할일 상태 변경에 실패했습니다');
        }
        
        // 할일 목록 새로고침
        loadTodos();
        
    } catch (error) {
        showError(error.message);
    }
}

// 할일 삭제
async function deleteTodo(todoId) {
    if (!confirm('이 할일을 삭제하시겠습니까?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/todos/${todoId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('할일 삭제에 실패했습니다');
        }
        
        // 할일 목록 새로고침
        loadTodos();
        
    } catch (error) {
        showError(error.message);
    }
}

// 로딩 표시
function showLoading() {
    document.getElementById('todos').innerHTML = '<p class="loading">로딩 중...</p>';
}

// 오류 메시지 표시
function showError(message) {
    const todosContainer = document.getElementById('todos');
    todosContainer.innerHTML = `<div class="error">${message}</div>`;
}

// Enter 키로 할일 추가
document.addEventListener('DOMContentLoaded', function() {
    // 페이지 로드 시 할일 목록 불러오기
    loadTodos();
    
    // Enter 키 이벤트 리스너
    document.getElementById('todoTitle').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTodo();
        }
    });

    document.getElementById('todoDescription').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTodo();
        }
    });
});