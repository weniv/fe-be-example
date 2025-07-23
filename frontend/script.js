/**
 * 할일 관리 앱 JavaScript
 * FastAPI 백엔드와 통신하여 할일을 관리하는 프론트엔드 스크립트
 * 
 * 이 파일의 역할:
 * 1. 인증된 사용자의 할일 CRUD 작업을 처리합니다
 * 2. JWT 토큰을 사용하여 API 요청을 인증합니다
 * 3. 할일 목록을 동적으로 표시하고 관리합니다
 * 4. 검색 및 필터링 기능을 제공합니다
 */

// API 기본 URL 설정
// 백엔드 서버가 실행되는 주소 (auth.js와 동일)
const API_BASE_URL = 'http://localhost:8000';

// 전역 변수로 할일 목록 저장 (검색 기능을 위해)
let allTodos = [];

// DOM이 완전히 로드된 후 실행
// 페이지가 로드되면 자동으로 할일 목록을 불러옴
document.addEventListener('DOMContentLoaded', function() {
    // 메인 페이지에서만 할일 목록 로드
    const currentPage = window.location.pathname.split('/').pop();
    if (currentPage === 'main.html') {
        loadTodos();
    }
});

/**
 * 서버에서 할일 목록을 불러오는 함수
 * async/await를 사용하여 비동기 처리
 */
async function loadTodos() {
    try {
        // 로딩 표시
        showLoading();
        
        // API에서 할일 목록 가져오기 (인증된 요청)
        const response = await authenticatedFetch(`${API_BASE_URL}/todos/`);
        
        // 응답 상태 확인
        if (!response.ok) {
            throw new Error('할일 목록을 불러오는데 실패했습니다');
        }
        
        // JSON 데이터로 변환
        const todos = await response.json();
        
        // 전역 변수에 저장
        allTodos = todos;
        
        // 화면에 표시
        displayTodos(todos);
    } catch (error) {
        // 오류 발생 시 오류 메시지 표시
        showError(error.message);
    }
}

/**
 * 할일 목록을 화면에 표시하는 함수
 * @param {Array} todos - 할일 객체 배열
 */
function displayTodos(todos) {
    const todosContainer = document.getElementById('todos');
    
    // 할일이 없는 경우
    if (todos.length === 0) {
        todosContainer.innerHTML = '<p class="loading">등록된 할일이 없습니다.</p>';
        return;
    }
    
    // 할일 목록을 HTML로 변환
    // map() 함수로 각 할일을 HTML 문자열로 변환하고 join()으로 합침
    todosContainer.innerHTML = todos.map(todo => {
        // 우선순위 텍스트 및 클래스 설정
        const priorityText = todo.priority === 1 ? '🔴 높음' : 
                           todo.priority === 2 ? '🟡 보통' : '🟢 낮음';
        const priorityClass = todo.priority === 1 ? 'high' : 
                            todo.priority === 2 ? 'medium' : 'low';
        
        // 생성일자 포맷팅
        const createdDate = new Date(todo.created_at).toLocaleDateString('ko-KR');
        
        return `
            <div class="todo-item priority-${todo.priority} ${todo.completed ? 'completed' : ''}">
                <div>
                    <span class="priority-badge ${priorityClass}">${priorityText}</span>
                    <h3>${todo.title}</h3>
                </div>
                <p>${todo.description || '설명 없음'}</p>
                <div class="created-date">생성일: ${createdDate}</div>
                <div class="todo-actions">
                    <button class="complete-btn" onclick="toggleTodo(${todo.id}, ${!todo.completed})">
                        ${todo.completed ? '미완료로 변경' : '완료'}
                    </button>
                    <button class="delete-btn" onclick="deleteTodo(${todo.id})">
                        삭제
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

/**
 * 새로운 할일을 추가하는 함수
 * 폼에서 입력받은 데이터를 서버로 전송
 */
async function addTodo() {
    // 입력 필드에서 값 가져오기 (trim()으로 공백 제거)
    const title = document.getElementById('todoTitle').value.trim();
    const description = document.getElementById('todoDescription').value.trim();
    const priority = parseInt(document.getElementById('todoPriority').value);
    
    // 제목이 비어있는지 확인
    if (!title) {
        showError('할일 제목을 입력해주세요');
        return;
    }
    
    try {
        // POST 요청으로 새 할일 생성
        const response = await authenticatedFetch(`${API_BASE_URL}/todos/`, {
            method: 'POST',
            body: JSON.stringify({
                title: title,
                description: description,
                priority: priority
            })
        });
        
        // 응답 확인
        if (!response.ok) {
            throw new Error('할일 추가에 실패했습니다');
        }
        
        // 성공 시 폼 초기화
        document.getElementById('todoTitle').value = '';
        document.getElementById('todoDescription').value = '';
        document.getElementById('todoPriority').value = '2'; // 기본값으로 재설정
        
        // 할일 목록 새로고침
        loadTodos();
        
    } catch (error) {
        showError(error.message);
    }
}

/**
 * 할일의 완료 상태를 토글하는 함수
 * @param {number} todoId - 할일 ID
 * @param {boolean} completed - 새로운 완료 상태
 */
async function toggleTodo(todoId, completed) {
    try {
        // PUT 요청으로 할일 상태 업데이트 (인증된 요청)
        const response = await authenticatedFetch(`${API_BASE_URL}/todos/${todoId}`, {
            method: 'PUT',
            body: JSON.stringify({
                completed: completed // 완료 상태만 업데이트
            })
        });
        
        if (!response.ok) {
            throw new Error('할일 상태 변경에 실패했습니다');
        }
        
        // 성공 시 목록 새로고침
        loadTodos();
        
    } catch (error) {
        showError(error.message);
    }
}

/**
 * 할일을 삭제하는 함수
 * @param {number} todoId - 삭제할 할일 ID
 */
async function deleteTodo(todoId) {
    // 삭제 확인 대화상자
    if (!confirm('이 할일을 삭제하시겠습니까?')) {
        return;
    }
    
    try {
        // DELETE 요청으로 할일 삭제 (인증된 요청)
        const response = await authenticatedFetch(`${API_BASE_URL}/todos/${todoId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('할일 삭제에 실패했습니다');
        }
        
        // 성공 시 목록 새로고침
        loadTodos();
        
    } catch (error) {
        showError(error.message);
    }
}

/**
 * 로딩 상태를 표시하는 함수
 */
function showLoading() {
    document.getElementById('todos').innerHTML = '<p class="loading">로딩 중...</p>';
}

/**
 * 오류 메시지를 표시하는 함수
 * @param {string} message - 표시할 오류 메시지
 */
function showError(message) {
    const todosContainer = document.getElementById('todos');
    todosContainer.innerHTML = `<div class="error">${message}</div>`;
}

// DOM 로드 완료 후 이벤트 리스너 추가
document.addEventListener('DOMContentLoaded', function() {
    // Enter 키 이벤트 리스너 추가 (요소가 존재하는 경우에만)
    const todoTitleElement = document.getElementById('todoTitle');
    const todoDescriptionElement = document.getElementById('todoDescription');
    
    // 제목 입력 필드에서 Enter 키를 누르면 할일 추가
    if (todoTitleElement) {
        todoTitleElement.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addTodo();
            }
        });
    }

    // 설명 입력 필드에서도 Enter 키로 할일 추가 가능
    if (todoDescriptionElement) {
        todoDescriptionElement.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addTodo();
            }
        });
    }
});

/**
 * 할일 검색 기능
 * 제목과 설명에서 검색어를 찾아 필터링
 */
function filterTodos() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
    
    // 검색어가 없으면 모든 할일 표시
    if (!searchTerm) {
        displayTodos(allTodos);
        return;
    }
    
    // 제목이나 설명에 검색어가 포함된 할일들 필터링
    const filteredTodos = allTodos.filter(todo => 
        todo.title.toLowerCase().includes(searchTerm) ||
        (todo.description && todo.description.toLowerCase().includes(searchTerm))
    );
    
    displayTodos(filteredTodos);
}