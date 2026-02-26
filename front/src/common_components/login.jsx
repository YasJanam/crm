import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import '../style/login.css';

function LoginPage() {
    const navigate = useNavigate();
    const [loading,setLoading] = useState(false);
    const [error,setError] = useState('');

    const [data,setData] = useState({
        username:'',
        password:''
    });

    const handleChange = (e) => {
        const {name,value} = e.target;
        setData(prev => ({
            ...prev,
            [name]:value
        }));

        if (error) setError('');
    };


    const handleSubmit = async(e) => {
        e.preventDefault();

        const {username,password} = data;

        if (!username || !password){
            setError('لطفاً همه فیلدها را پر کنید');
            return;
        }

        setLoading(true);
        setError('');

        try{
            const tokenResponse = await api.post('/api/token/',{
                username,
                password
            });

            const {access,refresh} = tokenResponse.data;

            localStorage.setItem('access_token',access);
            localStorage.setItem('refresh_token',refresh);

            api.defaults.headers.common['Authorization'] = `Bearer ${access}`;


            const userResponse = await api.get('/user-role/');
            const userData = userResponse.data;

            localStorage.setItem('role',userData.role);
            localStorage.setItem('user_id',userData.id);
            localStorage.setItem('user',JSON.stringify(userData));


            if (userData.role === 'admin'){
                navigate('/adminpanel');
            }else if (userData.role === 'salemanager'){
                navigate('/managerpanel');
            }else if (userData.role === 'saler'){
                navigate('/salerpanel');
            }


        }catch(err){
            console.error('خطای لاگین:', err);

     if (err.response) {
     
        if (err.response.status === 401) {

          setError('نام کاربری یا رمز عبور اشتباه است');
        } else if (err.response.status === 400) {
          setError(err.response.data.detail || 'اطلاعات وارد شده معتبر نیست');
        } else {
          setError('خطای سرور. لطفاً بعداً تلاش کنید');
        }

      } else if (err.request) {
        setError('خطا در ارتباط با سرور');
      } else {
      console.error('🔴 خطای ناشناخته جزئیات:', err);
      setError(`خطا: ${err.message || 'ناشناخته'}`);
      }           
        }finally {
            setLoading(false);
        }
    };

    const goToRegister = () => {
        navigate('/register');
    };

    return (
        <div className='login-page'>
        <div className='login-container'>
            <h2>ورود به پنل</h2>
            <form onSubmit={handleSubmit}>
                <input
                type="text"
                name = 'username'
                value={data.username}
                onChange={handleChange}
                disabled={loading}
                />

                <input
                type='password'
                name = 'password'
                value={data.password}
                onChange={handleChange}
                disabled={loading}
                />

                <button
                    type="submit"
                    disabled={loading}
                    onClick={handleSubmit}
                    className={loading ? 'loading' : ''}
                >
                    {loading? (
                        <span>
                            در حال ورود ...
                        </span>
                    ) : 'ورود'}
                </button>
            </form>

            <button
                onClick={goToRegister}
                disabled={loading}
                className="register-btn"
            >
                ثبت نام
            </button>


            <div className="login-footer">
                <a href='/forget-password'>
                رمز عبور را فراموش کرده‌اید؟
                </a>
            </div>
        </div>
        </div>
    )
}

export default LoginPage;