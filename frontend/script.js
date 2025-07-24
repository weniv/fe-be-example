// 할일 목록을 표시하는 함수 (더미 데이터 사용)
function displayTodos() {
    // HTML에서 할일을 표시할 컨테이너 요소를 가져옵니다
    const todosContainer = document.getElementById('todos');
    
    // 더미 데이터 - 실제 API 연동 전 테스트용 데이터
    const dummyTodos = [
        { 
            id: 1, 
            title: "FastAPI 공부하기", 
            description: "Step 5 완료하기", 
            completed: false 
        },
        { 
            id: 2, 
            title: "JavaScript 연습", 
            description: "프론트엔드 개발", 
            completed: true 
        }
    ];
    
    // 할일이 없는 경우 메시지 표시
    if (dummyTodos.length === 0) {
        todosContainer.innerHTML = '<p class="loading">등록된 할일이 없습니다.</p>';
        return;
    }
    
    // 각 할일을 HTML 요소로 변환하여 화면에 표시
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

// 새 할일 추가 함수 (현재는 화면에만 표시, 실제 저장은 되지 않음)
function addTodo() {
    // 입력 필드에서 값을 가져옵니다
    const title = document.getElementById('todoTitle').value.trim();
    const description = document.getElementById('todoDescription').value.trim();
    
    // 제목이 입력되지 않은 경우 경고 메시지 표시
    if (!title) {
        alert('할일 제목을 입력해주세요');
        return;
    }
    
    // 입력 필드 초기화 (폼을 깨끗하게 만듦)
    document.getElementById('todoTitle').value = '';
    document.getElementById('todoDescription').value = '';
    
    // 사용자에게 추가되었다는 메시지 표시 (실제로는 저장되지 않음)
    alert(`"${title}" 할일이 추가되었습니다! (실제로는 저장되지 않음)`);
    
    // 할일 목록을 다시 표시 (변화 없음, 더미 데이터만 표시)
    displayTodos();
}

// 할일 완료 상태를 토글하는 함수 (더미 함수)
function toggleTodo(todoId) {
    // 실제로는 서버에 요청을 보내 상태를 변경해야 하지만,
    // 현재는 메시지만 표시
    alert(`할일 ${todoId}의 상태가 변경되었습니다! (실제로는 저장되지 않음)`);
    
    // 할일 목록을 다시 표시 (변화 없음, 더미 데이터만 표시)
    displayTodos();
}

// 할일을 삭제하는 함수 (더미 함수)
function deleteTodo(todoId) {
    // 사용자에게 삭제 확인을 요청
    if (confirm('이 할일을 삭제하시겠습니까?')) {
        // 실제로는 서버에 요청을 보내 삭제해야 하지만,
        // 현재는 메시지만 표시
        alert(`할일 ${todoId}가 삭제되었습니다! (실제로는 삭제되지 않음)`);
        
        // 할일 목록을 다시 표시 (변화 없음, 더미 데이터만 표시)
        displayTodos();
    }
}

// 페이지가 완전히 로드된 후 실행되는 함수
document.addEventListener('DOMContentLoaded', function() {
    // 페이지 로드 시 할일 목록을 표시
    displayTodos();
    
    // Enter 키를 눌렀을 때 할일을 추가하는 이벤트 리스너 추가
    
    // 제목 입력 필드에서 Enter 키 처리
    document.getElementById('todoTitle').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTodo(); // Enter 키를 누르면 할일 추가
        }
    });

    // 설명 입력 필드에서 Enter 키 처리
    document.getElementById('todoDescription').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTodo(); // Enter 키를 누르면 할일 추가
        }
    });
});