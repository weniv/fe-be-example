/**
 * 할일 관리 앱 JavaScript - API 연동 버전
 * FastAPI 백엔드와 실제로 통신하여 데이터를 저장/조회하는 스크립트
 * 
 * 이 파일의 주요 변화:
 * 1. 더미 데이터 대신 실제 API 통신
 * 2. fetch() 함수를 사용한 HTTP 요청
 * 3. async/await를 사용한 비동기 처리
 * 4. 에러 처리 및 로딩 상태 관리
 */

// API 기본 URL 설정
// 백엔드 FastAPI 서버가 실행되는 주소
const API_BASE_URL = 'http://localhost:8000';

// DOM이 완전히 로드된 후 실행
// 페이지가 로드되면 자동으로 할일 목록을 불러옴
document.addEventListener('DOMContentLoaded', function() {
    // 할일 목록을 서버에서 불러옴
    loadTodos();
});

/**
 * 서버에서 할일 목록을 불러오는 함수
 * fetch() API를 사용하여 비동기 HTTP 요청 처리
 */
async function loadTodos() {
    try {
        // 로딩 상태 표시
        showLoading();
        
        // GET 요청으로 서버에서 할일 목록 가져오기
        const response = await fetch(`${API_BASE_URL}/todos/`);
        
        // HTTP 응답 상태 확인 (200번대가 아니면 에러)
        if (!response.ok) {
            throw new Error('할일 목록을 불러오는데 실패했습니다');
        }
        
        // 응답 데이터를 JSON으로 변환
        const todos = await response.json();
        
        // 화면에 할일 목록 표시
        displayTodos(todos);
    } catch (error) {
        // 네트워크 오류나 서버 오류 발생 시 에러 메시지 표시
        showError(error.message);
    }
}

/**
 * 할일 목록을 화면에 표시하는 함수
 * @param {Array} todos - 서버에서 받아온 할일 객체 배열
 */
function displayTodos(todos) {
    const todosContainer = document.getElementById('todos');
    
    // 할일이 없는 경우 안내 메시지 표시
    if (todos.length === 0) {
        todosContainer.innerHTML = '<p class="loading">등록된 할일이 없습니다.</p>';
        return;
    }
    
    // 할일 목록을 HTML로 변환하여 화면에 표시
    // map() 함수로 각 할일을 HTML 문자열로 변환하고 join()으로 합침
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

/**
 * 새로운 할일을 추가하는 함수
 * 폼에서 입력받은 데이터를 서버로 POST 요청으로 전송
 */
async function addTodo() {
    // 입력 필드에서 값 가져오기 (trim()으로 앞뒤 공백 제거)
    const title = document.getElementById('todoTitle').value.trim();
    const description = document.getElementById('todoDescription').value.trim();
    
    // 제목이 비어있는지 유효성 검사
    if (!title) {
        alert('할일 제목을 입력해주세요');
        return;
    }
    
    try {
        // POST 요청으로 서버에 새로운 할일 생성
        const response = await fetch(`${API_BASE_URL}/todos/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // JSON 데이터 전송을 위한 헤더
            },
            body: JSON.stringify({
                title: title,
                description: description
            })
        });
        
        // 응답 상태 확인
        if (!response.ok) {
            throw new Error('할일 추가에 실패했습니다');
        }
        
        // 성공 시 입력 폼 초기화
        document.getElementById('todoTitle').value = '';
        document.getElementById('todoDescription').value = '';
        
        // 할일 목록을 다시 불러와서 화면 업데이트
        loadTodos();
        
    } catch (error) {
        // 오류 발생 시 에러 메시지 표시
        showError(error.message);
    }
}

/**
 * 할일의 완료 상태를 토글하는 함수
 * @param {number} todoId - 수정할 할일의 ID
 * @param {boolean} completed - 변경할 완료 상태 (true/false)
 */
async function toggleTodo(todoId, completed) {
    try {
        // PUT 요청으로 서버에서 할일 상태 업데이트
        const response = await fetch(`${API_BASE_URL}/todos/${todoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                completed: completed // 완료 상태만 업데이트
            })
        });
        
        // 응답 상태 확인
        if (!response.ok) {
            throw new Error('할일 상태 변경에 실패했습니다');
        }
        
        // 성공 시 할일 목록을 다시 불러와서 화면 업데이트
        loadTodos();
        
    } catch (error) {
        showError(error.message);
    }
}

/**
 * 할일을 삭제하는 함수
 * @param {number} todoId - 삭제할 할일의 ID
 */
async function deleteTodo(todoId) {
    // 사용자에게 삭제 확인을 요청
    if (!confirm('이 할일을 삭제하시겠습니까?')) {
        return;
    }
    
    try {
        // DELETE 요청으로 서버에서 할일 삭제
        const response = await fetch(`${API_BASE_URL}/todos/${todoId}`, {
            method: 'DELETE'
        });
        
        // 응답 상태 확인
        if (!response.ok) {
            throw new Error('할일 삭제에 실패했습니다');
        }
        
        // 성공 시 할일 목록을 다시 불러와서 화면 업데이트
        loadTodos();
        
    } catch (error) {
        showError(error.message);
    }
}

/**
 * 로딩 상태를 표시하는 함수
 * 서버에서 데이터를 불러오는 동안 로딩 메시지를 표시
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

// Enter 키 이벤트 리스너 추가
// DOM이 완전히 로드된 후 이벤트 리스너를 추가하여 사용자 편의성 향상
document.addEventListener('DOMContentLoaded', function() {
    // 제목 입력 필드에서 Enter 키를 누르면 할일 추가
    document.getElementById('todoTitle').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTodo(); // Enter 키를 누르면 할일 추가
        }
    });

    // 설명 입력 필드에서도 Enter 키로 할일 추가 가능
    document.getElementById('todoDescription').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTodo(); // Enter 키를 누르면 할일 추가
        }
    });
});