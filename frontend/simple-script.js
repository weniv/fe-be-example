// 할일 목록을 표시하는 함수 (더미 데이터 사용)
function displayTodos() {
    const todosContainer = document.getElementById('todos');
    
    // 더미 데이터
    const dummyTodos = [
        { id: 1, title: "FastAPI 공부하기", description: "Step 5 완료하기", completed: false },
        { id: 2, title: "JavaScript 연습", description: "프론트엔드 개발", completed: true }
    ];
    
    if (dummyTodos.length === 0) {
        todosContainer.innerHTML = '<p class="loading">등록된 할일이 없습니다.</p>';
        return;
    }
    
    todosContainer.innerHTML = dummyTodos.map(todo => `
        <div class="todo-item ${todo.completed ? 'completed' : ''}">
            <h3>${todo.title}</h3>
            <p>${todo.description || '설명 없음'}</p>
            <div class="todo-actions">
                <button class="complete-btn" onclick="toggleTodo(${todo.id})">
                    ${todo.completed ? '미완료로 변경' : '완료'}
                </button>
                <button class="delete-btn" onclick="deleteTodo(${todo.id})">
                    삭제
                </button>
            </div>
        </div>
    `).join('');
}

// 새 할일 추가 (화면에만 표시)
function addTodo() {
    const title = document.getElementById('todoTitle').value.trim();
    const description = document.getElementById('todoDescription').value.trim();
    
    if (!title) {
        alert('할일 제목을 입력해주세요');
        return;
    }
    
    // 폼 초기화
    document.getElementById('todoTitle').value = '';
    document.getElementById('todoDescription').value = '';
    
    alert(`"${title}" 할일이 추가되었습니다! (실제로는 저장되지 않음)`);
    
    // 할일 목록 새로고침
    displayTodos();
}

// 할일 완료 상태 토글 (더미)
function toggleTodo(todoId) {
    alert(`할일 ${todoId}의 상태가 변경되었습니다! (실제로는 저장되지 않음)`);
    displayTodos();
}

// 할일 삭제 (더미)
function deleteTodo(todoId) {
    if (confirm('이 할일을 삭제하시겠습니까?')) {
        alert(`할일 ${todoId}가 삭제되었습니다! (실제로는 삭제되지 않음)`);
        displayTodos();
    }
}

// Enter 키로 할일 추가
document.addEventListener('DOMContentLoaded', function() {
    // 페이지 로드 시 할일 목록 표시
    displayTodos();
    
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