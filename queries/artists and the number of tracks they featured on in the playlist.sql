SELECT c.artist_name, COUNT(*) AS count
FROM track as A 
JOIN collab as B
on A.track_id = B.track_id
JOIN artist as C
on B.artist_id = C.artist_id
GROUP BY (c.artist_id, c.artist_name)
ORDER BY count DESC
