import React, { useState } from "react";

function LoginForm({ onLogin }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
  
    function handleSubmit(event) {
      event.preventDefault();
      // TODO perform a login request
      // TODO show an error message.
      onLogin(true)
    }
  
    return (
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input
            type="text"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />
        </label>
        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>
        <button type="submit">Login</button>
      </form>
    );
  }

  export default LoginForm;