/**
 * 인증 관련 JavaScript 모듈
 * 
 * 이 파일의 역할:
 * 1. 🔐 사용자 로그인, 회원가입, 로그아웃 기능을 구현합니다
 * 2. 🗄️ JWT 토큰을 로컬 스토리지에 안전하게 저장하고 관리합니다
 * 3. 🌐 API 요청 시 Authorization 헤더에 토큰을 자동으로 포함시킵니다
 * 4. 🛡️ 인증이 필요한 페이지에서 로그인 상태를 확인하고 보호합니다
 * 5. 🔄 토큰 만료나 오류 시 자동으로 로그아웃 처리합니다
 * 
 * 보안 특징:
 * - 토큰은 브라우저의 로컬 스토리지에 저장됩니다
 * - 모든 API 요청에 Bearer 토큰이 자동으로 포함됩니다
 * - 토큰이 유효하지 않으면 자동으로 로그인 페이지로 리다이렉트됩니다
 * - 비밀번호는 평문으로 저장되지 않고 서버에서 해싱됩니다
 * 
 * 초보자를 위한 설명:
 * - JWT: JSON Web Token, 사용자 인증 정보를 안전하게 담은 토큰
 * - 로컬 스토리지: 브라우저에 데이터를 저장하는 영구 저장소 (쿠키와 유사)
 * - API: 백엔드 서버와 통신하기 위한 인터페이스 (데이터 요청/응답)
 * - Bearer 토큰: HTTP 헤더에 포함되는 인증 방식 ("Bearer " + 토큰 문자열)
 */

// API 기본 URL (백엔드 서버 주소)
const API_BASE_URL = 'http://localhost:8000';

// ====== 토큰 관리 함수들 ======

/**
 * 로컬 스토리지에서 JWT 토큰을 가져옵니다
 * 
 * Returns:
 *     string | null: 저장된 토큰 또는 null (없는 경우)
 */
function getToken() {
    return localStorage.getItem('access_token');
}

/**
 * 로컬 스토리지에 JWT 토큰을 저장합니다
 * 
 * Args:
 *     token: 저장할 JWT 토큰
 */
function setToken(token) {
    localStorage.setItem('access_token', token);
}

/**
 * 로컬 스토리지에서 JWT 토큰을 제거합니다
 */
function removeToken() {
    localStorage.removeItem('access_token');
}

/**
 * 현재 사용자가 로그인 상태인지 확인합니다
 * 
 * Returns:
 *     boolean: 로그인 상태면 true, 아니면 false
 */
function isLoggedIn() {
    const token = getToken();
    return token !== null && token !== '';
}

// ====== API 요청 함수들 ======

/**
 * 인증 헤더가 포함된 fetch 요청을 보냅니다
 * 
 * Args:
 *     url: 요청할 URL
 *     options: fetch 옵션 객체
 * 
 * Returns:
 *     Promise: fetch 응답 Promise
 */
async function authenticatedFetch(url, options = {}) {
    const token = getToken();
    
    // 기본 헤더 설정
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    // 토큰이 있으면 Authorization 헤더 추가
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    return fetch(url, {
        ...options,
        headers
    });
}

// ====== 회원가입 함수 ======

/**
 * 회원가입 폼 제출을 처리합니다
 * 
 * Args:
 *     event: 폼 제출 이벤트
 */
async function handleSignup(event) {
    // 기본 폼 제출 동작을 막습니다 (페이지 새로고침 방지)
    event.preventDefault();
    
    // 폼 데이터 가져오기
    const formData = new FormData(event.target);
    const username = formData.get('username');
    const email = formData.get('email');
    const password = formData.get('password');
    const confirmPassword = formData.get('confirmPassword');
    
    // 에러 메시지 초기화
    hideMessage('errorMessage');
    hideMessage('successMessage');
    
    // 비밀번호 확인 검증
    if (password !== confirmPassword) {
        showError('비밀번호가 일치하지 않습니다.');
        return;
    }
    
    try {
        // 회원가입 API 요청
        const response = await fetch(`${API_BASE_URL}/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // 회원가입 성공
            showSuccess('회원가입이 완료되었습니다! 로그인 페이지로 이동합니다.');
            
            // 2초 후 로그인 페이지로 이동
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            // 회원가입 실패
            showError(data.detail || '회원가입에 실패했습니다.');
        }
    } catch (error) {
        console.error('회원가입 에러:', error);
        showError('서버와의 연결에 문제가 발생했습니다.');
    }
}

// ====== 로그인 함수 ======

/**
 * 로그인 폼 제출을 처리합니다
 * 
 * Args:
 *     event: 폼 제출 이벤트
 */
async function handleLogin(event) {
    // 기본 폼 제출 동작을 막습니다
    event.preventDefault();
    
    // 폼 데이터 가져오기
    const formData = new FormData(event.target);
    const username = formData.get('username');
    const password = formData.get('password');
    
    // 에러 메시지 초기화
    hideMessage('errorMessage');
    
    try {
        // 로그인 API 요청
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // 로그인 성공: 토큰 저장 후 메인 페이지로 이동
            setToken(data.access_token);
            window.location.href = 'main.html';
        } else {
            // 로그인 실패
            showError(data.detail || '로그인에 실패했습니다.');
        }
    } catch (error) {
        console.error('로그인 에러:', error);
        showError('서버와의 연결에 문제가 발생했습니다.');
    }
}

// ====== 로그아웃 함수 ======

/**
 * 로그아웃을 처리합니다
 */
function logout() {
    // 토큰 제거
    removeToken();
    
    // 로그인 페이지로 이동
    window.location.href = 'login.html';
}

// ====== 사용자 정보 로드 함수 ======

/**
 * 현재 로그인한 사용자 정보를 가져와서 표시합니다
 */
async function loadUserInfo() {
    try {
        const response = await authenticatedFetch(`${API_BASE_URL}/me`);
        
        if (response.ok) {
            const user = await response.json();
            
            // 환영 메시지 업데이트
            const welcomeMessage = document.getElementById('welcomeMessage');
            if (welcomeMessage) {
                welcomeMessage.textContent = `환영합니다, ${user.username}님!`;
            }
        } else if (response.status === 401) {
            // 토큰이 만료되었거나 유효하지 않음
            logout();
        }
    } catch (error) {
        console.error('사용자 정보 로드 에러:', error);
        logout();
    }
}

// ====== 페이지 보호 함수 ======

/**
 * 로그인이 필요한 페이지에서 인증 상태를 확인합니다
 * 로그인하지 않은 사용자는 로그인 페이지로 리다이렉트됩니다
 */
function requireLogin() {
    if (!isLoggedIn()) {
        // 로그인하지 않은 경우 로그인 페이지로 이동
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

/**
 * 이미 로그인한 사용자가 인증 페이지(로그인/회원가입)에 접근하는 것을 방지합니다
 */
function redirectIfLoggedIn() {
    if (isLoggedIn()) {
        // 이미 로그인한 경우 메인 페이지로 이동
        window.location.href = 'main.html';
    }
}

// ====== 메시지 표시 함수들 ======

/**
 * 에러 메시지를 표시합니다
 * 
 * Args:
 *     message: 표시할 에러 메시지
 */
function showError(message) {
    const errorElement = document.getElementById('errorMessage');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

/**
 * 성공 메시지를 표시합니다
 * 
 * Args:
 *     message: 표시할 성공 메시지
 */
function showSuccess(message) {
    const successElement = document.getElementById('successMessage');
    if (successElement) {
        successElement.textContent = message;
        successElement.style.display = 'block';
    }
}

/**
 * 메시지를 숨깁니다
 * 
 * Args:
 *     elementId: 숨길 메시지 요소의 ID
 */
function hideMessage(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'none';
    }
}

// ====== 페이지 로드 시 실행되는 코드 ======

// DOM이 로드된 후 실행
document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname.split('/').pop();
    
    // 현재 페이지에 따라 적절한 초기화 실행
    if (currentPage === 'main.html') {
        // 메인 페이지: 로그인 확인 후 사용자 정보 로드
        if (requireLogin()) {
            loadUserInfo();
        }
    } else if (currentPage === 'login.html' || currentPage === 'signup.html') {
        // 인증 페이지: 이미 로그인한 사용자는 메인 페이지로 리다이렉트
        redirectIfLoggedIn();
    }
});