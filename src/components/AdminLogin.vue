<template>
  <div class="admin-login">
    <div class="login-container">
      <div class="login-card">
        <h2 class="login-title">ورود به پنل مدیریت</h2>
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username">نام کاربری</label>
            <input
              id="username"
              v-model="credentials.username"
              type="text"
              placeholder="نام کاربری خود را وارد کنید"
              @input="clearError"
              required
            >
          </div>
          <div class="form-group">
            <label for="password">رمز عبور</label>
            <input
              id="password"
              v-model="credentials.password"
              type="password"
              placeholder="رمز عبور خود را وارد کنید"
              @input="clearError"
              required
            >
          </div>
          <div v-if="errorMessage" class="error-message">
            <span>{{ errorMessage }}</span>
          </div>
          <button
            type="submit"
            class="btn-login"
            :disabled="isLoading"
          >
            {{ isLoading ? 'در حال ورود...' : 'ورود' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { adminAuthService } from '../services/api';

export default {
  name: 'AdminLogin',
  data() {
    return {
      credentials: {
        username: '',
        password: ''
      },
      isLoading: false,
      errorMessage: ''
    }
  },
  provide() {
    return {
      navigateTo: this.navigateTo
    }
  },
  inject: ['navigateTo'],
  methods: {
    async handleLogin() {
      this.errorMessage = '';

      if (!this.credentials.username || !this.credentials.password) {
        this.errorMessage = 'لطفا نام کاربری و رمز عبور را وارد کنید';
        return;
      }

      this.isLoading = true;

      try {
        const response = await adminAuthService.login({
          username: this.credentials.username,
          password: this.credentials.password
        });

        // Store token
        localStorage.setItem('admin_token', response.data.access_token);

        // Navigate to dashboard
        this.navigateTo('/admin');
      } catch (error) {
        console.error('Login error:', error);
        this.errorMessage = error.response?.data?.detail || 'خطا در ورود. لطفا دوباره تلاش کنید.';
      } finally {
        this.isLoading = false;
      }
    },
    clearError() {
      this.errorMessage = '';
    }
  }
}
</script>

<style scoped>
.admin-login {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 400px;
}

.login-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.login-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 30px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: right;
}

.form-group label {
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
  font-size: 14px;
}

.form-group input {
  padding: 12px 15px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #1abc9c;
}

.form-group input::placeholder {
  color: #999;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 10px 15px;
  border-radius: 6px;
  font-size: 14px;
  text-align: center;
}

.btn-login {
  background: #1abc9c;
  color: white;
  padding: 12px 40px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  font-size: 16px;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.btn-login:hover:not(:disabled) {
  background: #16a085;
  transform: translateY(-1px);
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }

  .login-title {
    font-size: 20px;
  }

  .form-group input {
    padding: 10px 12px;
  }

  .btn-login {
    padding: 10px 30px;
    font-size: 14px;
  }
}
</style>