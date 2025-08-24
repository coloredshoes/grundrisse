INSERT User {
    username := <str>$username,
    password_hash := <str>$password_hash
} UNLESS CONFLICT ON .username
