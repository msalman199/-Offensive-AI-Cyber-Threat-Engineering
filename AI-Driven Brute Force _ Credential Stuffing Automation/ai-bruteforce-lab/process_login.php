<?php
if ($_POST['username'] == 'admin' && $_POST['password'] == 'password') {
    echo "<h2>Welcome to Dashboard!</h2>";
    echo "<p>Login successful</p>";
    echo "<a href='logout.php'>Logout</a>";
} else {
    echo "<h2>Login Failed</h2>";
    echo "<p>Invalid username or password</p>";
    echo "<a href='login.html'>Try Again</a>";
}
?>
