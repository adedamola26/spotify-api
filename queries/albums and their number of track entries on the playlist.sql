SELECT A.album_id, A.album_name, COUNT(*) as count
FROM album as A
JOIN track as B
on A.album_id = B.album_id
GROUP BY A.album_id, A.album_name
ORDER BY count DESC

