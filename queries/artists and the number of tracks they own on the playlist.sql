SELECT C.artist_id, C.artist_name, COUNT(*) as count
FROM track as A
JOIN album as B
ON A.album_id = B.album_id
JOIN artist as C
ON B.album_owner_id = C.artist_id
GROUP BY C.artist_id, C.artist_name
ORDER BY count DESC