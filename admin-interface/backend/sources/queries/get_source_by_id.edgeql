SELECT Source {
    id,
    name,
    type,
    url,
    is_active,
    created_at,
    updated_at
}
FILTER .id = <uuid>$source_id
