SELECT User {
    username
}
FILTER .username = <str>$username AND .password_hash = <str>$password_hash
